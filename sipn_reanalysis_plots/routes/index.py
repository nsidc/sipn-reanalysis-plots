import base64
import datetime as dt
from io import BytesIO

from flask import render_template

from sipn_reanalysis_plots import app
from sipn_reanalysis_plots.util.plot import plot_cfsr_daily


@app.route('/')
def index():
    fig = plot_cfsr_daily(dt.date(1979, 2, 1))

    # Convert figure to bytes for embedding
    buf = BytesIO()
    fig.savefig(buf, format='png')
    img_data = base64.b64encode(buf.getbuffer()).decode('ascii')

    return render_template('hello_world.html.j2', img_data=img_data)
