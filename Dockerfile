FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Health check with better error handling
HEALTHCHECK --interval=30s --timeout=15s --start-period=30s --retries=5 \
    CMD curl -f http://localhost:5000/health || exit 1

# Create startup script
RUN echo '#!/bin/bash\n\
echo "=== Container Startup Diagnostics ===\n\
echo "Python version: $(python --version)"\n\
echo "Working directory: $(pwd)"\n\
echo "PORT environment variable: ${PORT:-Not set}"\n\
echo "FLASK_ENV: ${FLASK_ENV:-Not set}"\n\
echo "Files in directory:"\n\
ls -la\n\
echo "=== Testing Application Import ===\n\
python -c "import sys; print(f\"Python path: {sys.path[:3]}\"); import app; print(\"✅ App import successful\")" || { echo "❌ App import failed"; exit 1; }\n\
echo "=== Starting Application ===\n\
exec python app.py' > /app/start.sh && chmod +x /app/start.sh

# Run the application with diagnostics
CMD ["/app/start.sh"]
