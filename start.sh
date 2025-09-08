#!/bin/bash

# Railway startup script for SME Debt Management Tool

# Set default port if not provided
PORT=${PORT:-8000}

echo "Starting SME Debt Management Tool..."
echo "Port: $PORT"
echo "Environment: $FLASK_ENV"
echo "Python path: $(which python)"
echo "Working directory: $(pwd)"

# Set Flask environment
export FLASK_ENV=${FLASK_ENV:-production}
export FLASK_APP=app.py

# Test if required environment variables are set
if [ -z "$PORT" ]; then
    echo "Warning: PORT environment variable not set, using default 8000"
    PORT=8000
fi

# Test if the app can be imported
echo "Testing app import..."
if ! python -c "from app import create_app; print('App import successful')"; then
    echo "App import failed! Checking for missing dependencies..."
    pip list
    exit 1
fi

# Test if gunicorn is available
echo "Checking gunicorn installation..."
if ! command -v gunicorn &> /dev/null; then
    echo "Gunicorn not found, installing..."
    pip install --no-cache-dir gunicorn==21.2.0
fi

# Verify gunicorn version
echo "Gunicorn version: $(gunicorn --version)"

echo "App import successful, starting server..."

echo "Starting gunicorn server..."
# Start the application with gunicorn
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 60 --log-level info app:app
