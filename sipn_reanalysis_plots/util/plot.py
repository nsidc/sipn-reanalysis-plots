"""Generate plots for display.

NOTE: The matplotlib docs specifically recommend against using pyplot! Can cause memory
leaks:
    https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html
"""
from cartopy import crs
from matplotlib.figure import Figure
from netCDF4 import Dataset

from sipn_reanalysis_plots.constants.crs import CRS


def plot_temperature_variable(dataset: Dataset) -> Figure:
    fig = Figure(figsize=(9, 9))
    fig.set_tight_layout(True)
    ax = fig.subplots(subplot_kw={'projection': CRS})
    ax.coastlines(resolution='110m', linewidth=0.5)
    ax.gridlines()

    ax.set_extent([-180, 180, 60, 60], crs=crs.PlateCarree())

    return fig
