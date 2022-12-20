"""Generate plots for display.

NOTE: The matplotlib docs specifically recommend against using pyplot! Can cause memory
leaks:
    https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html
"""
import datetime as dt
import functools

import xarray as xra
from cartopy import crs
from matplotlib.figure import Figure

from sipn_reanalysis_plots.constants.crs import CRS
from sipn_reanalysis_plots.constants.variables import VARIABLES
from sipn_reanalysis_plots.util.data import read_cfsr_daily_file, read_cfsr_daily_files
from sipn_reanalysis_plots._types import YearMonth


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
        # TODO: Can we get level by name?
        # TEMP: Remove this conditional once all vars are made 3d
        if len(VARIABLES[variable]['levels']) == 1:
            data_array = dataset[variable]
        else:
            data_array = dataset[variable][int(level)]

        # Average over time dimension if it exists
        if 't' in data_array.dims:
            data_array = data_array.mean(dim='t', keep_attrs=True)

        plot_title = _plot_title(
            var_longname=data_array.attrs['long_name'],
            var_units=data_array.attrs['units'],
            date=date,
            end_date=end_date,
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
    raise NotImplementedError()


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
        'transform': crs.PlateCarree(),
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
    ax.coastlines(resolution='110m', color='gray', linewidth=1)
    ax.gridlines(color='white', alpha=0.5)

    fig.colorbar(plot, extend='both')

    return fig


def _plot_title(
    *,
    var_longname: str,
    var_units: str,
    date: dt.date,
    end_date: dt.date | None = None,
) -> str:
    """Calculate standard plot title from variable name, units, and date (range)."""
    if end_date:
        date_str = f'{date:%Y-%m-%d} to {end_date:%Y-%m-%d}'
    else:
        date_str = f'{date:%Y-%m-%d}'

    title = f'{var_longname} ({var_units})\n{date_str}'
    return title
