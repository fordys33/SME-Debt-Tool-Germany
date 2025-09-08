#!/bin/bash

# Railway startup script for SME Debt Management Tool

# Set default port if not provided
PORT=${PORT:-8000}

echo "Starting SME Debt Management Tool..."
echo "Port: $PORT"
echo "Environment: $FLASK_ENV"

# Start the application with gunicorn
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 30 app:app
