import datetime as dt
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

import rioxarray  # noqa: F401; Activate xarray extension
import xarray as xra

# from sipn_reanalysis_plots.constants.crs import CRS_EPSG_STR
from sipn_reanalysis_plots.constants.paths import DATA_DAILY_DIR
from sipn_reanalysis_plots.util.date import date_range


@contextmanager
def read_cfsr_daily_file(date: dt.date) -> Generator[xra.Dataset, None, None]:
    fp = _cfsr_daily_fp(date)

    dataset = xra.open_dataset(fp, engine='netcdf4')
    _fix_dataset_crs(dataset)

    # TODO: Eliminate reprojecting on-the-fly
    # dataset.rio.reproject(CRS_EPSG_STR)

    yield dataset
    dataset.close()


@contextmanager
def read_cfsr_daily_files(
    *,
    start_date: dt.date,
    end_date: dt.date,
) -> Generator[xra.Dataset, None, None]:
    dates = date_range(start_date, end_date)
    file_paths = sorted(_cfsr_daily_fp(d) for d in dates)

    # Tested `h5netcdf` engine and it was 1/2 as fast as `netcdf4`
    dataset = xra.open_mfdataset(
        file_paths,
        engine='netcdf4',
        chunks={
            't': 100,
        },
        concat_dim='t',
        combine='nested',
        parallel=True,
    )
    _fix_dataset_crs(dataset, ndims=4)

    yield dataset
    dataset.close()


@contextmanager
def read_cfsr_monthly_file(
    year: int,
    month: int,
) -> Generator[xra.Dataset, None, None]:
    raise NotImplementedError()


def _cfsr_daily_fp(date: dt.date) -> Path:
    fp = DATA_DAILY_DIR / f'cfsr.{date:%Y%m%d}.nc'
    return fp


def _fix_dataset_crs(dataset: xra.Dataset, *, ndims: int = 3) -> None:
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
    _rearrange_data_vars_dimensions(dataset, ndims=ndims)


def _rearrange_data_vars_dimensions(dataset: xra.Dataset, *, ndims: int = 3) -> None:
    """Modify `dataset` *in place* to correctly set dimensions of each data_var.

    Order is expected to be (levelN, lat_0, lon_0), but it is (lat_0, lon_0, levelN).
    Error message:

        rioxarray.exceptions.InvalidDimensionOrder: Invalid dimension order. Expected
        order: ('level4', 'lat_0', 'lon_0') ... Data variable: U
    """
    for data_var in dataset.data_vars:
        arr = dataset[data_var]

        # Only transpose DataArrays containing lat, lon, and levels (or, if ndims is 4,
        # include t dimension)
        if len(arr.dims) != ndims:
            continue

        new_dims = (arr.dims[-1], *arr.dims[0:-1])
        dataset[data_var] = arr.transpose(*new_dims)
