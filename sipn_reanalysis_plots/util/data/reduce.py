import xarray as xra


def reduce_dataset(
    dataset: xra.Dataset,
    *,
    variable: str,
    level: int,
) -> xra.DataArray:
    """Reduce the dataset to a single grid."""
    data_array = dataset[variable]

    # Average over time dimension if it exists
    if 't' in data_array.dims:
        data_array = data_array.mean(dim='t', keep_attrs=True)

    level_dim_names = [d for d in data_array.dims if str(d).startswith('lev')]
    if len(level_dim_names) != 1:
        raise RuntimeError(
            f'Expected 1 "level" dimension in {data_array.dims=}; found {level_dim_names}',
        )

    level_dim_name = level_dim_names[0]
    data_array = data_array.isel({level_dim_name: level})

    return data_array
