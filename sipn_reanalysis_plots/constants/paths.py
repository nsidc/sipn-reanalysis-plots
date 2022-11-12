from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = PACKAGE_DIR.parent

DATA_DIR = Path('/data')
DATA_DAILY_DIR = DATA_DIR / 'daily'
DATA_MONTHLY_DIR = DATA_DIR / 'monthly'
