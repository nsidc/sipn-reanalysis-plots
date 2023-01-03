import datetime as dt

import xarray as xra

from sipn_reanalysis_plots._types import YearMonth
from sipn_reanalysis_plots.util.data import (
    read_cfsr_daily_climatology_file,
    read_cfsr_monthly_climatology_file,
    reduce_dataset,
)
from sipn_reanalysis_plots.util.date import date_range, month_range


# TODO: DRY daily/monthly logic
def diff_from_daily_climatology(
    data_array: xra.Dataset,
    *,
    variable: str,
    level: str,
    start_date: dt.date,
    end_date: dt.date | None = None,
) -> xra.DataArray:
    """Calculate difference from climatology for given `data_array`.

    Climatology is read from file and filtered to only include days in `data_array`
    and then averaged over the "day" dimension.
    """
    if not end_date:
        days = set(start_date.day)
    else:
        days = set(date.day for date in date_range(start_date, end_date))

    with read_cfsr_daily_climatology_file() as climatology_dataset:
        climatology_dataset = climatology_dataset.sel(day=list(days))
        climatology_dataset = climatology_dataset.mean(dim='day')
        climatology_data_array = reduce_dataset(
            climatology_dataset,
            variable=variable,
            level=int(level),
        )

    with xra.set_options(keep_attrs=True):
        diff = data_array - climatology_data_array
    return diff


def diff_from_monthly_climatology(
    data_array: xra.Dataset,
    *,
    variable: str,
    level: str,
    start_month: YearMonth,
    end_month: YearMonth | None = None,
) -> xra.DataArray:
    """Calculate difference from climatology for given `data_array`.

    Climatology is read from file and filtered to only include months in `data_array`
    and then averaged over the "month" dimension.
    """
    if not end_month:
        months = set(end_month.month)
    else:
        months = set(
            year_month.month for year_month in month_range(start_month, end_month)
        )

    with read_cfsr_monthly_climatology_file() as climatology_dataset:
        climatology_dataset = climatology_dataset.sel(month=list(months))
        climatology_dataset = climatology_dataset.mean(dim='month')
        climatology_data_array = reduce_dataset(
            climatology_dataset,
            variable=variable,
            level=int(level),
        )

    with xra.set_options(keep_attrs=True):
        diff = data_array - climatology_data_array
    return diff
