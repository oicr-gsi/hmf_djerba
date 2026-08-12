#! /usr/bin/env python3

"""
Test of the HMF WGTS CNV-Purple plugin
"""

import os
import unittest
import tempfile
import string

from shutil import copy

from djerba.util.validator import path_validator
from djerba.plugins.plugin_tester import PluginTester
import hmf_djerba.plugins.hmf.wgts.cnv_purple.plugin as cnv
from djerba.core.workspace import workspace
from djerba.util.environment import directory_finder

class TestPurplePlugin(PluginTester):

    INI_NAME = 'cnv_purple.ini'
    JSON_NAME = 'cnv_purple.json'

    def setUp(self):
        super().setUp()
        self.path_validator = path_validator()
        self.maxDiff = None
        self.test_dir = os.environ.get('HMF_DJERBA_TEST_DIR')

    def testWGTScnv(self):
        data_dir = os.path.join(self.test_dir, 'plugins', 'wgts', 'cnv_purple')
        purple_dir = os.path.join(data_dir, 'purple')
        with open(os.path.join(data_dir, self.INI_NAME)) as in_file:
            template_str = in_file.read()
        template = string.Template(template_str)
        ini_str = template.substitute({'PURPLE': purple_dir})
        input_dir = os.path.join(self.get_tmp_dir(), 'input')
        os.mkdir(input_dir)
        with open(os.path.join(input_dir, self.INI_NAME), 'w') as ini_file:
            ini_file.write(ini_str)
        copy(os.path.join(data_dir, self.JSON_NAME), input_dir)
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
