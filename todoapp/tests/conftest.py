import sys
from pathlib import Path

PROJECT_APP_DIR = Path(__file__).resolve().parents[1]

if str(PROJECT_APP_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_APP_DIR))
