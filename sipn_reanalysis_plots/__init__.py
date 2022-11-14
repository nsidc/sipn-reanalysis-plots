# isort: skip_file
import logging
import os

from flask import Flask

from sipn_reanalysis_plots.constants.version import VERSION

logger = logging.getLogger(__name__)


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'youcanneverguess')

app.jinja_env.globals.update(VERSION=VERSION)

# NOTE: This is a circular import, but it's specified by the Flask docs:
#     https://flask.palletsprojects.com/en/3.1.x/patterns/packages/
import sipn_reanalysis_plots.routes  # noqa: E402, F401

if os.environ.get('ENABLE_PROFILER'):
    logger.info(f'Running profiler: {app.config}')

    from werkzeug.middleware.profiler import ProfilerMiddleware

    app.wsgi_app = ProfilerMiddleware(  # type: ignore
        app.wsgi_app,
        profile_dir='./.prof',
    )
