# Fusion Plugin

The fusion plugin identifies oncogenic fusions in tumour samples.

## Pipeline
Uses Isofox

## Plugin Breakdown

The plugin is composed of the following files:
- **plugin.py**:
    - The main code
    - It calls configure, extract, and render methods to generate the fusions section
- **preprocess.py**:
    - Called by extract
    - Performs data wrangling on isofox fusion output
    - Annotates the fusions using the oncokb annotator
    - Outputs the following files to the workspace:
        - "data_fusions.txt"
        - "data_fusions_oncokb.txt"
        - "data_fusions_obcokb_annotated.txt"
        - "data_fusions_NCCN.txt"
- **tools.py**:
    - Called by extract
    - Uses output from preprocess.py to assemble all data for the fusions section
- **fusion_template.html**:
    - Called by render
    - Contains the template for rendering fusions in the clinical report 
- **html.py**:
    - Called by fusion_template.html
    - Assembles tables to be rendered
- **constants.py**:
    - Called by various files
    - Contains constants shared throughout the plugin
- **test/**
    - A directory containing all data to run the fusion plugin test  

## Preprocess Filtering 

### Preprocessing Isofox

The function that preprocesses the isofox file is preprocess.py/process_isofox

The following filtering steps are applied to the isofox output ${sample_name_tumour}.isf.pass_fusions.csv:
1. **self.add_tumour_id**: A column called "Sample" is added. This is a column with the tumour ID for every row.
2. **self.write_fusion_pairs**: A column is made to concatenate gene1-gene2 based on "GeneNameUp" and "GeneNameDown".
3. **self.get_clean_fusions**: Deduplicate fusions regardless of orientation (Up-Down vs Down-Up). The entry with the highest "TotalFragments" will be kept.
4. **self.process_svtype**: Maps acronyms in the "SVType" column to full names, and update translocation and inversion notations.
   
### Annotating OncoKB and NCCN variants 

The function that writes the files is still preprocess.py/write_fusion_files

It does the following to the preprocessed isofox data:
1. **self.process_nccn**: Filters data for only NCCN fusions (as described in djerba/data/NCCN_annotations.txt). 
2. **self.df_for_oncokb_annotator**: Prepares the data for the oncokb annotator. 
3. Outputs data_fusions.txt (for interpretation), data_fusions_NCCN.txt (for oncokb annotator), and data_fusions_oncokb.txt (for oncokb annotator) to the workspace.

## Additional filtering in tools.py

There is some minor filtering that happens when generating the fusion counts:
- **Clinically relevant variants**: this number is calculated from data_fusions_oncokb_annotated.txt. It only counts those entries for which the mutation effect is not "Unknown".
- **NCCN relevant variants**: this number is calculated from data_fusions_NCCN.txt, and only counts those fusions for which the fusion is not a Gene-None or None-Gene fusion. It does not care if those fusions have Unknown effect or not, only that there are NCCN fusions.
- **Total variants**: this number is calculated from data_fusions.txt. "None" fusions are counted as 1 gene. Ex. if "FGFR2-KRAS" and "CDKN2A-None" fusions were found, the count would be 3.

## History

See the [changelog](./CHANGELOG.md) for a detailed development history. In brief:

- **2025-03**: Created this README.md

