#! /usr/bin/env python3

"""
Test of the HMF WGTS CNV-Purple plugin
"""

import os
import unittest
from hmf_djerba.plugins.plugin_tester_hmf import PluginTesterHMF

class TestPurplePlugin(PluginTesterHMF):

    INI_NAME = 'cnv_purple.ini'
    JSON_NAME = 'cnv_purple.json'

    def testCNVPurple(self):
        data_dir = os.path.join(self.test_dir, 'plugins', 'wgts', 'cnv_purple')
        purple_dir = os.path.join(data_dir, 'purple')
        mapping = {'PURPLE': purple_dir}
        input_dir, work_dir = self.writeTestFiles(data_dir, mapping)
        params = {
            self.INI: self.INI_NAME,
            self.JSON: self.JSON_NAME,
            self.MD5: '2852815e5eb2b686d39c9cf51821ab2e'
        }
        self.run_basic_test(input_dir, params)

    def redact_json_data(self, data):
        """replaces empty method from testing.tools"""
        del data['results']['cnv plot']
        return data
    
if __name__ == '__main__':
    unittest.main()
