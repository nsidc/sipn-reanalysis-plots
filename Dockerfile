FROM mambaorg/micromamba:0.23.3

WORKDIR /app

# Activate the conda environment during build process
ARG MAMBA_DOCKERFILE_ACTIVATE=1

# NOTE: For some reason, micromamba doesn't like the filename
# "environment-lock.yml". It fails to parse it because it's missing some
# special lockfile key.
COPY environment-lock.yml ./environment.yml

# Install dependencies to conda environment
RUN micromamba install -y \
    # NOTE: -p is important to install to the "base" env
    -p /opt/conda \
    -f environment.yml
RUN micromamba clean --all --yes

# Install source
COPY ./setup.py .
COPY ./.mypy.ini .
COPY ./tasks ./tasks
COPY ./sipn_reanalysis_plots ./sipn_reanalysis_plots

ENV FLASK_APP=sipn_reanalysis_plots

# Did the build work?
RUN python -c "import flask"
RUN which flask

# Start a WSGI server
# WARNING: Using CMD is key; using ENTRYPOINT overrides the micromamba
# entrypoint and prevents env activation.
CMD ["gunicorn", "?"]
