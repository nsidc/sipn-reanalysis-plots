import datetime as dt
import re
from pathlib import Path

from sipn_reanalysis_plots import app
from sipn_reanalysis_plots._types import YearMonth
from sipn_reanalysis_plots.constants.paths import (
    DATA_DAILY_DATE_FORMAT,
    DATA_DAILY_DATE_REGEX,
    DATA_DAILY_DIR,
    DATA_MONTHLY_DIR,
    DATA_MONTHLY_YEARMONTH_REGEX,
)


def list_daily_data_paths() -> list[Path]:
    """List sorted paths of existing daily files.

    NOTE: With ~16k files, this listing takes two-tenths of a second on 2023 NSIDC
    networked storage infrastructure.
    """
    paths = DATA_DAILY_DIR.glob('*')
    return sorted(paths)


def list_daily_data_dates() -> list[dt.date]:
    paths = list_daily_data_paths()
    dates = [date for p in paths if (date := _date_from_daily_path(p)) is not None]
    return dates


def list_monthly_data_paths() -> list[Path]:
    """List sorted paths of existing monthly files."""
    paths = DATA_MONTHLY_DIR.glob('*')
    return sorted(paths)


def list_monthly_data_yearmonths() -> list[YearMonth]:
    paths = list_monthly_data_paths()
    dates = [
        yearmonth
        for p in paths
        if (yearmonth := _yearmonth_from_monthly_path(p)) is not None
    ]
    return dates


def _date_from_daily_path(path: Path) -> dt.date | None:
    match = re.search(DATA_DAILY_DATE_REGEX, path.name)
    if not match:
        app.logger.warning(f'A file with invalid format was found: {path}')
        return None

    date = dt.datetime.strptime(match.group(1), DATA_DAILY_DATE_FORMAT).date()
    return date


def _yearmonth_from_monthly_path(path: Path) -> YearMonth | None:
    match = re.search(DATA_MONTHLY_YEARMONTH_REGEX, path.name)
    if not match:
        app.logger.warning(f'A file with invalid format was found: {path}')
        return None

    yearmonth = YearMonth(year=int(match.group(1)), month=int(match.group(2)))
    return yearmonth
