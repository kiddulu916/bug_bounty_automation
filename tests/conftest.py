import os
import sys

# Get the current file's directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
BB_AUTO_FRAMEWORK_DIR = os.path.join(ROOT_DIR, 'BB_auto_framework')

# Add both the root directory and BB_auto_framework directory to Python path
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, BB_AUTO_FRAMEWORK_DIR)

# Now we can import from the main project directory and BB_auto_framework