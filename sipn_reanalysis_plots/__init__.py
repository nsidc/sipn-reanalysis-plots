# isort: skip_file
import logging
import os

from flask import Flask
from flask_bootstrap import Bootstrap5

from sipn_reanalysis_plots.constants.version import VERSION

logger = logging.getLogger(__name__)


app = Flask(__name__)
Bootstrap5(app)

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'youcanneverguess')

app.jinja_env.globals.update(VERSION=VERSION)

# NOTE: This is a circular import, but it's specified by the Flask docs:
#     https://flask.palletsprojects.com/en/3.1.x/patterns/packages/
import sipn_reanalysis_plots.routes  # noqa: E402, F401

# Profile data produced with this middleware may be visualized from file using snakeviz.
if os.environ.get('ENABLE_PROFILER'):
    logger.info(f'Running profiler: {app.config}')

    from werkzeug.middleware.profiler import ProfilerMiddleware

    app.wsgi_app = ProfilerMiddleware(  # type: ignore
        app.wsgi_app,
        profile_dir='./.prof',
    )

# Dask dashboard can be accessed at port 8787.
# NOTE: There is a strange race condition that results in a "disconnected" dashboard,
# and I haven't figured out a solution.  Recommend starting up dev server with these
# lines commented, then uncommenting them (the dev server will reload and the dashboard
# will be connected to the right cluster).
# if os.environ.get('ENABLE_DASK_DASHBOARD'):
#     from dask.distributed import Client
#     client = Client()
