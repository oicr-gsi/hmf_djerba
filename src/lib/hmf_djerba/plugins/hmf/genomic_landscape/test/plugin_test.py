#! /usr/bin/env python3

"""
Test of the genomic_landscape plugin
"""

import csv
import json
import logging
import os
import unittest
from shutil import copy
import hmf_djerba.plugins.hmf.wgts.cnv_purple.constants as purple_constants
from hmf_djerba.plugins.plugin_tester_hmf import PluginTesterHMF
from hmf_djerba.plugins.hmf.genomic_landscape.tmb import tmb_processor

class TestGenomicLandscapePlugin(PluginTesterHMF):
    
    INI_NAME = 'genomic_landscape.ini'
    JSON_NAME = 'genomic_landscape.json'
    BLANK = "INTENTIONALLY BLANK FOR TESTING"

    def testGenomicLandscape(self):
        data_dir = os.path.join(self.test_dir, 'plugins', 'genomic_landscape')
        msi_filename = 'BTC-0124-03-LB01-01.purple.purity.tsv'
        hrd_filename = 'BTC-0124-03-LB01-01.chord.prediction.tsv'
        mapping = {
            'MSI_PATH': os.path.join(data_dir, msi_filename),
            'HRD_PATH': os.path.join(data_dir, hrd_filename)
        }
        input_dir, work_dir = self.writeTestFiles(data_dir, mapping)
        # Not an INI parameter, but plugin implicitly assumes this file is present
        copy(os.path.join(data_dir, 'data_mutations_extended.txt'), work_dir)
        # purity for HRD/MSI reportability is read from purity_ploidy.json, normally written
        # by the cnv_purple plugin; take the value from the PURPLE purity file in the test data
        with open(os.path.join(data_dir, msi_filename)) as purity_file:
            purity = float(next(csv.DictReader(purity_file, delimiter="\t"))['purity'])
        with open(os.path.join(work_dir, purple_constants.PURITY_PLOIDY), 'w') as out_file:
            json.dump({purple_constants.PURITY: purity}, out_file)
        params = {
            self.INI: self.INI_NAME,
            self.JSON: self.JSON_NAME,
            self.MD5: '753bed1012632b361ff08706ce0fb0ca'
        }
        self.run_basic_test(input_dir, params, work_dir=work_dir)

    def testMergedTcgaCodeCohort(self):
        # contains the TMB comparison files
        data_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        tmb = tmb_processor(log_level=logging.ERROR, log_path=None)
        # merged codes are joined with '/' for display
        self.assertEqual(tmb.read_cohort(data_dir, "luad|lusc"), "TCGA LUAD/LUSC")
        # a single code is unchanged
        self.assertEqual(tmb.read_cohort(data_dir, "luad"), "TCGA LUAD")
        self.assertEqual(tmb.read_cohort(data_dir, "paad"), "COMPASS")
        self.assertEqual(tmb.read_cohort(data_dir, "zzz"), "NA")
        # the merged percentile pools both cohorts, it does not pick one of them
        self.assertEqual(tmb.read_cancer_specific_percentile(data_dir, 2.5, "TCGA LUAD", "luad"), 19)
        self.assertEqual(tmb.read_cancer_specific_percentile(data_dir, 2.5, "TCGA LUSC", "lusc"), 3)
        self.assertEqual(tmb.read_cancer_specific_percentile(data_dir, 2.5, "TCGA LUAD/LUSC", "luad|lusc"), 12)

    def redact_json_data(self, data):
        """replaces empty method from testing.tools"""
        plot_key = 'Genomic biomarker plot'
        for key in ['HRD','TMB','MSI']:
            data['results']['genomic_biomarkers'][key][plot_key] = self.BLANK
        return data

if __name__ == '__main__':
    unittest.main()
