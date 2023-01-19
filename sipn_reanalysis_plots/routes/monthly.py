import functools
from pathlib import Path

from flask import abort, render_template, request

from sipn_reanalysis_plots import app
from sipn_reanalysis_plots._types import YearMonth
from sipn_reanalysis_plots.constants.paths import DATA_DIR
from sipn_reanalysis_plots.constants.variables import VARIABLES
from sipn_reanalysis_plots.errors import NoDataFoundError
from sipn_reanalysis_plots.forms import MonthlyPlotForm
from sipn_reanalysis_plots.util.data.list import (
    max_monthly_data_yearmonth_str,
    min_monthly_data_yearmonth_str,
)
from sipn_reanalysis_plots.util.fig import fig_to_high_and_lowres_base64
from sipn_reanalysis_plots.util.plot import plot_cfsr_monthly


# TODO: DRY. Very similar to daily route. Maybe:
#       return plot_form(
#           args=request.args,
#           form=MonthlyPlotForm,
#           plot_func=plot_cfsr_monthly,
#       )
@app.route('/monthly')
def monthly():
    submitted = request.args != {}

    try:
        form = MonthlyPlotForm(request.args)
        render = functools.partial(
            render_template,
            'monthly.html.j2',
            min_available_data=min_monthly_data_yearmonth_str(),
            max_available_data=max_monthly_data_yearmonth_str(),
            form=form,
            variables=VARIABLES,
        )
    except NoDataFoundError as e:
        abort(code=500, description=str(e))

    # NOTE: We're not using flask_wtf's `validate_on_submit` helper deliberately here
    # because it expects the form's method to be POST, PUT, PATCH, or DELETE, but we're
    # using GET so URLs can be shared.
    if not submitted or not form.validate():
        return render()

    start_month = YearMonth(
        year=form.start_month.data.year,
        month=form.start_month.data.month,
    )
    end_month = (
        None
        if not form.end_month.data
        else YearMonth(
            year=form.end_month.data.year,
            month=form.end_month.data.month,
        )
    )

    try:
        fig = plot_cfsr_monthly(
            start_month,
            end_month=end_month,
            variable=form.variable.data,
            level=form.analysis_level.data,
            as_filled_contour=form.contour.data,
            anomaly=form.anomaly.data,
        )
    except FileNotFoundError as e:
        fn = Path(e.filename.decode('utf-8')).relative_to(DATA_DIR)
        return render(
            error=(
                f'Requested file not found: "{fn}".'
                ' Please report this message to ops so data can be ingested.',
            )
        )

    img_b64_small, img_b64_big = fig_to_high_and_lowres_base64(fig)

    return render(
        img_b64_small=img_b64_small,
        img_b64_big=img_b64_big,
    )
