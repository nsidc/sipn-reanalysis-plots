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

        fig = _plot_data_array(
            data_array,
            date=date,
            end_date=end_date,
            as_filled_contour=as_filled_contour,
        )

    return fig


def _plot_data_array(
    data_array: xra.DataArray,
    *,
    date: dt.date,
    end_date: dt.date | None = None,
    as_filled_contour: bool = False,
) -> Figure:
    """Extract and plot the "surface temperature" data in `dataset`.

    Display variable name, units, and `date` in the title.
    """
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

    plot.axes.set_title(
        _plot_title(
            data_array=data_array,
            date=date,
            end_date=end_date,
        )
    )

    # Add decorations over top of imagery
    ax.coastlines(resolution='110m', color='gray', linewidth=1)
    ax.gridlines(color='white', alpha=0.5)

    fig.colorbar(plot, extend='both')

    return fig


def _plot_title(
    *,
    data_array: xra.DataArray,
    date: dt.date,
    end_date: dt.date | None = None,
) -> str:
    long_name = data_array.attrs['long_name']
    units = data_array.attrs['units']
    if end_date:
        date_str = f'{date:%Y-%m-%d} to {end_date:%Y-%m-%d}'
    else:
        date_str = f'{date:%Y-%m-%d}'

    title = f'{long_name} ({units})\n{date_str}'
    return title
