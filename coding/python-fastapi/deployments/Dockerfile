# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.12
# Renamed variable as requested
ARG IMAGE_REGISTRY="docker.io"

# --- Stage 1: Builder (uv & dependencies) ---
FROM ${IMAGE_REGISTRY}/python:${PYTHON_VERSION}-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install dependencies
COPY pyproject.toml uv.lock ./
# --frozen: strict lockfile sync
# --no-dev: exclude test/lint dependencies for prod
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-install-project --no-dev

# --- Stage 2: Development (Watch Target) ---
FROM ${IMAGE_REGISTRY}/python:${PYTHON_VERSION}-slim AS dev
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app

# Copy venv from builder
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY . .
# Sync dev dependencies (ruff, pytest, etc.)
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen

EXPOSE 8000
# Run Uvicorn with reload for dev
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# --- Stage 3: Production (Runtime) ---
FROM ${IMAGE_REGISTRY}/python:${PYTHON_VERSION}-slim AS prod
WORKDIR /app

# Copy only the runtime venv
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY . .

# Create non-root user
RUN useradd -m fastapi && chown -R fastapi:fastapi /app
USER fastapi

EXPOSE 8000
# Production: No reload, optimized workers
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
