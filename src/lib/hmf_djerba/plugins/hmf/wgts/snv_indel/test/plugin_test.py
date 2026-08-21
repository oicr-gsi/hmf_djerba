#! /usr/bin/env python3

"""
Test of the HMF WGTS SNV/indel plugin
"""

import os
import unittest
from hmf_djerba.plugins.plugin_tester_hmf import PluginTesterHMF

class TestSnvIndelPlugin(PluginTesterHMF):

    INI_NAME = 'snv_indel.ini'
    JSON_NAME = 'snv_indel.json'
    
    def testSnvIndel(self):
        data_dir = os.path.join(self.test_dir, 'plugins', 'wgts', 'snv_indel')
        maf_filename = 'BTC-0124-03-LB01-01.sage.somatic.maf.gz'
        maf_path = os.path.join(data_dir, maf_filename)
        mapping = {'MAF_PATH': maf_path}
        input_dir, work_dir = self.writeTestFiles(data_dir, mapping)
        params = {
            self.INI: self.INI_NAME,
            self.JSON: self.JSON_NAME,
            self.MD5: 'e9d874c2e0f7449b56fc674bd9198dd6'
        }
        self.run_basic_test(input_dir, params, work_dir=work_dir)

    def redact_json_data(self, data):
        """replaces empty method from testing.tools"""
        del data['results']['vaf_plot']
        return data 

if __name__ == '__main__':
    unittest.main()
