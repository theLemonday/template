ARG PYTHON_VERSION
ARG BASE_REGISTRY

# --- Stage 1: Builder (uv & dependencies) ---
FROM ${BASE_REGISTRY}python:${PYTHON_VERSION}-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Enable bytecode compilation for faster startup
ENV UV_COMPILE_BYTECODE=1
# Use a virtual environment for isolation, even in Docker
ENV UV_LINK_MODE=copy

# Install dependencies (leverage cache)
# We copy only the lockfiles first
COPY pyproject.toml uv.lock ./
# --frozen ensures we stick exactly to the lockfile
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-install-project --no-dev

# --- Stage 2: Development (Watch Target) ---
FROM ${BASE_REGISTRY}python:${PYTHON_VERSION}-slim AS dev
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app

# Copy the venv from builder
COPY --from=builder /app/.venv /app/.venv

# Add venv to PATH so we can run 'python' or 'gunicorn' directly
ENV PATH="/app/.venv/bin:$PATH"

COPY . .
# Sync dev dependencies (if any extra) and install the project itself
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen

EXPOSE 8000
# Django development server (auto-reloads)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# --- Stage 3: Production (Runtime) ---
FROM ${BASE_REGISTRY}python:${PYTHON_VERSION}-slim AS prod
WORKDIR /app

# Copy only the virtual environment from builder (no dev tools)
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY . .

# Create a non-root user for security
RUN useradd -m django && chown -R django:django /app
USER django

EXPOSE 8000
# Use Gunicorn for production
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
