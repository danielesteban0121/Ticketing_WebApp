#!/bin/bash
set -e

SERVICE_NAME=${1:-ms-categories}

cd /opt/render/project/src

exec gunicorn -k uvicorn.workers.UvicornWorker ${SERVICE_NAME}.main:app --bind 0.0.0.0:${PORT} --workers 2
