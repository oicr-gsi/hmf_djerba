"""
Fusion pre-processing of isofox files, as well as annotation.
Replaces legacy R script: fusions.R

Intended for Hartwig Isofox fusion data.
"""

import csv
import logging
import os
import re
import pandas as pd
import numpy as np
from djerba.util.logger import logger
from djerba.util.environment import directory_finder
from djerba.util.oncokb.tools import levels as oncokb_levels
from djerba.util.oncokb.annotator import annotator_factory
import hmf_djerba.plugins.hmf.fusion.constants as fc
import djerba.core.constants as core_constants
from djerba.util.subprocess_runner import subprocess_runner
pd.set_option('future.no_silent_downcasting', True)

class prepare_fusions(logger):

    def __init__(self, work_dir, log_level=logging.WARNING, log_path=None):
        super().__init__()
        self.log_level = log_level
        self.log_path = log_path
        self.logger = self.get_logger(log_level, __name__, log_path)
        self.work_dir = work_dir
        self.data_dir = directory_finder(log_level, log_path).get_data_dir()

    def annotate_fusion_files(self, config_wrapper):
        # annotate from OncoKB
        # TODO check if fusions are non empty
        factory = annotator_factory(self.log_level, self.log_path)
        factory.get_annotator(self.work_dir, config_wrapper).annotate_fusion()

    def process_fusion_files(self, config_wrapper): 
        """
        MAIN FUNCTION, called by Extract.
        
        Inputs:
        - isofox file
        - tumour id
        - oncotree code

        Outputs:
        - main fusions file with isofox information
        - annotated oncokb file
        """

        isofox_path = config_wrapper.get_my_string(fc.ISOFOX_PATH)
        if not isofox_path:
            msg = "Could not find isofox file. Perhaps you need to manually specify it?"
            self.logger.error(msg)
            raise FileNotFoundError(msg)

        tumour_id = config_wrapper.get_my_string(core_constants.TUMOUR_ID)
        oncotree_code = config_wrapper.get_my_string(fc.ONCOTREE_CODE)
        oncotree_code = oncotree_code.upper()
        min_reads = config_wrapper.get_my_int(fc.MIN_FUSION_READS)
        
        self.logger.info("Processing fusion (isofox) results and writing fusion files")
        df_isofox = self.process_isofox(isofox_path, tumour_id, min_reads)
        self.write_fusion_files(df_isofox, oncotree_code)
        self.annotate_fusion_files(config_wrapper)
        self.logger.info("Finished writing fusion files")
    
    def add_tumour_id(self, df, tumour_id):
        """
        Adds a column with the tumour id
        """
        df["Sample"] = tumour_id
        return df
        
    def process_isofox(self, isofox_path, tumour_id, min_reads):
        """
        Process linx information via pandas dataframe operations.
        Processing includes changing column names and writing fusion pairs for merging with mavis.
        Returns a processed isofox dataframe.
        """
        # Get the data_frame if the isofox path is not completely empty:
        # Note: the code should work even if there is only a header.
        if os.path.getsize(isofox_path) != 0:
            df_isofox = pd.read_csv(isofox_path, sep = ',') # isofox output csv file, while linx output tsv file
            # First a column with tumor id
            df_isofox = self.add_tumour_id(df_isofox, tumour_id)    
            # Add fusion tuples as well, for merging with mavis
            df_isofox = self.write_fusion_pairs(df_isofox, "GeneNameUp", "GeneNameDown")
            # Remove duplicated fusions regardless of orientation (Up-Down vs Down-Up).
            df_isofox = self.get_clean_fusions(df_isofox)
            # Map acronyms to full name for the SVType column & update translocation and inversion notation
            df_isofox = self.process_svtype(df_isofox)
        else:
            msg = "Isofox file is completely empty (no header)."
            self.logger.info(msg)
            df_isofox = pd.DataFrame()

        return df_isofox
    
    def get_clean_fusions(self, df):
        """
        Deduplicates fusions regardless of orientation (Up-Down vs Down-Up).
        Keeps the entry with the highest TotalFragments.
        """
        # Create a temporary order-agnostic key for deduplication
        # This sorts the genes alphabetically ONLY for the purpose of finding duplicates
        df["dedup_key"] = df.apply(
            lambda row: "-".join(sorted([str(row["GeneNameUp"]), str(row["GeneNameDown"])])), 
            axis=1
        )

        # Sort by TotalFragments, keep the first and remove the temporary key column
        df = df.sort_values(by="TotalFragments", ascending=False)
        df = df.drop_duplicates(subset=["dedup_key"], keep="first")
        df = df.drop(columns=["dedup_key"])

        return df
        
    def process_svtype(self, df):
        """
        1. Map acronyms to full name for the SVType column
        2. Update translocation and inversion notation
        """
        mapping = {
            'BND': 'Translocation',
            'SGL': 'Single breakend',
            'DEL': 'Deletion',
            'INS': 'Insertion',
            'DUP': 'Duplication',
            'INV': 'Inversion',
            'INF': 'Inferred'
        }
        df["SVType"] = df["SVType"].replace(mapping)

        # Update translocation and inversion notation
        df = self.change_translocation_and_inversion_notation(df)

        return df

    def change_translocation_and_inversion_notation(self, df):
        """
        Translocations should be in t(min_chr;max_chr) notation with X always on the right.
        Inversion should be in v(chr) notation.
        """

        def process_translocation_notation(chrom1, chrom2):
            chrom1 = chrom1.replace("chr", "")
            chrom2 = chrom2.replace("chr", "")
            if chrom1 == "X" or chrom2 == "X":
                return f"t({min(chrom1, chrom2)};X)" 
            elif chrom1 == "Y" or chrom2 == "Y":
                return f"t({min(chrom1, chrom2)};Y)"
            else:
                chrom1_num = int(chrom1)
                chrom2_num = int(chrom2)
                return f"t({min(chrom1_num, chrom2_num)};{max(chrom1_num, chrom2_num)})"
            
        def process_inversion_notation(chrom1):
            chrom1 = chrom1.replace("chr", "")
            return f"inv({chrom1})"
        
        
        def update_svtype(row):
            if "Translocation" in row["SVType"]:
                return process_translocation_notation(row["ChrUp"], row["ChrDown"])
            elif "Inversion" in row["SVType"]:
                return process_inversion_notation(row["ChrUp"])
            else:
                return row["SVType"]

        df["SVType"] = df.apply(update_svtype, axis=1)

        return df


    def process_nccn(self, df_isofox, oncotree_code):
        """
        Looks only at the NCCN translocations in djerba/data/NCCN_annotations.txt
        Makes the nccn dataframe that will be ready for input into the oncokb annotator.
        The annotator only requires two columns:
            1. Tumor_Sample_Barcode     (ex. OCT2-01-0014-ARC_SE24-0335)
            2. Fusion (ex. KRAS-FGFR2)
        It is deduplicated further as the oncokb annotator does not care about event types.
        We also remove any fusion pairs with None as they will not be reported in Djerba.
        """

        df_annotations = pd.read_csv(os.path.join(self.data_dir, fc.NCCN_ANNOTATION_FILE), sep = '\t')
        
        marker_dict = dict(zip(df_annotations["marker"], df_annotations["oncotree"]))

        dict_nccn = {"Tumor_Sample_Barcode":[], "Fusion": []}
        for row in df_isofox.iterrows():
            svtype = row[1]["SVType"]
            if svtype in marker_dict and oncotree_code == marker_dict[svtype]:
                dict_nccn["Fusion"].append(row[1]["fusion_pairs"])
                dict_nccn["Tumor_Sample_Barcode"].append(row[1]["Sample"])

        df_nccn = pd.DataFrame(dict_nccn)
        return df_nccn

    def write_fusion_files(self, df_isofox, oncotree_code):
        """
        Writes data_fusions.txt to the workspace.
        It also writes data_fusions_oncokb.txt to the workspace.
        This is for the oncokb annotator to use.
        It looks like:

        Sample          Fusion
        my_sample_id    ACTN1-DACH2
        my_sample_id    BROX-FGFR2
        my_sample_id    DENND2C-PKN2
        ...             ...

        This function does not return anything.
        """

        # Get the NCCN calls
        df_nccn = self.process_nccn(df_isofox, oncotree_code)

        # Make the dataframe for oncokb annotation
        df_oncokb = self.df_for_oncokb_annotator(df_isofox)

        # Write data_fusions.txt to the workspace for main reporting task
        df_isofox.to_csv(os.path.join(self.work_dir, fc.DATA_FUSIONS), index = False, sep = "\t")
        
        # Write data_fusions_oncokb.txt to the workspace for annotation task
        df_oncokb.to_csv(os.path.join(self.work_dir, fc.DATA_FUSIONS_ONCOKB), index = False, sep = "\t")

        df_nccn.to_csv(os.path.join(self.work_dir, fc.DATA_FUSIONS_NCCN), index = False, sep = "\t")

    def write_fusion_pairs(self, df, column1, column2):
        """
        Takes genes in GeneNameUp and GeneNameDown and concatonates with ::
        Ex. 
    
        geneStart    geneEnd
        FGFR2        KRAS
        
        Will make a third column
        
        GeneNameUp    GeneNameDown      fusion_pairs
        FGFR2         KRAS              FGFR2-KRAS
        
        The new delimiter is ::, but - is used for now as OncoKB requires it.
        It always orders it alphabetically.
        """
        # First change all nans to the string None
        df[column1] = df[column1].replace({np.nan: None})
        df[column2] = df[column2].replace({np.nan: None})
    
        
        # Make fusion tuples 
        df["fusion_pairs"] = df.apply(lambda row: "-".join([str(row[column1]), str(row[column2])]), axis=1)
        return df 

    def df_for_oncokb_annotator(self, df):
        """
        Makes the dataframe that will be ready for input into the oncokb annotator.
        The annotator only requires two columns:
            1. Tumor_Sample_Barcode	(ex. OCT2-01-0014-ARC_SE24-0335)
            2. Fusion (ex. KRAS-FGFR2)
        It is deduplicated further as the oncokb annotator does not care about event types.
        We also remove any fusion pairs with None as they will not be reported in Djerba.
        """
        new_df = df[["Sample", "fusion_pairs"]].copy()
        new_df = self.drop_duplicates(new_df, ["fusion_pairs"])
        new_df["fusion_pairs"] = new_df["fusion_pairs"].astype(str)
        new_df = new_df[~new_df["fusion_pairs"].str.contains("None")]
        # Change headers
        new_df.rename(columns={'Sample': 'Tumor_Sample_Barcode', 'fusion_pairs': 'Fusion'}, inplace=True)

        return new_df
    
    def drop_duplicates(self, df, columns):
        """
        """
        df = df.drop_duplicates(subset=columns)
        return df

class FileNotFoundError(Exception):
    pass
