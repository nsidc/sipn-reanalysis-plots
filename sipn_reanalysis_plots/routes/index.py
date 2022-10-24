from flask import render_template

from sipn_reanalysis_plots import app


@app.route('/')
def index():
    return render_template('hello_world.html.j2')
