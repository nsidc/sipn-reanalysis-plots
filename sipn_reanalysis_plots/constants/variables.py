from sipn_reanalysis_plots._types import Variable

VARIABLES: dict[str, Variable] = {
    'U': {
        'long_name': 'U-component of wind',
        'levels': ('10m', '925mb', '850mb', '500mb'),
    },
    'V': {
        'long_name': 'V-component of wind',
        'levels': ('10m', '925mb', '850mb', '500mb'),
    },
    'WSPD': {
        'long_name': 'Wind speed',
        'levels': ('10m', '925mb', '850mb', '500mb'),
    },
    'T': {
        'long_name': 'Air temperature',
        'levels': ('2m', '925mb', '850mb', '500mb'),
    },
    'SH': {
        'long_name': 'Specific humidity',
        'levels': ('2m', '925mb', '850mb', '500mb'),
    },
    'RH': {
        'long_name': 'Relative humidity',
        'levels': ('2m', '925mb', '850mb', '500mb'),
    },
    'HGT': {
        'long_name': 'Geopotential height',
        'levels': ('925mb', '850mb', '500mb'),
    },
    'PWAT': {
        'long_name': 'Precipitable water',
        'levels': ('only',),
    },
    'MSLP': {
        'long_name': 'Pressure reduced to sea level',
        'levels': ('only',),
    },
}
