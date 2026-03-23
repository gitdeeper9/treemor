# TREEMOR Docker Image
# Multi-stage build for optimized production deployment

# ============================================
# Stage 1: Builder
# ============================================
FROM python:3.10-slim as builder

WORKDIR /build

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libhdf5-dev \
    libnetcdf-dev \
    liblapack-dev \
    libblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml setup.py setup.cfg MANIFEST.in ./
COPY README.md ./

# Install build dependencies
RUN pip install --upgrade pip wheel setuptools

# Build the package
COPY treemor/ treemor/
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels .

# ============================================
# Stage 2: Runtime
# ============================================
FROM python:3.10-slim

LABEL maintainer="Samir Baladi <gitdeeper@gmail.com>"
LABEL description="TREEMOR - Bio-Seismic Sensing & Planetary Infrasound Resonance"
LABEL version="1.0.0"
LABEL doi="10.5281/zenodo.19183878"

WORKDIR /app

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \
    libhdf5-dev \
    libnetcdf-dev \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r treemor && useradd -r -g treemor treemor

# Copy wheels from builder
COPY --from=builder /build/wheels /wheels

# Install TREEMOR and dependencies
RUN pip install --no-cache-dir /wheels/* && \
    pip install --no-cache-dir \
    numpy>=1.21.0 \
    scipy>=1.7.0 \
    pandas>=1.3.0 \
    xarray>=0.20.0 \
    netCDF4>=1.5.0 \
    h5py>=3.6.0 \
    matplotlib>=3.4.0 \
    plotly>=5.0.0 \
    dash>=2.0.0 \
    obspy>=1.3.0 \
    scikit-learn>=1.0.0 \
    click>=8.0.0 \
    tqdm>=4.62.0

# Create data directories
RUN mkdir -p /data/treemor/{catalog,sensors,fsin,validation,insar,models,logs} && \
    chown -R treemor:treemor /data/treemor

# Copy configuration
COPY .env.example .env
COPY treomor/config/ config/

# Copy entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Switch to non-root user
USER treemor

# Expose ports
EXPOSE 8050  # Dashboard
EXPOSE 9090  # Metrics

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8050/health || exit 1

ENTRYPOINT ["docker-entrypoint.sh"]

# Default command
CMD ["treomor-dashboard"]
