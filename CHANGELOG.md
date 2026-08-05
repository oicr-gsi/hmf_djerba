# CHANGELOG

## v0.0.4: 2026-08-05
- Modified genomic landscape plugin to support HRD CHORD output from HMF (cannot currently find the files automatically; must be specified in the config)
- Modified genomic landscape plugin to support MSI PURPLE output from HMF (cannot currently find the files automatically; must be specified in the config)
- Minor plot fixes to HMF HRD plugin
- Updated the Purple plugin to support directory input instead of a ZIP file and to generate a populated purple.alternate.json for potential manual runs.
- Updated the expression plugin to support HMF output and to use TPM instead of FPKM.
- Updated fusion, cnv, and snv_indel plugins to support changes to `djerba.util` in Djerba v1.11.11
- Implement integration test that verifies the compatibility between HMF_Djerba and Djerba.
- Use new RODiC database rebuilt using TPM-based data from TCGA GDC.

## v0.0.3: 2025-12-04
- More name fixes in `setup.py`

## v0.0.2: 2025-12-04
- Fix plugin names in `setup.py`
- Add a changelog

## v0.0.1: 2025-12-02
- Initial development release
