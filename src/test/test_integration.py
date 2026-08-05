#! /usr/bin/env python3

import unittest
import os
import sys
import logging
import tempfile
import shutil

HMF_DJERBA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
HMF_DJERBA_LIB = os.path.join(HMF_DJERBA_ROOT, 'src', 'lib')
if HMF_DJERBA_LIB not in sys.path:
    sys.path.insert(0, HMF_DJERBA_LIB)


# Use djerba from the environment

try:
    from djerba.core.loaders import plugin_loader
    from djerba.core.workspace import workspace
    import djerba.version
    DJERBA_AVAILABLE = True
except ImportError:
    DJERBA_AVAILABLE = False

class TestHmfIntegration(unittest.TestCase):
    def setUp(self):
        if not DJERBA_AVAILABLE:
            self.skipTest("Djerba not found on PYTHONPATH")
        self.tmp_dir = tempfile.mkdtemp()
        self.original_djerba_packages = os.environ.get('DJERBA_PACKAGES')
        
    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
        if self.original_djerba_packages is not None:
            os.environ['DJERBA_PACKAGES'] = self.original_djerba_packages
        else:
            if 'DJERBA_PACKAGES' in os.environ:
                del os.environ['DJERBA_PACKAGES']

    def test_djerba_version(self):
        """Verify we are testing against the expected djerba version"""
        # This version should match what's in requirements.txt
        expected_version = '1.11.11'
        self.assertEqual(djerba.version.__version__, expected_version, 
                         f"Djerba version mismatch. Expected {expected_version}, found {djerba.version.__version__}")

    def test_load_hmf_fusion_plugin(self):
        """Verify hmf.fusion plugin can be loaded by djerba"""
        os.environ['DJERBA_PACKAGES'] = 'hmf_djerba:djerba'
        loader = plugin_loader(log_level=logging.DEBUG)
        
        # The workspace needs a directory
        ws = workspace(self.tmp_dir)
        
        # Try to load the plugin
        # djerba loader will look for hmf_djerba.plugins.hmf.fusion
        plugin = loader.load('hmf.fusion', ws)
        self.assertIsNotNone(plugin)
        self.assertEqual(plugin.PLUGIN_VERSION, '1.1.0')

    def test_load_hmf_genomic_landscape_plugin(self):
        """Verify hmf.genomic_landscape plugin can be loaded by djerba"""
        os.environ['DJERBA_PACKAGES'] = 'hmf_djerba:djerba'
        loader = plugin_loader(log_level=logging.DEBUG)
        ws = workspace(self.tmp_dir)
        plugin = loader.load('hmf.genomic_landscape', ws)
        self.assertIsNotNone(plugin)

    def test_load_hmf_wgts_plugins(self):
        """Verify hmf.wgts sub-plugins can be loaded"""
        os.environ['DJERBA_PACKAGES'] = 'hmf_djerba:djerba'
        loader = plugin_loader(log_level=logging.DEBUG)
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
