#!/bin/sh
# Runs a command inside python:3.12-slim with the project's .venv (created on
# first use). The host Python has no venv support and pip is PEP 668-locked.
# SETUPTOOLS_SCM_PRETEND_VERSION lets hatch-vcs build without git in the image.
set -eu
exec docker run --rm -i \
  --user "$(id -u):$(id -g)" \
  -e HOME=/tmp \
  -e PIP_DISABLE_PIP_VERSION_CHECK=1 \
  -e SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0.dev0 \
  ${SCRAPINGISNOTACRIME_API_KEY:+-e SCRAPINGISNOTACRIME_API_KEY} \
  -v "$PWD":/w -w /w \
  python:3.12-slim \
  sh -c '[ -x .venv/bin/python ] || { python -m venv .venv && .venv/bin/pip install -q -e ".[dev]"; } && . .venv/bin/activate && exec "$@"' sh "$@"
