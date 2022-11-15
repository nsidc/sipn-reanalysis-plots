from sipn_reanalysis_plots._types import Variable

VARIABLES = {
    'U': {
        'longname': 'U-component of wind',
        'levels': ('10m', '925mb', '850mb', '500mb'),
    },
    'V': {
        'longname': 'V-component of wind',
        'levels': ('10m', '925mb', '850mb', '500mb'),
    },
    'WSPD': {
        'longname': 'Wind speed',
        'levels': ('10m', '925mb', '850mb', '500mb'),
    },
    'T': {
        'longname': 'Air temperature',
        'levels': ('2m', '925mb', '850mb', '500mb'),
    },
    'SH': {
        'longname': 'Specific humidity',
        'levels': ('2m', '925mb', '850mb', '500mb'),
    },
    'RH': {
        'longname': 'Relative humidity',
        'levels': ('2m', '925mb', '850mb', '500mb'),
    },
    'HGT': {
        'longname': 'Geopotential height',
        'levels': ('925mb', '850mb', '500mb'),
    },
    'PWAT': {
        'longname': 'Precipitable water',
        'levels': ('only', ),
    },
    'MSLP': {
        'longname': 'Pressure reduced to sea level',
        'levels': ('only', ),
    },

}
