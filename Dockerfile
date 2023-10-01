FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Define the expected Factorio version as a build arg
ARG FACTORIO_VERSION=stable-latest

# Set Default Value as Build Args
ARG FACTORIO_SAVE_PATH=/opt/app/saves/save.zip
ARG FACTORIO_MODS_PATH=/opt/app/mods

# Set Environment Variables for
ENV FACTORIO_SAVE_PATH=${FACTORIO_SAVE_PATH}
ENV FACTORIO_MODS_PATH=${FACTORIO_MODS_PATH}

EXPOSE 34197/udp

# Install dependencies and cleanup
# TODO: Remove software-properties-common to manually add deadsnakes repo
RUN apt-get update && apt-get install -y software-properties-common && rm -rf /var/lib/apt/lists/*
RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get install -y \
    python3.11 python3.11-venv && rm -rf /var/lib/apt/lists/*

# Prepare Directories and Copy files
RUN mkdir -p /opt/app/dist/wheels && \
    mkdir -p /opt/app/tmp && \
    mkdir -p /opt/app/mods && \
    mkdir -p /opt/app/factorio && \
    mkdir -p /opt/app/saves

WORKDIR /opt/app
COPY dist/requirements.txt /opt/app/dist/requirements.txt
COPY dist/wheels/* /opt/app/dist/wheels

# Setup Virtual Environment and Install Factorio Setup CLI and dependencies and cl
RUN python3.11 -m venv /opt/app/.venv
RUN . /opt/app/.venv/bin/activate && \
    pip install -r /opt/app/dist/requirements.txt --no-index --find-links=/opt/app/dist/wheels && \
    pip install /opt/app/dist/wheels/factorio_setup_cli-*.whl && \
    rm -rf /opt/app/dist

# Download Factorio Server
RUN . /opt/app/.venv/bin/activate && python -m factorio server download ${FACTORIO_VERSION} --tmp=/opt/app/tmp --install-dir=/opt/app/factorio && rm -rf /opt/app/tmp

# Launch Factorio Server on Startup
# TODO: Add support for map generation if don't exist.
CMD [ \ 
    "/opt/app/factorio/factorio/bin/x64/factorio", \
    "--port","34197", \
    "--start-server", "${FACTORIO_SAVE_PATH}", \
    "--mod-directory","${FACTORIO_MODS_PATH}", \
    "--server-settings", "/opt/app/server-settings.json" \
    ]
