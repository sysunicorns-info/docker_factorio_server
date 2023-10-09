#!/usr/bin/env bash

set -e

poetry run black --check src tests
poetry run isort --check-only src tests
poetry run flake8 src tests
poetry run pylint src tests
