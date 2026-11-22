#!/usr/bin/env sh
# Start Chartist on macOS or Linux. Needs Python 3.10 or newer.
cd "$(dirname "$0")" && exec python3 chartist/app.py "$@"
