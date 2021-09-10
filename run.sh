#!/usr/bin/env bash

PYTHONPATH=$PYTHONPATH:. \
LOG_MODE=LOCAL \
gunicorn \
    --bind 0.0.0.0:5100 \
    --reload \
    --logger-class app.core.logging.loggers.GunicornLogger \
'app.main:run()'
