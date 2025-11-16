# ============================
# Stage 1 — Builder
# ============================
FROM python:3.10-slim AS builder

WORKDIR /app

# Install system deps needed for ML (numpy, pandas, shap, matplotlib)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libgomp1 \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirement file
COPY requirements.txt .

# Create virtual environment
RUN python -m venv /opt/venv

# Install dependencies inside venv
RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


# ============================
# Stage 2 — Final Runtime
# ============================
FROM python:3.10-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Activate venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application source
COPY . .

# Create non-root user (optional but recommended)
RUN useradd -m appuser
USER appuser

# Expose FastAPI port
EXPOSE 8000

# Default command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
