#!/bin/bash
set -e

# Set default port if not provided
PORT=${PORT:-8000}

echo "Starting SME Debt Management Tool on port $PORT..."

# Start the application with gunicorn
exec gunicorn "app:create_app()" --bind "0.0.0.0:$PORT" --workers 2 --timeout 60 --log-level info
