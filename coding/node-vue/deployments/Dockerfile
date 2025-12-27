# syntax=docker/dockerfile:1
ARG IMAGE_REGISTRY
ARG NODE_VERSION

# --- Stage 1: Base (Prerequisites) ---
FROM {IMAGE_REGISTRY}/node:${NODE_VERSION} AS base
# Install pnpm
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

WORKDIR /app

# --- Stage 2: Dependencies (Cache Layer) ---
FROM base AS deps
COPY package.json pnpm-lock.yaml ./
# Install dependencies (frozen-lockfile ensures deterministic builds)
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile

# --- Stage 3: Development (Watch Target) ---
FROM base AS dev
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# Expose Vite/Next.js default port
EXPOSE 5173
# Ensure host binding for container access
CMD ["pnpm", "run", "dev"]

# --- Stage 4: Builder (Compile Source) ---
FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN pnpm run build

# --- Stage 5: Production (Runtime) ---
FROM nginx:alpine AS prod
# Copy the build artifacts from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html
# Optional: Copy custom Nginx config if you have one
# COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
