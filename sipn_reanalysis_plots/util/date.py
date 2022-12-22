import datetime as dt
from typing import Iterator

from sipn_reanalysis_plots._types import YearMonth


def date_range(start: dt.date, end: dt.date) -> Iterator[dt.date]:
    """Generate list of dates between start and end, inclusive."""
    delta = end - start

    for i in range(delta.days + 1):
        yield start + dt.timedelta(days=i)


def _months_since_0ad(month: dt.date | YearMonth) -> int:
    """Calculate the number of months between 0 AD and `month`.

    Ignore day portion of `date`.

    NOTE: Python's built-in datetime module doesn't support 0AD. This is only a hack for
    calculating month ranges, since Python's built-in datetime module also doesn't
    support adding or subtracting months (ignoring month length).
    """
    num_months = (12 * month.year) + month.month
    return num_months


def _yearmonth_from_months_since_0ad(months_since_0ad: int) -> YearMonth:
    divisor = 12
    quotient, remainder = divmod(months_since_0ad, divisor)

    # Handle the December case: remainder is 0, and quotient is 1 higher than it should
    # be. e.g. Dec of 0 A.D. would be 12 months since 0 A.D., and after division have
    # quotient 1 and remainder 0, but we want to return (year=0, month=12).
    if remainder == 0:
        return YearMonth(year=quotient - 1, month=divisor)

    # The simple case (all other months). e.g. November of 0 A.D. would be 11 months
    # since 0 A.D. The division operation yields quotient 0 and remainder 11.
    return YearMonth(year=quotient, month=remainder)


def month_range(
    start: dt.date | YearMonth,
    end: dt.date | YearMonth,
) -> list[YearMonth]:
    """List months that lie within `start` and `end` ("day" portion of dates ignored).

    The result is inclusive, e.g. if `end` is `2022-01`, then `(2022, 1)` will be in
    the result.
    """
    start_months_since_0ad = _months_since_0ad(start)
    end_months_since_0ad = _months_since_0ad(end)

    # Add 1 to generate inclusive closed interval result
    month_indexes_since_0ad = range(start_months_since_0ad, end_months_since_0ad + 1)

    months = [_yearmonth_from_months_since_0ad(m) for m in month_indexes_since_0ad]
    return months
