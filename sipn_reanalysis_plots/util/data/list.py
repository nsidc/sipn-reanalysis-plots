import datetime as dt
import re
from pathlib import Path

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
    dates = [
        dt.datetime.strptime(
            re.search(DATA_DAILY_DATE_REGEX, p.name).group(1),
            DATA_DAILY_DATE_FORMAT,
        ).date()
        for p in paths
    ]
    return dates


def list_monthly_data_paths() -> list[Path]:
    """List sorted paths of existing monthly files."""
    paths = DATA_MONTHLY_DIR.glob('*')
    return sorted(paths)


def list_monthly_data_yearmonths() -> list[YearMonth]:
    paths = list_monthly_data_paths()
    dates = [_yearmonth_from_monthly_path(p) for p in paths]
    return dates


def _yearmonth_from_monthly_path(path: Path) -> YearMonth:
    match = re.search(DATA_MONTHLY_YEARMONTH_REGEX, path.name)
    return YearMonth(year=match.group(1), month=match.group(2))
