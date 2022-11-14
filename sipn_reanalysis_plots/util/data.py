import datetime as dt
from contextlib import contextmanager
from typing import Generator

import rioxarray  # noqa: F401; Activate xarray extension
import xarray as xra

from sipn_reanalysis_plots.constants.crs import CRS_EPSG_STR
from sipn_reanalysis_plots.constants.paths import DATA_DAILY_DIR


def _rearrange_data_vars_dimensions(dataset: xra.Dataset) -> None:
    """Modify `dataset` *in place* to correctly set dimensions of each data_var.

    Order is expected to be (levelN, lat_0, lon_0), but it is (lat_0, lon_0, levelN).
    Error:

        rioxarray.exceptions.InvalidDimensionOrder: Invalid dimension order. Expected
        order: ('level4', 'lat_0', 'lon_0') ... Data variable: U
    """
    for data_var in dataset.data_vars:
        arr = dataset[data_var]

        # Only transpose DataArrays containing lat, lon, and levels
        if len(arr.dims) != 3:
            continue

        new_dims = (arr.dims[2], arr.dims[0], arr.dims[1])
        dataset[data_var] = arr.transpose(*new_dims)


@contextmanager
def read_cfsr_daily_file(date: dt.date) -> Generator[xra.Dataset, None, None]:
    yyyymmdd = date.strftime('%Y%m%d')
    fn = f'cfsr.{yyyymmdd}.nc'
    fp = DATA_DAILY_DIR / fn

    dataset = xra.open_dataset(fp)

    # Set CRS, spatial dimensions, and dimension order of source data to make xarray
    # happy.
    # TODO: Can we embed this in the netcdf?
    dataset.rio.write_crs(
        4326,
        inplace=True,
    )
    dataset.rio.set_spatial_dims(
        x_dim='lon_0',
        y_dim='lat_0',
        inplace=True,
    )
    dataset.rio.write_coordinate_system(inplace=True)
    _rearrange_data_vars_dimensions(dataset)

    # TODO: Avoid reprojecting on-the-fly
    # dataset.rio.reproject(CRS_EPSG_STR)

    yield dataset
    dataset.close()


@contextmanager
def read_cfsr_monthly_file(
    year: int,
    month: int,
) -> Generator[xra.Dataset, None, None]:
    raise NotImplementedError()
