#! /usr/bin/env python3

"""
Test of the WGTS SNV/indel plugin
"""

import os
import unittest
import string
import tempfile
from shutil import copy
from djerba.util.validator import path_validator
from djerba.plugins.plugin_tester import PluginTester
import djerba.plugins.wgts.snv_indel.plugin as snv_indel
from djerba.core.workspace import workspace
from djerba.util.environment import directory_finder

class TestSnvIndelPlugin(PluginTester):

    INI_NAME = 'snv_indel.ini'
    JSON_NAME = 'snv_indel.json'
    JSON_NAME_NO_CNV = 'snv_indel_no_cnv.json'
    JSON_NAME_NO_MUT = 'snv_indel_no_somatic_mutations.json'
    
    def setUp(self):
        super().setUp()
        self.path_validator = path_validator()
        self.maxDiff = None
        #self.test_dir = directory_finder().get_test_dir()
        #directory_finder does not support HMF Djerba. Fix this?
        self.test_dir = os.environ.get('HMF_DJERBA_TEST_DIR')

    def testSnvIndel(self):
        data_dir = os.path.join(self.test_dir, 'plugins', 'wgts', 'snv_indel')
        # TODO put INI generation from template into its own method?
        maf_filename = 'BTC-0124-03-LB01-01.sage.somatic.maf.gz'
        maf_path = os.path.join(data_dir, maf_filename)
        test_source_dir = os.path.realpath(os.path.dirname(__file__))
        with open(os.path.join(test_source_dir, self.INI_NAME)) as in_file:
            template_str = in_file.read()
        template = string.Template(template_str)
        ini_str = template.substitute( {'MAF_PATH': maf_path})
        tmp_dir = self.get_tmp_dir()
        input_dir = os.path.join(tmp_dir, 'input')
        os.mkdir(input_dir)
        work_dir = os.path.join(tmp_dir, 'work')
        os.mkdir(work_dir)
        with open(os.path.join(input_dir, self.INI_NAME), 'w') as ini_file:
            ini_file.write(ini_str)
        copy(os.path.join(data_dir, self.JSON_NAME), input_dir)
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
