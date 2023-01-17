import datetime as dt
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

import rioxarray  # noqa: F401; Activate xarray extension
import xarray as xra

from sipn_reanalysis_plots._types import YearMonth
from sipn_reanalysis_plots.constants.paths import (
    DATA_CLIMATOLOGY_DAILY_FILE,
    DATA_CLIMATOLOGY_MONTHLY_FILE,
    DATA_DAILY_DIR,
    DATA_DAILY_TEMPLATE,
    DATA_MONTHLY_DIR,
    DATA_MONTHLY_TEMPLATE,
)
from sipn_reanalysis_plots.util.date import date_range, month_range


@contextmanager
def read_cfsr_daily_file(date: dt.date) -> Generator[xra.Dataset, None, None]:
    fp = _cfsr_daily_fp(date)

    dataset = _dataset_from_nc(fp)
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
    dataset = _dataset_from_multi_nc(file_paths)
    yield dataset
    dataset.close()


@contextmanager
def read_cfsr_monthly_file(month: YearMonth) -> Generator[xra.Dataset, None, None]:
    fp = _cfsr_monthly_fp(month)

    dataset = _dataset_from_nc(fp)
    yield dataset
    dataset.close()


@contextmanager
def read_cfsr_monthly_files(
    start_month: YearMonth,
    end_month: YearMonth,
) -> Generator[xra.Dataset, None, None]:
    months = month_range(start_month, end_month)
    file_paths = sorted(_cfsr_monthly_fp(d) for d in months)

    dataset = _dataset_from_multi_nc(file_paths)
    yield dataset
    dataset.close()


@contextmanager
def read_cfsr_daily_climatology_file() -> Generator[xra.Dataset, None, None]:
    dataset = _dataset_from_nc(
        DATA_CLIMATOLOGY_DAILY_FILE,
        chunks={'date': 10},
    )
    yield dataset
    dataset.close()


@contextmanager
def read_cfsr_monthly_climatology_file() -> Generator[xra.Dataset, None, None]:
    dataset = _dataset_from_nc(
        DATA_CLIMATOLOGY_MONTHLY_FILE,
        chunks={'month': 4},
    )
    yield dataset
    dataset.close()


def _dataset_from_nc(
    fp: Path,
    *,
    chunks: dict | None = None,
) -> xra.Dataset:
    # Tested `h5netcdf` engine and it was 1/2 as fast as `netcdf4`
    dataset = xra.open_dataset(fp, engine='netcdf4', chunks=chunks)
    return dataset


def _dataset_from_multi_nc(fps: list[Path]) -> xra.Dataset:
    # Tested `h5netcdf` engine and it was 1/2 as fast as `netcdf4`
    dataset = xra.open_mfdataset(
        fps,
        engine='netcdf4',
        chunks={
            't': 100,
        },
        concat_dim='t',
        combine='nested',
        parallel=True,
    )
    return dataset


def _cfsr_daily_fp(date: dt.date) -> Path:
    fp = DATA_DAILY_DIR / DATA_DAILY_TEMPLATE.format(date=date)
    return fp


def _cfsr_monthly_fp(month: YearMonth) -> Path:
    fp = DATA_MONTHLY_DIR / DATA_MONTHLY_TEMPLATE.format(month=month)
    return fp
