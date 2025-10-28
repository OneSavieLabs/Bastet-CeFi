FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Set work directory
WORKDIR /app

# Copy pyproject.toml and uv.lock
COPY pyproject.toml uv.lock* ./

# Install dependencies with uv
RUN uv sync

# Copy application code
COPY ./cli /app/cli
COPY ./n8n_workflow /app/n8n_workflow

# Entrypoint for Typer CLI
CMD ["uv","run", "./cli/main.py", "init"]