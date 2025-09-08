#!/bin/bash

# Railway startup script for SME Debt Management Tool

# Set default port if not provided
PORT=${PORT:-8000}

echo "Starting SME Debt Management Tool..."
echo "Port: $PORT"

# Export PORT for the application
export PORT=$PORT

# Set Flask environment
export FLASK_ENV=production
export FLASK_APP=app.py

# Quick app import test
echo "Testing app import..."
python -c "from app import app; print('App import successful')" || exit 1

echo "Starting gunicorn server..."
# Start the application with gunicorn
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 30 --log-level info app:app
