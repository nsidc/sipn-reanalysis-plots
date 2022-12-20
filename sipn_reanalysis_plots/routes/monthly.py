import base64
import functools
from io import BytesIO

from flask import render_template, request

from sipn_reanalysis_plots import app
from sipn_reanalysis_plots.constants.variables import VARIABLES
from sipn_reanalysis_plots.forms import MonthlyPlotForm
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
    form = MonthlyPlotForm(request.args)
    render = functools.partial(
        render_template,
        'monthly.html.j2',
        form=form,
        variables=VARIABLES,
    )

    # NOTE: We're not using flask_wtf's `validate_on_submit` helper deliberately here
    # because it expects the form's method to be POST, PUT, PATCH, or DELETE, but we're
    # using GET so URLs can be shared.
    if not submitted or not form.validate():
        return render()

    fig = plot_cfsr_monthly(
        form.start_date.data,
        end_date=form.end_date.data,
        variable=form.variable.data,
        level=form.analysis_level.data,
        as_filled_contour=form.contour.data,
    )

    # Convert figure to bytes for embedding
    buf = BytesIO()
    fig.savefig(buf, format='png')

    # TODO: Pass high-res and low-res images to template. High res:
    # `fig.savefig(..., dpi=600)`
    img_data = base64.b64encode(buf.getbuffer()).decode('ascii')

    return render(img_data=img_data)
