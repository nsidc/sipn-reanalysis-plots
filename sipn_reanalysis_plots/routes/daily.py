import functools

from flask import render_template, request

from sipn_reanalysis_plots import app
from sipn_reanalysis_plots.constants.variables import VARIABLES
from sipn_reanalysis_plots.forms import DailyPlotForm
from sipn_reanalysis_plots.util.data.list import list_daily_data_dates
from sipn_reanalysis_plots.util.fig import fig_to_high_and_lowres_base64
from sipn_reanalysis_plots.util.plot import plot_cfsr_daily


@app.route('/')
@app.route('/daily')
def daily():
    submitted = request.args != {}
    form = DailyPlotForm(request.args)

    available_dates = list_daily_data_dates()
    min_date = available_dates[0]
    max_date = available_dates[-1]
    render = functools.partial(
        render_template,
        'daily.html.j2',
        min_available_data=f'{min_date:%Y-%m-%d}',
        max_available_data=f'{max_date:%Y-%m-%d}',
        form=form,
        variables=VARIABLES,
    )

    # NOTE: We're not using flask_wtf's `validate_on_submit` helper deliberately here
    # because it expects the form's method to be POST, PUT, PATCH, or DELETE, but we're
    # using GET so URLs can be shared.
    if not submitted or not form.validate():
        return render()

    fig = plot_cfsr_daily(
        form.start_date.data,
        end_date=form.end_date.data,
        variable=form.variable.data,
        level=form.analysis_level.data,
        as_filled_contour=form.contour.data,
        anomaly=form.anomaly.data,
    )

    img_b64_small, img_b64_big = fig_to_high_and_lowres_base64(fig)

    return render(
        img_b64_small=img_b64_small,
        img_b64_big=img_b64_big,
    )
