"""Generate plots for display.

NOTE: The matplotlib docs specifically recommend against using pyplot! Can cause memory
leaks:
    https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html
"""
import datetime as dt

import numpy as np
import xarray as xra
from cartopy import crs
from matplotlib.figure import Figure

from sipn_reanalysis_plots.constants.crs import CRS
from sipn_reanalysis_plots.util.data import read_cfsr_daily_file


def plot_cfsr_daily(date: dt.date) -> Figure:
    with read_cfsr_daily_file(date) as dataset:
        fig = _plot_temperature_variable(
            dataset=dataset,
            date=date,
        )

    return fig


def _plot_temperature_variable(
    *,
    dataset: xra.Dataset,
    date: dt.date,
) -> Figure:
    """Extract and plot the "surface temperature" data in `dataset`.

    Display variable name, units, and `date` in the title.

    TODO: Accept any DataArray and plot it.
    """

    temp_surface = dataset['T'][0]
    plot = temp_surface.plot(
        subplot_kws={
            'projection': CRS,
            'facecolor': 'gray',
        },
        transform=crs.PlateCarree(),
        # If figsize not set here, behavior can get weird:
        #     https://github.com/pydata/xarray/issues/7288
        figsize=(6, 6),
        add_colorbar=False,
    )

    plot.axes.set_title(_plot_title(data_array=temp_surface, date=date))

    # Add decorations over top of imagery
    plot.axes.coastlines(resolution='110m', color='white', linewidth=0.5)
    plot.axes.gridlines()

    fig = plot.figure
    fig.set_tight_layout(True)

    fig.colorbar(plot, extend='both')

    return fig


def _plot_title(*, data_array: xra.DataArray, date: dt.date) -> str:
    long_name = data_array.attrs['long_name']
    units = data_array.attrs['units']
    date_str = date.strftime('%Y-%m-%d')

    title = f'{long_name} ({units})\n{date_str}'
    return title
