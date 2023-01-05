import datetime as dt
from typing import Callable

from flask_wtf import FlaskForm
from wtforms import Field, Form, fields, validators

from sipn_reanalysis_plots.constants.variables import VARIABLES
from sipn_reanalysis_plots.util.data.list import (
    max_daily_data_date,
    max_daily_data_date_str,
    max_monthly_data_yearmonth,
    max_monthly_data_yearmonth_str,
    min_daily_data_date,
    min_daily_data_date_str,
    min_monthly_data_yearmonth,
    min_monthly_data_yearmonth_str,
)


class MagicString:
    """Enable instantiation of objects which look stringy enough to wtforms.

    This enables us to have dynamic values to pass to `render_kw` so, for example, every
    time a new form is instantiated a check will be done to find the latest available
    data and render a field based on that result, e.g. limit a date field to a min/max
    value of the min/max available data.
    """

    def __init__(self, func: Callable[[], str]):
        self.func = func

    def __str__(self):
        return f'{self.func()}'


# TODO: Remove mock and use most recent file as end of epoch date
mock_end_of_epoch = dt.date(dt.date.today().year, 12, 31)
date_render_kw = {
    'min': MagicString(min_daily_data_date_str),
    'max': MagicString(max_daily_data_date_str),
}
month_render_kw = {
    'min': MagicString(min_monthly_data_yearmonth_str),
    'max': MagicString(max_monthly_data_yearmonth_str),
}


class CoercesOk(validators.DataRequired):
    """Validate like DataRequired, but prevent Javascript empty check.

    The DataRequired validator applies Javascript validation that the field is not
    empty, and this widget disables that behavior.

    The parent class turns on this Javascript behavior by setting the field flag on
    init, but this class omits this line:
        self.field_flags = {"required": True}
    """

    def __init__(self, message=None):
        self.message = message


def validate_date_in_available_range(form: Form, field: Field) -> None:
    min_date = min_daily_data_date()
    max_date = max_daily_data_date()

    if field.data < min_date or field.data > max_date:
        raise validators.ValidationError(
            f'Date must be within range ({min_date:%Y-%m-%d}, {max_date:%Y-%m-%d})',
        )


def validate_month_in_available_range(form: Form, field: Field) -> None:
    min_yearmonth = min_monthly_data_yearmonth()
    min_yearmonth_str = min_monthly_data_yearmonth_str()
    min_date = dt.date(min_yearmonth.year, min_yearmonth.month, 1)
    max_yearmonth = max_monthly_data_yearmonth()
    max_yearmonth_str = max_monthly_data_yearmonth_str()
    max_date = dt.date(max_yearmonth.year, max_yearmonth.month, 1)

    if field.data < min_date or field.data > max_date:
        raise validators.ValidationError(
            f'Month must be within range ({min_yearmonth_str}, {max_yearmonth_str})'
        )


class PlotForm(FlaskForm):
    class Meta:
        # We don't care about CSRF in this app, and we'd rather not have a token in our
        # URL.
        csrf = False

    variable = fields.SelectField(
        'Variable',
        choices=[(key, val['long_name']) for key, val in VARIABLES.items()],
        validators=[validators.InputRequired()],
    )
    analysis_level = fields.SelectField(
        'Analysis level',
        choices=[],
        validate_choice=False,
        validators=[validators.InputRequired()],
    )

    contour = fields.BooleanField(
        'Display as filled contours?',
        default=False,
        validators=[],
    )
    anomaly = fields.BooleanField(
        'Calculate anomaly from 1981-2010 climatology?',
        default=False,
        validators=[],
    )


class DailyPlotForm(PlotForm):
    start_date = fields.DateField(
        'Start date',
        default=max_daily_data_date,
        render_kw=date_render_kw,
        validators=[
            validators.DataRequired(message="This field requires format 'YYYY-MM-DD'"),
            validate_date_in_available_range,
        ],
    )
    end_date = fields.DateField(
        'End date (leave blank for single day)',
        render_kw=date_render_kw,
        validators=[
            validators.Optional(),
            CoercesOk(message="This field requires format 'YYYY-MM-DD'"),
            validate_date_in_available_range,
        ],
    )

    def validate_end_date(form: Form, field: Field) -> None:
        """Validate relationship between start and end date."""
        start_date = form.start_date.data
        end_date = field.data
        if not end_date:
            # If no end date is provided, we don't need to validate relationship between
            # start and end date.
            return

        if start_date >= end_date:
            raise validators.ValidationError('End date must be after start date.')

        start_date_plus_one_year = dt.date(
            start_date.year + 1,
            start_date.month,
            start_date.day,
        )
        if end_date >= start_date_plus_one_year:
            raise validators.ValidationError(
                'Difference between start and end date must be less than 1 year.'
            )


class MonthlyPlotForm(PlotForm):
    start_month = fields.MonthField(
        'Start month',
        default=lambda: dt.date(
            max_monthly_data_yearmonth().year,
            max_monthly_data_yearmonth().month,
            1,
        ),
        render_kw=month_render_kw,
        validators=[
            validators.DataRequired(message="This field requires format 'YYYY-MM'"),
            validate_month_in_available_range,
        ],
    )
    end_month = fields.MonthField(
        'End month (leave blank for single month)',
        render_kw=month_render_kw,
        validators=[
            validators.Optional(),
            CoercesOk(message="This field requires format 'YYYY-MM'"),
            validate_month_in_available_range,
        ],
    )

    def validate_end_month(form: Form, field: Field) -> None:
        """Validate relationship between start and end month.

        TODO: DRY. This validator is same as the daily plot validator (the month fields
        are really dates with day=1)

        TODO: Why is this a validator method instead of function passed to the field's
        validator array?
        """
        start_month = form.start_month.data
        end_month = field.data
        if not end_month:
            # If no end month is provided, we don't need to validate relationship
            # between start and end month.
            return

        if start_month >= end_month:
            raise validators.ValidationError('End date must be after start date.')

        start_month_plus_one_year = dt.date(
            start_month.year + 1,
            start_month.month,
            start_month.day,
        )
        if end_month >= start_month_plus_one_year:
            raise validators.ValidationError(
                'Difference between start and end month must be less than 1 year.'
            )
