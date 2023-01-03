from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = PACKAGE_DIR.parent

DATA_DIR = Path('/data')
DATA_DAILY_DIR = DATA_DIR / 'daily'
DATA_MONTHLY_DIR = DATA_DIR / 'monthly'
DATA_CLIMATOLOGY_DIR = DATA_DIR / 'climatology'
DATA_CLIMATOLOGY_MONTHLY_FILE = (
    DATA_CLIMATOLOGY_DIR / 'cfsr.monthly_1981-2010_climatology.nc'
)
DATA_CLIMATOLOGY_DAILY_FILE = (
    DATA_CLIMATOLOGY_DIR / 'cfsr.daily_1981-2010_climatology.nc'
)
