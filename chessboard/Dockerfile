# Set python image
FROM python:3.10-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.1.8

# Update system packages
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --upgrade pip \
    && pip install "poetry==$POETRY_VERSION"

# Set work directory
WORKDIR /app

# Configure virtual environment and install dependencies
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false \
    && poetry config experimental.new-installer false \
    && poetry install

# Copy project
COPY . .
