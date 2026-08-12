"""Base class for HMF-Djerba plugin tests"""

import os
import string
from shutil import copy
from djerba.plugins.plugin_tester import PluginTester

class PluginTesterHMF(PluginTester):

    INPUT_NAME = 'input'
    WORK_NAME = 'work'
    
    # placeholders, can override these in subclasses
    INI_NAME = 'hmf_test.ini'
    JSON_NAME = 'hmf_test.json'

    def setUp(self):
        super().setUp()
        self.test_dir = os.environ.get('HMF_DJERBA_TEST_DIR')

    def writeTestFiles(self, data_dir, mapping):
        # write INI and JSON files to the working test directory
        with open(os.path.join(data_dir, self.INI_NAME)) as in_file:
            template_str = in_file.read()
        template = string.Template(template_str)
        ini_str = template.substitute(mapping)
        tmp_dir = self.get_tmp_dir() # inherited from TestBase
        input_dir = os.path.join(tmp_dir, self.INPUT_NAME)
        os.mkdir(input_dir)
        work_dir = os.path.join(tmp_dir, self.WORK_NAME)
        os.mkdir(work_dir)
        with open(os.path.join(input_dir, self.INI_NAME), 'w') as ini_file:
            ini_file.write(ini_str)
        copy(os.path.join(data_dir, self.JSON_NAME), input_dir)
        return input_dir, work_dir
