import unittest
from BB_auto_framework.core.plugin_loader import load_plugins

class TestPluginLoader(unittest.TestCase):
    def test_load_dummy_plugin(self):
        plugins = load_plugins("recon")
        self.assertGreater(len(plugins), 0)
        self.assertTrue(callable(getattr(plugins[0], "run", None)))
