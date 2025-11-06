# Multi-stage build for development and production

# Base stage
FROM node:20-alpine AS base

WORKDIR /app

# Install pnpm
RUN npm install -g pnpm

# Development stage
FROM base AS dev

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install all dependencies (including dev dependencies)
RUN pnpm install --frozen-lockfile

# Expose port for Vite dev server
EXPOSE 5173

# Start development server with hot reload
CMD ["pnpm", "dev", "--host", "0.0.0.0"]

# Build stage
FROM base AS builder

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Build arguments for version info
ARG HEIMDALLR_VERSION
ENV VITE_APP_VERSION=$HEIMDALLR_VERSION
ARG COMMIT_ID
ENV VITE_COMMIT_ID=$COMMIT_ID

# Build the application
RUN pnpm build

# Production stage
FROM nginx:alpine AS production

# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]