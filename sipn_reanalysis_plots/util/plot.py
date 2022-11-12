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
    fig = Figure(figsize=(6, 6))
    fig.set_tight_layout(True)

    # ax = fig.subplots(subplot_kw={'projection': CRS})
    ax = fig.subplots(subplot_kw={'projection': crs.PlateCarree()})

    temp_surface = dataset['T'][0]

    title = _plot_title(data_array=temp_surface, date=date)
    ax.set_title(title)

    ax.set_extent([-180, 180, 60, 90], crs=crs.PlateCarree())

    # Populate nodata values as nans. TODO: Is there a helper method for this?
    breakpoint()
    temp_surface[temp_surface == dataset.nodata] = np.nan

    left, bottom, right, top = dataset.bounds
    extent = [left, right, bottom, top]
    plot = ax.imshow(
        temp_surface,
        vmin=np.nanmin(temp_surface),
        vmax=np.nanmax(temp_surface),
        extent=extent,
    )
    fig.colorbar(plot, extend='both')

    # Add coastlines over top of imagery
    ax.coastlines(resolution='110m', color='white', linewidth=0.5)
    ax.gridlines()

    return fig


def _plot_title(*, data_array: xra.DataArray, date: dt.date) -> str:
    long_name = data_array.attrs['long_name']
    units = data_array.attrs['units']
    date_str = date.strftime('%Y-%m-%d')

    title = f'{long_name} ({units})\n{date_str}'
    return title
