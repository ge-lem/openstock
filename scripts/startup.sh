#!/bin/bash
. /path/to/venv/bin/activate
cd /path/to/openstock
gunicorn openstock.wsgi:application --bind=0.0.0.0:8000

