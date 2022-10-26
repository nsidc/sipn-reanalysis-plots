from contextlib import contextmanager
from datetime import date
from typing import Generator

import rasterio
from rasterio.io import DatasetReader

from sipn_reanalysis_plots.constants.paths import DATA_DIR


@contextmanager
def read_cfsr_daily_file(the_date: date) -> Generator[DatasetReader, None, None]:
    yyyymmdd = the_date.strftime('%Y%m%d')
    fn = f'cfsr.{yyyymmdd}.reproj2.nc'
    fp = DATA_DIR / fn

    dataset = rasterio.open(f'NETCDF:{fp}:Band1', mode='r', driver='netCDF')
    yield dataset

    dataset.close()


@contextmanager
def read_cfsr_monthly_file(
    year: int,
    month: int,
) -> Generator[DatasetReader, None, None]:
    raise NotImplementedError()
