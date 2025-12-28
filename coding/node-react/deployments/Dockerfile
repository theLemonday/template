# syntax=docker/dockerfile:1
ARG NODE_VERSION=22
ARG IMAGE_REGISTRY=""

# --- Stage 1: Base (Prerequisites) ---
FROM ${IMAGE_REGISTRY}/node:${NODE_VERSION}-alpine AS base
# Enable Corepack (includes pnpm) to avoid 'npm i -g pnpm'
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
WORKDIR /app

# --- Stage 2: Dependencies (Cache Layer) ---
FROM base AS deps
# Copy only lockfiles first to leverage caching
COPY package.json pnpm-lock.yaml ./
# --frozen-lockfile: strict deterministic install
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile

# --- Stage 3: Development (Watch Target) ---
FROM base AS dev
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# Expose Vite's default port
EXPOSE 5173
# --host is required for container port mapping
CMD ["pnpm", "run", "dev", "--", "--host"]

# --- Stage 4: Builder (Production Compile) ---
FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# Build the static assets (creates /app/dist)
RUN pnpm run build

# --- Stage 5: Production (Runtime) ---
# We switch to Nginx for serving static files
FROM ${IMAGE_REGISTRY}/nginx:alpine AS prod
# Copy custom Nginx config (optional, but recommended for SPA)
# COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
