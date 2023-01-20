import datetime as dt

import xarray as xra

from sipn_reanalysis_plots._types import YearMonth
from sipn_reanalysis_plots.util.data.read import (
    read_cfsr_daily_climatology_file,
    read_cfsr_monthly_climatology_file,
)
from sipn_reanalysis_plots.util.data.reduce import reduce_dataset
from sipn_reanalysis_plots.util.date import date_range, month_range


# TODO: DRY daily/monthly logic
def diff_from_daily_climatology(
    data_array: xra.DataArray,
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
        days = {f'{start_date:%m-%d}'}
    else:
        days = set(f'{date:%m-%d}' for date in date_range(start_date, end_date))

    with read_cfsr_daily_climatology_file() as climatology_dataset:
        climatology_dataset = climatology_dataset.sel(date=list(days))
        climatology_data_array = reduce_dataset(
            climatology_dataset,
            variable=variable,
            level=level,
        )
        climatology_data_array = climatology_data_array.mean(dim='date')

    with xra.set_options(keep_attrs=True):
        diff = data_array - climatology_data_array
    return diff


def diff_from_monthly_climatology(
    data_array: xra.DataArray,
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
    if end_month is None:
        months = {start_month.month}
    else:
        months = set(
            year_month.month for year_month in month_range(start_month, end_month)
        )

    with read_cfsr_monthly_climatology_file() as climatology_dataset:
        climatology_dataset = climatology_dataset.sel(month=list(months))
        climatology_data_array = reduce_dataset(
            climatology_dataset,
            variable=variable,
            level=level,
        )
        climatology_data_array = climatology_data_array.mean(dim='month')

    with xra.set_options(keep_attrs=True):
        diff = data_array - climatology_data_array
    return diff
