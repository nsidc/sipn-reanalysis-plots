import base64
import datetime as dt
import json
from io import BytesIO

from flask import render_template, request

from sipn_reanalysis_plots import app
from sipn_reanalysis_plots.constants.epoch import EPOCH_START
from sipn_reanalysis_plots.constants.variables import VARIABLES
from sipn_reanalysis_plots.util.plot import plot_cfsr_daily


@app.route('/')
def index():
    # TODO: Use real yesterday value once we have current test data
    # yesterday = dt.date.today() - dt.timedelta(days=1)
    yesterday = dt.date(EPOCH_START.year, 12, 31)

    if request.args == {}:
        return render_template(
            'plot.html.j2',
            date=yesterday,
            min_date=EPOCH_START,
            max_date=yesterday,
            variables=VARIABLES,
        )

    date = dt.datetime.strptime(request.args['date'], '%Y-%m-%d').date()
    variable = request.args['variable']
    level = request.args['level']
    fig = plot_cfsr_daily(date, variable=variable, level=level)

    # Convert figure to bytes for embedding
    buf = BytesIO()
    fig.savefig(buf, format='png')
    img_data = base64.b64encode(buf.getbuffer()).decode('ascii')

    return render_template(
        'plot.html.j2',
        date=date,
        min_date=EPOCH_START,
        max_date=yesterday,
        variables=VARIABLES,
        variable=variable,
        level=level,
        img_data=img_data,
    )
