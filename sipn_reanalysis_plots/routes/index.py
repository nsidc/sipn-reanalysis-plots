import base64
from datetime import date
from io import BytesIO

from flask import render_template

from sipn_reanalysis_plots import app
from sipn_reanalysis_plots.util.data import read_cfsr_daily_file
from sipn_reanalysis_plots.util.plot import plot_temperature_variable 


@app.route('/')
def index():
    dataset = read_cfsr_daily_file(date(1979, 1, 1))
    fig = plot_temperature_variable(dataset)

    # Convert figure to bytes for embedding
    buf = BytesIO()
    fig.savefig(buf, format='png')
    img_data = base64.b64encode(buf.getbuffer()).decode('ascii')

    return render_template('hello_world.html.j2', img_data=img_data)
