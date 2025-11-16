# ============================
# Stage 1 — Builder
# ============================
FROM python:3.10-slim AS builder

WORKDIR /app

# Install system dependencies needed for ML packages (pandas, numpy, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirement file and install dependencies
COPY requirements.txt .

# Create a virtual environment inside the builder
RUN python -m venv /opt/venv

# Activate venv and install packages
RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt


# ============================
# Stage 2 — Final Runtime
# ============================
FROM python:3.10-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Ensure venv is used for all python commands
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy app source code
COPY . .

# ----------------------------
# ✅ Fix: create non-root user and ensure /app is writable
# ----------------------------
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Expose FastAPI port
EXPOSE 8000

# Start the FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
