# ---------------------
# Base image
# ---------------------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# ---------------------
# Install system deps
# ---------------------
RUN apt-get update && apt-get install -y curl build-essential

# ---------------------
# Install Poetry
# ---------------------
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# ---------------------
# Copy project files
# ---------------------
COPY pyproject.toml poetry.lock* README.md /app/
COPY src /app/src

# ---------------------
# Install dependencies
# ---------------------
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

# ---------------------
# Expose port
# ---------------------
EXPOSE 8000

# ---------------------
# Run app
# ---------------------
CMD ["uvicorn", "orders_service.api.main:app", "--host", "0.0.0.0", "--port", "8000"]