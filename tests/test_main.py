# tests/test_main.py

import unittest
from unittest.mock import patch, MagicMock
from BB_auto_framework.main import run_stage

class TestMain(unittest.TestCase):

    @patch('BB_auto_framework.main.setup_logger')
    @patch('BB_auto_framework.main.load_plugins')
    def test_run_stage_executes_plugins(self, mock_load_plugins, mock_setup_logger):
        mock_logger = MagicMock()
        mock_setup_logger.return_value = mock_logger

        mock_plugin = MagicMock()
        mock_plugin.__name__ = 'MockPlugin'
        mock_load_plugins.return_value = [mock_plugin]

        run_stage("recon", "example.com")

        mock_setup_logger.assert_called_once()
        mock_logger.info.assert_any_call("Starting stage: recon for example.com")
        mock_logger.info.assert_any_call("Running plugin: MockPlugin")
        mock_plugin.run.assert_called_once_with("example.com")

if __name__ == '__main__':
    unittest.main()
