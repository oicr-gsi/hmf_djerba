CNV_PLOT = 'cnv plot'
PURITY = 'purity'
PLOIDY = 'ploidy'
PLOTNINE_VERBOSE = 'plotnine_verbose'

# FILE NAMES
PURPLE_PURITY_RANGE = "purple_purity_file"
PURPLE_CNV = "purple_cnv_file"
PURPLE_SEG = "purple_segment_file"
PURPLE_GENE = "purple_gene_file"
PURPLE_DIR = "purple_dir"
PURPLE_ALT = "purple.alternate.json"
PURITY_PLOIDY = "purity_ploidy.json"
TEMPLATE_NAME = 'cnv_template.html'

# WORKFLOWS
PURPLE = 'purple'
GRIDSS = "gridss"
MUTECT2 = "mutect2_matched"
BMPP = "bamMergePreprocessing_by_sample"

# HTML
BODY = 'body'
CLINICALLY_RELEVANT_VARIANTS = 'clinically relevant variants'
HAS_EXPRESSION_DATA = 'has expression data'
PERCENT_GENOME_ALTERED = 'percent genome altered'
TOTAL_VARIANTS = 'total variants'

# purple alternate solutions launcher
ALT_REF_FASTA = "/.mounts/labs/gsi/src/hmftools/ref_data/GRCh38_hmf/25.1/" \
    "GRCh38_masked_exclusions_alts_hlas.fasta"
ALT_REF_FAI = ALT_REF_FASTA + ".fai"
ALT_NORMAL_CRAM = "normal.cram"
ALT_NORMAL_CRAM_INDEX = ALT_NORMAL_CRAM + ".crai"
ALT_TUMOUR_CRAM = "tumour.cram"
ALT_TUMOUR_CRAM_INDEX = ALT_TUMOUR_CRAM + ".crai"
ALT_SAGE_VCF_SUFFIX = ".sage.somatic.vcf.gz"
ALT_SAGE_VCF_INDEX_SUFFIX = ALT_SAGE_VCF_SUFFIX + ".tbi"

# data files
CENTROMERES = "hg38_centromeres.txt"
GENEBED =  "gencode_v44_hg38_genes.bed"
ONCOLIST =  "20251008-oncoKBcancerGeneList.tsv"

# whizbam
WHIZBAM_BASE_URL = 'https://whizbam.oicr.on.ca'
WHIZBAM_SEQTYPE = 'GENOME'
WHIZBAM_GENOME_VERSION = 'hg38'
WHIZBAM_PROJECT = 'whizbam_project'

# variables so short they're hard to search for
ALT = 'Alteration'
NA = 'NA'

