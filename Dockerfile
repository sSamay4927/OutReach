# ── Stage 1: Build React Frontend ───────────────────────────────────────────
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# ── Stage 2: Production Python Runner ───────────────────────────────────────
FROM python:3.11-slim AS runner
WORKDIR /app

# Install curl for health check verification
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python backend dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r ./backend/requirements.txt

# Copy backend source code
COPY backend/ ./backend/

# Copy built frontend assets from Stage 1
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Copy startup script and make sure it has execution permissions and UNIX line endings
COPY render_start.sh ./
RUN sed -i 's/\r$//' render_start.sh && chmod +x render_start.sh

# Environment settings
ENV PYTHONUNBUFFERED=1 \
    PORT=5000 \
    FRONTEND_DIST=/app/frontend/dist \
    DATA_DIR=/app/backend

EXPOSE 5000

CMD ["./render_start.sh"]
