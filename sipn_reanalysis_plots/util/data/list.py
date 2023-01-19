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
from sipn_reanalysis_plots.errors import NoDataFoundError


def list_daily_data_paths() -> list[Path]:
    """List sorted paths of existing daily files.

    NOTE: With ~16k files, this listing takes two-tenths of a second on 2023 NSIDC
    networked storage infrastructure.
    """
    paths = list(DATA_DAILY_DIR.glob('*'))
    if len(paths) == 0:
        raise NoDataFoundError('No daily data found. Please run ingest!')

    return sorted(paths)


def list_daily_data_dates() -> list[dt.date]:
    paths = list_daily_data_paths()
    dates = [date for p in paths if (date := _date_from_daily_path(p)) is not None]
    return dates


def min_daily_data_date() -> dt.date:
    return list_daily_data_dates()[0]


def min_daily_data_date_str() -> str:
    min_date = min_daily_data_date()
    return f'{min_date:%Y-%m-%d}'


def max_daily_data_date() -> dt.date:
    return list_daily_data_dates()[-1]


def max_daily_data_date_str() -> str:
    max_date = max_daily_data_date()
    return f'{max_date:%Y-%m-%d}'


def list_monthly_data_paths() -> list[Path]:
    """List sorted paths of existing monthly files."""
    paths = list(DATA_MONTHLY_DIR.glob('*'))

    if len(paths) == 0:
        raise NoDataFoundError('No monthly data found. Please run ingest!')

    return sorted(paths)


def list_monthly_data_yearmonths() -> list[YearMonth]:
    paths = list_monthly_data_paths()
    dates = [
        yearmonth
        for p in paths
        if (yearmonth := _yearmonth_from_monthly_path(p)) is not None
    ]
    return dates


def min_monthly_data_yearmonth() -> YearMonth:
    min_yearmonth = list_monthly_data_yearmonths()[0]
    return min_yearmonth


def min_monthly_data_yearmonth_str() -> str:
    min_yearmonth = min_monthly_data_yearmonth()
    min_yearmonth_str = f'{min_yearmonth.year}-{min_yearmonth.month:02d}'
    return min_yearmonth_str


def max_monthly_data_yearmonth() -> YearMonth:
    max_yearmonth = list_monthly_data_yearmonths()[-1]
    return max_yearmonth


def max_monthly_data_yearmonth_str() -> str:
    max_yearmonth = max_monthly_data_yearmonth()
    max_yearmonth_str = f'{max_yearmonth.year}-{max_yearmonth.month:02d}'
    return max_yearmonth_str


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
