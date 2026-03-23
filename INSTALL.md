# 🌲 TREEMOR Installation Guide

## Quick Install (PyPI)

```bash
pip install treomor
```

📋 Table of Contents

· System Requirements
· Installation Methods
  · 1. PyPI (Recommended)
  · 2. From Source
  · 3. Docker
  · 4. Docker Compose (Full Stack)
· Platform-Specific Instructions
  · Linux (Ubuntu/Debian)
  · macOS
  · Windows (WSL2)
· Verification
· Troubleshooting
· Next Steps

---

System Requirements

Minimum Requirements

Component Requirement
Python 3.9 - 3.11
RAM 4 GB
Storage 10 GB (for validation data)
OS Linux, macOS, Windows (WSL2)
Network Internet for API access

Recommended Requirements

Component Recommendation
Python 3.10
RAM 8+ GB
Storage 50+ GB SSD
CPU 4+ cores
GPU Optional (for deep learning)

Dependencies

· NumPy ≥ 1.21.0
· SciPy ≥ 1.7.0
· Pandas ≥ 1.3.0
· Xarray ≥ 0.20.0
· ObsPy ≥ 1.3.0
· Scikit-learn ≥ 1.0.0
· Dash ≥ 2.0.0

---

Installation Methods

1. PyPI (Recommended)

```bash
# Create virtual environment (recommended)
python -m venv treomor-env
source treomor-env/bin/activate  # Linux/macOS
# treomor-env\Scripts\activate   # Windows

# Install TREEMOR
pip install treomor

# Upgrade if already installed
pip install --upgrade treomor

# Install with optional dependencies
pip install treomor[ml]      # Machine learning extras
pip install treomor[dash]    # Dashboard extras
pip install treomor[all]     # All extras
```

2. From Source

```bash
# Clone the repository
git clone https://github.com/gitdeeper9/treomor.git
cd treomor

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks (for contributors)
pre-commit install
```

3. Docker

```bash
# Pull from Docker Hub (coming soon)
docker pull gitdeeper/treomor:latest

# Or build locally
git clone https://github.com/gitdeeper9/treomor.git
cd treomor
docker build -t treomor:latest .

# Run container
docker run -d \
  --name treomor \
  -p 8050:8050 \
  -p 9090:9090 \
  -v treomor_data:/data/treomor \
  treomor:latest

# View logs
docker logs -f treomor

# Stop and remove
docker stop treomor && docker rm treomor
```

4. Docker Compose (Full Stack)

```bash
# Clone repository
git clone https://github.com/gitdeeper9/treomor.git
cd treomor

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
nano .env

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes (caution: deletes data)
docker-compose down -v
```

Services included:

· Dashboard: http://localhost:8050
· Grafana: http://localhost:3000 (admin/admin)
· Jupyter Lab: http://localhost:8888
· PostgreSQL: localhost:5432
· TimescaleDB: localhost:5433
· Redis: localhost:6379
· Prometheus: localhost:9091

---

Platform-Specific Instructions

Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install system dependencies
sudo apt install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    libhdf5-dev \
    libnetcdf-dev \
    liblapack-dev \
    libblas-dev \
    gcc \
    g++ \
    git

# Create virtual environment
python3 -m venv treomor-env
source treomor-env/bin/activate

# Install TREEMOR
pip install treomor

# Test installation
treomor --version
```

macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install hdf5 netcdf

# Create virtual environment
python3 -m venv treomor-env
source treomor-env/bin/activate

# Install TREEMOR
pip install treomor

# For M1/M2 Macs, you may need:
# export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=1
# pip install treomor --no-cache-dir
```

Windows (WSL2)

Step 1: Install WSL2

```powershell
# In PowerShell as Administrator
wsl --install
# Restart computer
```

Step 2: Install Ubuntu from Microsoft Store

Step 3: Follow Linux instructions inside WSL2

```bash
# Inside WSL2 terminal
sudo apt update
sudo apt install python3-pip python3-venv
python3 -m venv treomor-env
source treomor-env/bin/activate
pip install treomor
```

Windows (Native - Experimental)

```bash
# Install Python 3.10+ from python.org
# Ensure Python is added to PATH

# Create virtual environment
python -m venv treomor-env
treomor-env\Scripts\activate

# Install Microsoft Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Install TREEMOR
pip install treomor
```

---

Verification

Check Installation

```bash
# Check version
treomor --version
# Expected: treomor version 1.0.0

# Check Python import
python -c "import treomor; print(treomor.__version__)"
# Expected: 1.0.0

# Check DOI
python -c "import treomor; print(treomor.__doi__)"
# Expected: 10.5281/zenodo.19183878

# List available commands
treomor --help
```

Run Quick Test

```python
# test_treomor.py
import treomor
from treomor.fsin import ResonanceCalculator

# Test FSIN calculations
calc = ResonanceCalculator(
    E=13e9,      # Elastic modulus (Pa)
    D=1.0,       # Diameter (m)
    L=50,        # Height (m)
    rho=450      # Density (kg/m³)
)

# Calculate fundamental frequency
f0 = calc.fundamental_frequency()
print(f"Fundamental Resonance: {f0:.2f} Hz")
# Expected: ~0.48 Hz

# Calculate TSSI
tssi = calc.calculate_tssi()
print(f"Tree Seismic Sensitivity Index: {tssi:.2f}")
# Expected: >0.6 for good sensors

print("✅ TREEMOR installed successfully!")
```

```bash
python test_treomor.py
```

Run Dashboard

```bash
# Launch dashboard
treomor-dashboard

# Access at: http://localhost:8050
```

Download Validation Data

```bash
# Download validation dataset (847 events)
treomor download-data --catalog validation

# List available events
treomor list-events --limit 10

# Analyze specific event
treomor analyze-event --id "2024_vancouver_island"
```

---

Troubleshooting

Common Issues

1. ModuleNotFoundError: No module named 'treomor'

```bash
# Check if installed
pip list | grep treomor

# Reinstall
pip uninstall treomor
pip install treomor

# Check Python path
python -c "import sys; print(sys.path)"
```

2. ImportError: libhdf5.so.xxx: cannot open shared object file

```bash
# Ubuntu/Debian
sudo apt install libhdf5-dev

# macOS
brew install hdf5

# Windows
# Install HDF5 from: https://www.hdfgroup.org/downloads/hdf5/
```

3. MemoryError when loading large datasets

```python
# Use chunked reading
import xarray as xr
ds = xr.open_dataset('data.nc', chunks={'time': 1000})

# Or limit data
treomor load-data --catalog validation --max-events 100
```

4. Dashboard won't start (port 8050 in use)

```bash
# Find process using port
lsof -i :8050  # Linux/macOS
netstat -ano | findstr :8050  # Windows

# Kill process or change port
treomor-dashboard --port 8051
```

5. Permission denied on Linux

```bash
# Fix permissions
sudo chown -R $USER:$USER ~/.cache/pip
sudo chown -R $USER:$USER ~/.local

# Or use --user flag
pip install --user treomor
```

6. SSL certificate errors

```bash
# Update certificates
pip install --upgrade certifi

# Or temporarily (not recommended for production)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org treomor
```

Getting Help

· GitHub Issues: https://github.com/gitdeeper9/treomor/issues
· Documentation: https://treomor.readthedocs.io
· Email: gitdeeper@gmail.com

---

Next Steps

1. Quick Start Tutorial

```bash
# Download sample data
treomor download-sample

# Run detection on sample
treomor detect --input sample_data.h5 --output results.json

# View results
treomor view-results results.json
```

2. Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit with your settings
nano .env  # or use your preferred editor

# Key settings to configure:
# - TREEMOR_DATA_DIR: Path to data storage
# - USGS_API_KEY: For real-time earthquake data (optional)
# - MAPBOX_TOKEN: For interactive maps (optional)
```

3. Set Up Database (Optional)

```bash
# Initialize PostgreSQL database
createdb treomor
psql -d treomor -f database/schema.sql

# Run migrations
alembic upgrade head

# Load validation data
treomor load-data --catalog validation/847_events.h5
```

4. Enable Real-Time Monitoring

```bash
# Start real-time monitoring
treomor monitor --stream realtime

# With custom thresholds
treomor monitor --tssi-threshold 0.6 --magnitude-threshold 3.5
```

5. Deploy Dashboard (Production)

See DEPLOY.md for production deployment options:

· Netlify (frontend)
· Docker Compose (full stack)
· Kubernetes (scalable)
· Cloud platforms (AWS, GCP, Azure)

---

Uninstallation

```bash
# Remove package
pip uninstall treomor

# Remove virtual environment
rm -rf treomor-env

# Remove Docker containers
docker rm -f treomor
docker-compose down -v

# Remove data (caution!)
rm -rf /data/treomor
```

---

Support

· Documentation: https://treomor.readthedocs.io
· Examples: https://github.com/gitdeeper9/treomor/tree/main/examples
· Issues: https://github.com/gitdeeper9/treomor/issues
· Discussions: https://github.com/gitdeeper9/treomor/discussions

---

🌲 TREEMOR is now ready! Start detecting earthquakes with the world's forests.

```
pip install treomor && treomor-dashboard
```

When forests become Earth's sentinels, conservation becomes infrastructure.

— Samir Baladi, March 2026
