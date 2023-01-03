import datetime as dt

from flask_wtf import FlaskForm
from wtforms import Field, Form, fields, validators

from sipn_reanalysis_plots.constants.epoch import EPOCH_START
from sipn_reanalysis_plots.constants.variables import VARIABLES

# TODO: Remove mock and use most recent file as end of epoch date
mock_end_of_epoch = dt.date(dt.date.today().year, 12, 31)


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


def validate_date_in_epoch(form: Form, field: Field) -> None:
    if field.data < EPOCH_START:
        raise validators.ValidationError(f'Date must be later than {EPOCH_START}')

    # TODO: Use real today value once we have current test data
    # today = dt.date.today()
    today = mock_end_of_epoch + dt.timedelta(days=1)
    if field.data >= today:
        raise validators.ValidationError(f'Date must be before {today}')


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
        # TODO: use date of latest daily file
        # default=...,
        default=mock_end_of_epoch,
        render_kw={'min': EPOCH_START.isoformat()},
        validators=[
            validators.DataRequired(message="This field requires format 'YYYY-MM-DD'"),
            validate_date_in_epoch,
        ],
    )
    end_date = fields.DateField(
        'End date (leave blank for single day)',
        render_kw={'min': EPOCH_START.isoformat()},
        validators=[
            validators.Optional(),
            CoercesOk(message="This field requires format 'YYYY-MM-DD'"),
            validate_date_in_epoch,
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
        # TODO: Use date of latest monthly file
        # default=...,
        default=mock_end_of_epoch,
        render_kw={'min': EPOCH_START.isoformat()},
        validators=[
            validators.DataRequired(message="This field requires format 'YYYY-MM'"),
            validate_date_in_epoch,
        ],
    )
    end_month = fields.MonthField(
        'End month (leave blank for single month)',
        render_kw={'min': EPOCH_START.isoformat()},
        validators=[
            validators.Optional(),
            CoercesOk(message="This field requires format 'YYYY-MM'"),
            validate_date_in_epoch,
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
