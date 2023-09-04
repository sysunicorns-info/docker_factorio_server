FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ARG FACTORIO_SAVE_PATH=/opt/app/saves/save.zip

# Install dependencies
# TODO: Remove software-properties-common to manually add deadsnakes repo
RUN apt-get update && apt-get install -y software-properties-common && rm -rf /var/lib/apt/lists/*
RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get install -y \
    python3.11 python3.11-venv && rm -rf /var/lib/apt/lists/*

# Copy files
RUN mkdir -p /opt/app/dist/wheels && mkdir -p /opt/app/tmp && mkdir -p /opt/app/factorio && mkdir -p /opt/app/saves
WORKDIR /opt/app
COPY dist/wheels/* /opt/app/dist/wheels
COPY dist/requirements.txt /opt/app/dist/requirements.txt

RUN python3.11 -m venv /opt/app/.venv
RUN . /opt/app/.venv/bin/activate && pip install -r /opt/app/dist/requirements.txt --no-index --find-links=/opt/app/dist/wheels
RUN . /opt/app/.venv/bin/activate && pip install /opt/app/dist/wheels/factorio_setup_cli-*.whl
RUN . /opt/app/.venv/bin/activate && python -m factorio server download latest --tmp=/opt/app/tmp --install-dir=/opt/app/factorio && rm -rf /opt/app/tmp

CMD [ "/opt/app/factorio/factorio/bin/x64/factorio", "--start-server", "${FACTORIO_SAVE_PATH}", "--server-settings", "/opt/app/server-settings.json" ]
