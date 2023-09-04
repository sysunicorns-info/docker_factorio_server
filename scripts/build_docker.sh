#!/usr/bin/env bash

# Prepare requirements.txt for dependencies
poetry export -f requirements.txt --output dist/requirements.txt --without=dev,test --with-credentials

# Clean up wheels directory
if [ -d "dist/wheels" ]; then
  rm -rf dist/wheels
fi
mkdir -p dist/wheels

# Build wheels for dependencies
pip wheel -r dist/requirements.txt --wheel-dir dist/wheels

# Build wheel for package
poetry build -f wheel
mv dist/*.whl dist/wheels

# Build docker image
docker build \
    --build-arg FACTORIO_VERSION=latest \
    --build-arg FACTORIO_SAVE_PATH=/opt/app/saves/save.zip \
    -t factorio:latest .



