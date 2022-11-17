import datetime as dt

from flask_wtf import FlaskForm
from wtforms import Field, Form, fields, validators

from sipn_reanalysis_plots.constants.epoch import EPOCH_START
from sipn_reanalysis_plots.constants.variables import VARIABLES

# TODO: Remove mock and use yesterday as end of epoch date
mock_end_of_epoch = dt.date(EPOCH_START.year, 12, 31)


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


class DailyPlotForm(PlotForm):
    start_date = fields.DateField(
        'Start date',
        # Use real today value
        # default=dt.date.today,
        default=mock_end_of_epoch,
        validators=[
            validators.InputRequired(),
            validate_date_in_epoch,
        ],
    )
    end_date = fields.DateField(
        'End date (leave blank for single day)',
        validators=[
            validators.Optional(),
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

        if start_date > end_date:
            raise validators.ValidationError(
                'End date must be after start date.'
            )

        start_date_plus_one_year = dt.date(
            start_date.year + 1,
            start_date.month,
            start_date.day,
        )
        if end_date >= start_date_plus_one_year:
            raise validators.ValidationError(
                'Difference between start and end date must be less than 1 year.'
            )
