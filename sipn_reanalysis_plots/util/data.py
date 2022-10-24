from datetime import date

from netCDF4 import Dataset

from sipn_reanalysis_plots.constants.paths import DATA_DIR


def read_cfsr_daily_file(the_date: date) -> Dataset: 
    yyyymmdd = the_date.strftime('%Y%m%d')
    fn = f'cfsr.{yyyymmdd}.nc'
    fp = DATA_DIR / fn

    dataset = Dataset(fp, mode="r", format='NetCDF4')
    return dataset
