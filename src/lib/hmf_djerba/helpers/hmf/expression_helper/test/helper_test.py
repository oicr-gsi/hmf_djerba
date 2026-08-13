#! /usr/bin/env python3

"""
Test of the HMF expression helper
"""

import logging
import os
import unittest
from configparser import ConfigParser
from djerba.core.loaders import helper_loader
from djerba.core.workspace import workspace
from hmf_djerba.plugins.plugin_tester_hmf import PluginTesterHMF


class TestExpressionHelper(PluginTesterHMF):

    INI_NAME = 'expression_helper.ini'
    JSON_NAME = 'expression_helper.json'
    HELPER_NAME = 'hmf.expression_helper'
    PYTHON_VERSION = 'python3.10'
    
    def setUp(self):
        super().setUp()
        self.data_dir = os.path.join(self.test_dir, 'helpers', 'expression_helper')        

    def testExtract(self):
        # construct the input paths
        hmf_djerba_root = os.environ.get('HMF_DJERBA_ROOT')
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
