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
