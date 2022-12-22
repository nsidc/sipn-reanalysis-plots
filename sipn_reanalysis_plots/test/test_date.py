import datetime as dt

import pytest

from sipn_reanalysis_plots.util.date import date_range, month_range


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


@pytest.mark.parametrize(
    'range_endpoints,expected',
    [
        pytest.param(
            (dt.date(2021, 1, 1), dt.date(2021, 1, 1)),
            [
                {'year': 2021, 'month': 1},
            ],
        ),
        pytest.param(
            (dt.date(2021, 1, 31), dt.date(2021, 2, 1)),
            [
                {'year': 2021, 'month': 1},
                {'year': 2021, 'month': 2},
            ],
        ),
        pytest.param(
            (dt.date(2021, 1, 15), dt.date(2021, 5, 3)),
            [{'year': 2021, 'month': n} for n in range(1, 5 + 1)],
        ),
        pytest.param(
            (dt.date(1981, 1, 1), dt.date(1982, 3, 1)),
            [
                *[{'year': 1981, 'month': n} for n in range(1, 12 + 1)],
                {'year': 1982, 'month': 1},
                {'year': 1982, 'month': 2},
                {'year': 1982, 'month': 3},
            ],
        ),
    ],
)
def test_month_range(range_endpoints, expected):
    actual = month_range(*range_endpoints)
    assert [a.__dict__ for a in actual] == expected


@pytest.mark.parametrize(
    'range_endpoints,expected_len',
    [
        pytest.param((dt.date(2021, 1, 1), dt.date(2021, 1, 1)), 1),
        pytest.param((dt.date(2021, 1, 1), dt.date(2022, 1, 1)), 13),
        pytest.param((dt.date(2021, 1, 31), dt.date(2021, 2, 1)), 2),
        pytest.param((dt.date(2017, 1, 31), dt.date(2021, 2, 1)), 50),
    ],
)
def test_month_range_by_len(range_endpoints, expected_len):
    actual = len(month_range(*range_endpoints))
    assert actual == expected_len
