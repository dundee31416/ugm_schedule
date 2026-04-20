FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy application code
COPY . .

# Create __init__.py files to make directories Python packages
RUN touch src/__init__.py \
    && touch src/api/__init__.py \
    && touch src/models/__init__.py \
    && touch src/schemas/__init__.py \
    && touch src/services/__init__.py \
    && touch src/database/__init__.py \
    && touch src/config/__init__.py \
    && touch src/utils/__init__.py

# Expose port
EXPOSE 8000

# Command will be overridden by docker-compose
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
