#!/bin/bash

# Activate virtual environment and run Flask app for debugging
test -f .venv/bin/activate && source .venv/bin/activate
exec python3 wsgi.py
