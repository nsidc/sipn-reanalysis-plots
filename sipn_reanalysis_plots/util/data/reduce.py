import xarray as xra


def reduce_dataset(
    dataset: xra.Dataset,
    *,
    variable: str,
    level: str,
) -> xra.DataArray:
    """Reduce the dataset to a single grid."""
    # Select variable
    data_array = dataset[variable]

    # Select level
    level_dim_names = [d for d in data_array.dims if str(d).startswith('lev')]
    if len(level_dim_names) != 1:
        raise RuntimeError(
            f'Expected 1 "level" dimension in {data_array.dims=};'
            f' found {level_dim_names}'
        )

    level_dim_name = level_dim_names[0]
    data_array = data_array.sel({level_dim_name: level})
    data_array.attrs['analysis_level'] = level

    # Average over time dimension if it exists
    if 't' in data_array.dims:
        data_array = data_array.mean(dim='t', keep_attrs=True)

    return data_array
