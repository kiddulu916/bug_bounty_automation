import unittest
from BB_auto_framework.core.logger import setup_logger
import logging

class TestLogger(unittest.TestCase):
    def test_logger_setup(self):
        logger = setup_logger()
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, "bughunt")
