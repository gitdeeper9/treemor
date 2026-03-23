#!/bin/bash
# TREEMOR Docker Entrypoint Script

set -e

echo "🌲 TREEMOR - Bio-Seismic Sensing & Planetary Infrasound Resonance"
echo "Version: 1.0.0 | DOI: 10.5281/zenodo.19183878"
echo ""

# Check if data directory exists
if [ ! -d "$TREEMOR_DATA_DIR" ]; then
    echo "Creating data directory: $TREEMOR_DATA_DIR"
    mkdir -p "$TREEMOR_DATA_DIR"/{catalog,sensors,fsin,validation,insar,models,logs}
fi

# Check if .env file exists
if [ ! -f .env ] && [ -f .env.example ]; then
    echo "Copying .env.example to .env"
    cp .env.example .env
    echo "WARNING: Please update .env with your actual configuration"
fi

# Wait for PostgreSQL if needed
if [ -n "$DB_HOST" ]; then
    echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
    while ! nc -z "$DB_HOST" "$DB_PORT"; do
        sleep 1
    done
    echo "PostgreSQL is ready!"
fi

# Wait for TimescaleDB if needed
if [ -n "$TIMESCALE_HOST" ]; then
    echo "Waiting for TimescaleDB at $TIMESCALE_HOST:$TIMESCALE_PORT..."
    while ! nc -z "$TIMESCALE_HOST" "$TIMESCALE_PORT"; do
        sleep 1
    done
    echo "TimescaleDB is ready!"
fi

# Run database migrations if needed
if command -v alembic &> /dev/null; then
    echo "Running database migrations..."
    alembic upgrade head
fi

# Execute the command
echo "Starting TREEMOR: $@"
exec "$@"
