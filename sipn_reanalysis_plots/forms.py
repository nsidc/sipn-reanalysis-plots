import datetime as dt

from flask_wtf import FlaskForm
from wtforms import Form, fields, validators

from sipn_reanalysis_plots.constants.epoch import EPOCH_START
from sipn_reanalysis_plots.constants.variables import VARIABLES

mock_end_of_epoch = dt.date(EPOCH_START.year, 12, 31)


def validate_date_in_epoch(form: Form, field: dt.date) -> None:
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

    submit = fields.SubmitField('Create plot!')


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
    # end_date = fields.DateField(
    #     'End date',
    #     validators=[
    #         validators.Optional(),
    #         validate_date_in_epoch,
    #     ],
    # )

    # def validate_dates_relationship(self) -> bool:
    #     if not super().validate(self):
    #         return False

    #     if self.start_date > self.end_date:
    #         raise ValidationError('Start date must be prior to end date.')

    #     if self.start_date + dt.timedelta(years=1) >= self.end_date:
    #         raise ValidationError(
    #             'Difference between start and end date must be less than 1 year.'
    #         )

