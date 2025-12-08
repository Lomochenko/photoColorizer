# Multi-stage build for production
FROM node:18-alpine AS builder

# Install build dependencies
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM node:18-alpine AS runner

# Install runtime dependencies
RUN apk add --no-cache libc6-compat python3 py3-pip
WORKDIR /app

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nuxt

# Copy built application
COPY --from=builder --chown=nuxt:nodejs /app/.output ./.output
COPY --from=builder --chown=nuxt:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nuxt:nodejs /app/package.json ./package.json

# Copy Python model files (if needed)
COPY --chown=nuxt:nodejs python/ ./python/

# Install Python dependencies
RUN pip install --no-cache-dir -r python/requirements.txt

# Switch to non-root user
USER nuxt

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/api/health || exit 1

# Start the application
CMD ["node", ".output/server/index.mjs"]