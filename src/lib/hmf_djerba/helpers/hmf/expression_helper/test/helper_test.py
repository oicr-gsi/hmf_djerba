#! /usr/bin/env python3

"""
Test of the HMF expression helper
"""

import logging
import os
import unittest
from configparser import ConfigParser
from shutil import copy
from djerba.core.loaders import helper_loader
from djerba.core.workspace import workspace
from hmf_djerba.plugins.plugin_tester_hmf import PluginTesterHMF
from hmf_djerba.util.environment import hmf_directory_finder


class TestExpressionHelper(PluginTesterHMF):

    INI_NAME = 'expression_helper.ini'
    INI_NAME_MINIMAL = 'expression_helper_minimal.ini'
    INI_NAME_EXPECTED = 'expression_helper_expected.ini'
    HELPER_NAME = 'hmf.expression_helper'
    PYTHON_VERSION = 'python3.10'

    # Note: The test data on Bitbucket contains an empty JSON file with this name,
    # for compatibility with PluginTesterHMF
    JSON_NAME = 'expression_helper.json'
    
    def setUp(self):
        super().setUp()
        self.data_dir = os.path.join(self.test_dir, 'helpers', 'expression_helper')

    def testConfigure(self):
        tmp_dir = self.get_tmp_dir() # inherited from TestBase
        work_dir = os.path.join(tmp_dir, self.WORK_NAME)
        os.mkdir(work_dir)
        sample_info_path = os.path.join(self.data_dir, 'sample_info.json')
        copy(sample_info_path, work_dir)
        # helper expects this file to be present, even though we configure input manually
        provenance_subset_path = os.path.join(self.data_dir, 'provenance_subset.tsv.gz')
        copy(provenance_subset_path, work_dir)
        ws = workspace(work_dir)
        loader = helper_loader(logging.ERROR)
        cp = ConfigParser()
        cp.read(os.path.join(self.data_dir, self.INI_NAME_MINIMAL))
        # load the helper and run its 'configure' method
        configured = loader.load(self.HELPER_NAME, ws).configure(cp)
        expected = ConfigParser()
        expected.read(os.path.join(self.data_dir, self.INI_NAME_EXPECTED))
        self.assertEqual(configured, expected)

    def testExtract(self):
        # construct the input paths
        hmf_djerba_root = hmf_directory_finder().get_hmf_root_dir()
        enscon_path = os.path.join(hmf_djerba_root, 'lib', self.PYTHON_VERSION,
                                   'site-packages', 'hmf_djerba', 'helpers', 'hmf',
                                   'expression_helper', 'ensemble_conversion_hg38.txt')
        rsem_path = os.path.join(self.data_dir, 'BTC-0124-03-LB03-01.isf.gene_data.csv')
        mapping = {
            'ENSCON_PATH': enscon_path,
            'RSEM_PATH': rsem_path
        }
        input_dir, work_dir = self.writeTestFiles(self.data_dir, mapping)
        ws = workspace(work_dir)
        loader = helper_loader(logging.ERROR)
        cp = ConfigParser()
        cp.read(os.path.join(input_dir, self.INI_NAME))
        # load the helper and run its 'extract' method
        loader.load(self.HELPER_NAME, ws).extract(cp)
        expected = {
            'data_expression_percentile_comparison.txt': '761f14e0b4b96fc386fa17d67e1fbc03',
            'data_expression_percentile_tcga.json': 'f97131c11d95c9d29d7c327a2d0eb06d',
            'data_expression_percentile_tcga.txt': 'fa292b6606be6221e1bcc3b4aa8808a1',
            'data_expression_zscores_comparison.txt': 'a10d5fe3de528ef21934690d33173354',
            'data_expression_zscores_tcga.txt': 'dbd23c232dbb59c0cd24c95f4a7b1c73'
        }
        for name in expected:
            out_path = os.path.join(work_dir, name)
            self.assertTrue(os.path.exists(out_path))
            self.assertEqual(self.getMD5(out_path), expected[name])

if __name__ == '__main__':
    unittest.main()
