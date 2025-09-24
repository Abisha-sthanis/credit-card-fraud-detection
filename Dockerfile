# -------------------------------
# ATM Fraud Detection - Dockerfile
# -------------------------------

# Use Python 3.13 slim image
FROM python:3.13-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Set working directory
WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
 && rm -rf /var/lib/apt/lists/*

# Copy dependency list
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt gunicorn

# Copy project files into container
COPY . .

# Expose application port
EXPOSE 5000

# Run the Flask app with Gunicorn (app.py must define `app = Flask(__name__)`)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers=3", "--threads=2", "--timeout=120"]
