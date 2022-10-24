"""Generate plots for display.

NOTE: The matplotlib docs specifically recommend against using pyplot! Can cause memory
leaks:
    https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html
"""
import cartopy
from matplotlib.figure import Figure
from netCDF4 import Dataset

from sipn_reanalysis_plots.constants.crs import CRS


def plot_temperature_variable(dataset: Dataset) -> Figure:
    fig = Figure()
    ax = fig.subplots(subplot_kw={'projection': CRS})
    ax.coastlines()
    # ax.plot([1, 2])

    return fig
