#! /usr/bin/env python3

"""
Test of the genomic_landscape plugin
"""

import os
import unittest
from shutil import copy
from hmf_djerba.plugins.plugin_tester_hmf import PluginTesterHMF

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
        params = {
            self.INI: self.INI_NAME,
            self.JSON: self.JSON_NAME,
            self.MD5: '496d9830f4dbbe46b30b39506171a722'
        }
        self.run_basic_test(input_dir, params, work_dir=work_dir)

    def redact_json_data(self, data):
        """replaces empty method from testing.tools"""
        plot_key = 'Genomic biomarker plot'
        for key in ['HRD','TMB','MSI']:
            data['results']['genomic_biomarkers'][key][plot_key] = self.BLANK
        return data

if __name__ == '__main__':
    unittest.main()
