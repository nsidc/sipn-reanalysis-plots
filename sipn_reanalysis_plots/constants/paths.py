import re
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = PACKAGE_DIR.parent

DATA_DIR = Path('/data')

DATA_DAILY_DIR = DATA_DIR / 'daily'
DATA_DAILY_DATE_REGEX = re.compile(r'^cfsr\.(\d{8})\.nc$')
DATA_DAILY_DATE_FORMAT = '%Y%m%d'
DATA_DAILY_TEMPLATE = f'cfsr.{{date:{DATA_DAILY_DATE_FORMAT}}}.nc'

DATA_MONTHLY_DIR = DATA_DIR / 'monthly'
DATA_MONTHLY_YEARMONTH_REGEX = re.compile(r'^cfsr\.(\d{4})(\d{2})\.nc$')
DATA_MONTHLY_TEMPLATE = 'cfsr.{month}.nc'

DATA_CLIMATOLOGY_DIR = DATA_DIR / 'climatology'
DATA_CLIMATOLOGY_MONTHLY_FILE = (
    DATA_CLIMATOLOGY_DIR / 'cfsr.monthly_1981-2010_climatology.nc'
)
DATA_CLIMATOLOGY_DAILY_FILE = (
    DATA_CLIMATOLOGY_DIR / 'cfsr.daily_1981-2010_climatology.nc'
)
