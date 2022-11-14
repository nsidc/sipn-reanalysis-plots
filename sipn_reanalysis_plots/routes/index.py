import base64
import datetime as dt
from io import BytesIO

from flask import render_template, request

from sipn_reanalysis_plots import app
from sipn_reanalysis_plots.constants.epoch import EPOCH_START
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
            min=EPOCH_START,
            max=yesterday,
        )

    date = dt.datetime.strptime(request.args['date'], '%Y-%m-%d').date()
    fig = plot_cfsr_daily(date)

    # Convert figure to bytes for embedding
    buf = BytesIO()
    fig.savefig(buf, format='png')
    img_data = base64.b64encode(buf.getbuffer()).decode('ascii')

    return render_template(
        'plot.html.j2',
        date=date,
        min=EPOCH_START,
        max=yesterday,
        img_data=img_data,
    )
