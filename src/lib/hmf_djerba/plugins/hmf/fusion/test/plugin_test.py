#!/usr/bin/env python3

"""Test of the fusions plugin"""

import os
import unittest
from hmf_djerba.plugins.plugin_tester_hmf import PluginTesterHMF

class TestFusion(PluginTesterHMF):

    INI_NAME = 'fusion.ini'
    JSON_NAME = 'fusion.json'

    def testFusion(self):
        data_dir = os.path.join(self.test_dir, 'plugins', 'fusion')
        isf_filename = 'BTC-0124-03-LB03-01.isf.pass_fusions.csv' # isofox
        isf_path = os.path.join(data_dir, isf_filename)
        mapping = {'ISOFOX_PATH': isf_path}
        input_dir, work_dir = self.writeTestFiles(data_dir, mapping)
        params = {
            self.INI: self.INI_NAME,
            self.JSON: self.JSON_NAME,
            self.MD5: 'c3963040dabfa2a06823b42fd6b1bed7'
        }
        self.run_basic_test(input_dir, params, work_dir=work_dir)

if __name__ == '__main__':
    unittest.main()

