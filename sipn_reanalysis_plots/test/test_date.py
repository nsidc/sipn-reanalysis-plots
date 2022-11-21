import datetime as dt

import pytest

from sipn_reanalysis_plots.util.date import date_range


@pytest.mark.parametrize(
    'range_endpoints,expected_len',
    [
        pytest.param(
            (dt.date(2000, 1, 1), dt.date(2000, 1, 5)),
            5,
        ),
        pytest.param(
            (dt.date(1979, 1, 1), dt.date(2020, 1, 1)),
            14_976,
        ),
    ],
)
def test_date_range(range_endpoints, expected_len):
    actual = date_range(*range_endpoints)
    assert len(list(actual)) == expected_len
    assert all(isinstance(d, dt.date) for d in actual)
