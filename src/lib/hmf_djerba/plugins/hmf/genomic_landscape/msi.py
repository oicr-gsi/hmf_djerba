"""
List of functions to convert MSI information into json format.
"""

# IMPORTS
import csv
import os

import numpy

import hmf_djerba.plugins.hmf.genomic_landscape.constants as constants
from djerba.util.image_to_base64 import converter
from djerba.util.logger import logger
from djerba.util.subprocess_runner import subprocess_runner
from djerba.util.validator import path_validator

class msi_processor(logger):

    def __init__(self, log_level, log_path):
        self.log_level = log_level
        self.log_path = log_path
        self.logger = self.get_logger(log_level, __name__, log_path)
        self.validator = path_validator(log_level, log_path)

    def run(self, work_dir, msi_file, biomarkers_path, tumour_id):
        """
          Runs all functions below.
          Assembles a chunk of json.
          """
        msi_summary = self.preprocess_msi(work_dir, msi_file)
        msi_data = self.assemble_MSI(work_dir, msi_summary)

        # Write to genomic biomarkers maf if MSI is actionable
        if msi_data[constants.METRIC_ACTIONABLE]:
            self.validator.validate_input_file(biomarkers_path)
            with open(biomarkers_path, "a") as biomarkers_file:
                row = '\t'.join([constants.HUGO_SYMBOL, tumour_id, msi_data[constants.METRIC_ALTERATION]])
                biomarkers_file.write(row + "\n")

        return msi_data

    def preprocess_msi(self, work_dir, msi_file):
        """
          summarize purple MSI-related values
        """
        out_path = os.path.join(work_dir, 'msi.txt')
        self.validator.validate_output_dir(work_dir)
        self.validator.validate_input_file(msi_file)
        
        with open(msi_file, 'r') as msi_file:
            reader_file = list(csv.reader(msi_file, delimiter="\t"))
            purple_msi_header = reader_file[0]
            purple_msi_data = reader_file[1]
            
            # Find the column positions
            idx1 = purple_msi_header.index("msIndelsPerMb")
            idx2 = purple_msi_header.index("msStatus")
        
            # Store the values in a list
            msi_perc = [purple_msi_data[idx1], purple_msi_data[idx2]]

        with open(out_path, 'w') as out_file:
            print("\t".join([str(item) for item in msi_perc]), file=out_file)
        return out_path

    def assemble_MSI(self, work_dir, msi_summary):
        msi_value, msi_status = self.extract_MSI(work_dir, msi_summary)
        msi_dict = self.call_MSI(msi_value, msi_status)
        
        return msi_dict

    def call_MSI(self, msi_value, msi_status):
        """convert MSI percentage into a Low, Unknown or High call"""
        msi_dict = {constants.ALT: constants.MSI,
                    constants.ALT_URL: "https://www.oncokb.org/gene/Other%20Biomarkers/MSI-H",
                    constants.METRIC_VALUE: msi_value
                    }
        try:
            if msi_status == "MSI":
                msi_dict[constants.METRIC_ACTIONABLE] = True
                msi_dict[constants.METRIC_ALTERATION] = "MSI-H"
                msi_dict[constants.METRIC_TEXT] = "Microsatellite Instability High (MSI-H)"
            elif msi_status == "UNKNOWN":
                msi_dict[constants.METRIC_ACTIONABLE] = False
                msi_dict[constants.METRIC_ALTERATION] = "UNKNOWN"
                msi_dict[constants.METRIC_TEXT] = "Unknown Microsatellite Instability status"
            elif msi_status == "MSS":
                msi_dict[constants.METRIC_ACTIONABLE] = False
                msi_dict[constants.METRIC_ALTERATION] = "MSS"
                msi_dict[constants.METRIC_TEXT] = "Microsatellite Stable (MSS)"
            else:
                # shouldn't happen, but include for completeness
                msg = f'Cannot evaluate for MSI status {msi_status}'
                self.logger.error(msg)
                raise RuntimeError(msg)
        except TypeError:
            msg = "Illegal value '{0}' extracted from file for MSI; must be a string".format(msi_status)
            self.logger.error(msg)
            raise RuntimeError(msg)
        return (msi_dict)

    def extract_MSI(self, work_dir, msi_path):
        if msi_path is None:
            msi_path = os.path.join(work_dir, constants.MSI_FILE_NAME)
        self.validator.validate_input_file(msi_path)
        with open(msi_path, 'r') as msi_file:
            reader_file = csv.reader(msi_file, delimiter="\t")
            for row in reader_file:
                try:
                    msi_value = float(row[0])
                    msi_status = str(row[1])
                except IndexError as err:
                    msg = "Incorrect number of columns in msi file: '{0}'".format(row) + \
                          "read from '{0}'".format(os.path.join(work_dir, constants.MSI_FILE_NAME))
                    self.logger.error(msg)
                    raise RuntimeError(msg) from err
        return msi_value, msi_status

