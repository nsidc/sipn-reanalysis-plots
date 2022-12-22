"""Generate plots for display.

NOTE: The matplotlib docs specifically recommend against using pyplot! Can cause memory
leaks:
    https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html
"""
import datetime as dt
import functools

import xarray as xra
from matplotlib.figure import Figure

from sipn_reanalysis_plots._types import YearMonth
from sipn_reanalysis_plots.constants.crs import CRS
from sipn_reanalysis_plots.util.data import (
    read_cfsr_daily_file,
    read_cfsr_daily_files,
    read_cfsr_monthly_file,
    read_cfsr_monthly_files,
)


# TODO: Accept a form object?
def plot_cfsr_daily(
    date: dt.date,
    *,
    end_date: dt.date | None = None,
    # TODO: Better types
    variable: str,
    level: str,
    as_filled_contour: bool = False,
) -> Figure:
    if not end_date:
        opener = functools.partial(read_cfsr_daily_file, date)
    else:
        opener = functools.partial(
            read_cfsr_daily_files,
            start_date=date,
            end_date=end_date,
        )

    with opener() as dataset:
        data_array = _reduce_dataset(
            dataset,
            variable=variable,
            level=int(level),
        )

    plot_title = _plot_title(
        var_longname=data_array.attrs['long_name'],
        var_units=data_array.attrs['units'],
        date_str=_daily_date_str(date, end_date),
    )

    fig = _plot_data_array(
        data_array,
        title=plot_title,
        as_filled_contour=as_filled_contour,
    )

    return fig


def plot_cfsr_monthly(
    month: YearMonth,
    *,
    end_month: YearMonth | None = None,
    # TODO: Better types
    variable: str,
    level: str,
    as_filled_contour: bool = False,
) -> Figure:
    if not end_month:
        opener = functools.partial(read_cfsr_monthly_file, month)
    else:
        opener = functools.partial(
            read_cfsr_monthly_files,
            start_month=month,
            end_month=end_month,
        )

    with opener() as dataset:
        data_array = _reduce_dataset(
            dataset,
            variable=variable,
            level=int(level),
        )

    plot_title = _plot_title(
        var_longname=data_array.attrs['long_name'],
        var_units=data_array.attrs['units'],
        date_str=_monthly_date_str(month, end_month),
    )
    fig = _plot_data_array(
        data_array,
        title=plot_title,
        as_filled_contour=as_filled_contour,
    )

    return fig


def _plot_data_array(
    data_array: xra.DataArray,
    *,
    title: str,
    as_filled_contour: bool = False,
) -> Figure:
    """Extract and plot the "surface temperature" data in `dataset`."""
    fig = Figure(figsize=(6, 6))
    fig.set_tight_layout(True)
    ax = fig.subplots(subplot_kw={'projection': CRS})

    plot_opts = {
        'ax': ax,
        'add_colorbar': False,
    }
    if as_filled_contour:
        plot = data_array.plot.contourf(
            levels=20,
            extend='both',
            **plot_opts,
        )
    else:
        plot = data_array.plot(**plot_opts)

    plot.axes.set_title(title)

    # Add decorations over top of imagery
    # TODO: The coastlines are filled with a semitransparent white color. How to make
    # fully transparent?
    ax.coastlines(
        resolution='110m',
        color='gray',
        linewidth=1,
    )
    ax.gridlines(color='white', alpha=0.5)

    fig.colorbar(plot, extend='both')

    return fig


def _monthly_date_str(
    month: YearMonth,
    end_month: YearMonth | None = None,
) -> str:
    if end_month:
        date_str = f'{month.year}-{month.month} to {end_month.year}-{end_month.month}'
    else:
        date_str = f'{month}'
    return date_str


def _daily_date_str(
    date: dt.date,
    end_date: dt.date | None = None,
) -> str:
    if end_date:
        date_str = f'{date:%Y-%m-%d} to {end_date:%Y-%m-%d}'
    else:
        date_str = f'{date:%Y-%m-%d}'
    return date_str


def _plot_title(
    *,
    var_longname: str,
    var_units: str,
    date_str: str,
) -> str:
    """Calculate standard plot title from variable name, units, and date (range)."""
    title = f'{var_longname} ({var_units})\n{date_str}'
    return title


def _reduce_dataset(
    dataset: xra.Dataset,
    *,
    variable: str,
    level: int,
) -> xra.DataArray:
    """Reduce the dataset to a single grid."""
    data_array = dataset[variable]

    # Average over time dimension if it exists
    if 't' in data_array.dims:
        data_array = data_array.mean(dim='t', keep_attrs=True)

    # TODO: Can we get level by name?
    data_array = data_array[level]

    return data_array
