#! /usr/bin/env python3

import unittest
import os
import sys
import logging
import tempfile
import shutil

from djerba.core.loaders import plugin_loader
from djerba.core.workspace import workspace
from djerba.version import get_djerba_version

class TestPluginLoading(unittest.TestCase):

    TEST_LOG_LEVEL = logging.WARNING

    def setUp(self):
        if not os.environ.get('HMF_DJERBA_ROOT'):
            raise RuntimeError('Must load the hmf-djerba environment module')
        self.tmp_dir = tempfile.mkdtemp(prefix='hmf_djerba_')
        
    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_djerba_version(self):
        """Verify we are testing against the expected djerba version"""
        # This version should match what's in requirements.txt
        expected_version = '1.13.0'
        found_version = get_djerba_version()
        self.assertEqual(found_version, expected_version,
                         f"Djerba version mismatch. Expected {expected_version}, found {found_version}")

    def test_load_hmf_fusion_plugin(self):
        """Verify hmf.fusion plugin can be loaded by djerba"""
        loader = plugin_loader(log_level=self.TEST_LOG_LEVEL)
        
        # The workspace needs a directory
        ws = workspace(self.tmp_dir)
        
        # Try to load the plugin
        # djerba loader will look for hmf_djerba.plugins.hmf.fusion
        plugin = loader.load('hmf.fusion', ws)
        self.assertIsNotNone(plugin)
        self.assertEqual(plugin.PLUGIN_VERSION, '1.1.0')

    def test_load_hmf_genomic_landscape_plugin(self):
        """Verify hmf.genomic_landscape plugin can be loaded by djerba"""
        loader = plugin_loader(log_level=self.TEST_LOG_LEVEL)
        ws = workspace(self.tmp_dir)
        plugin = loader.load('hmf.genomic_landscape', ws)
        self.assertIsNotNone(plugin)

    def test_load_hmf_wgts_plugins(self):
        """Verify hmf.wgts sub-plugins can be loaded"""
        loader = plugin_loader(log_level=self.TEST_LOG_LEVEL)
        ws = workspace(self.tmp_dir)
        
        plugins_to_test = [
            'hmf.wgts.cnv_purple',
            'hmf.wgts.snv_indel'
        ]
        
        for p_name in plugins_to_test:
            with self.subTest(plugin=p_name):
                plugin = loader.load(p_name, ws)
                self.assertIsNotNone(plugin)

if __name__ == '__main__':
    unittest.main()
