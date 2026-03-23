# TREEMOR Deployment Guide

## Deployment Options

### 1. Local Development

```bash
# Install
pip install -e .

# Run dashboard locally
treomor-dashboard

# Access at http://localhost:8050
```

2. Docker Single Container

```bash
# Build image
docker build -t treomor:latest .

# Run container
docker run -d \
  --name treomor \
  -p 8050:8050 \
  -p 9090:9090 \
  -v treomor_data:/data/treomor \
  -e DB_HOST=your_db_host \
  treomor:latest
```

3. Docker Compose (Full Stack)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

4. Netlify Dashboard

The TREEMOR dashboard is deployed at: https://treemor.netlify.app

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy from Netlify directory
cd Netlify
netlify deploy --prod --dir=public

# Or use GitLab CI (automatic on push to main)
```

5. Kubernetes (Production)

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: treomor
spec:
  replicas: 3
  selector:
    matchLabels:
      app: treomor
  template:
    metadata:
      labels:
        app: treomor
    spec:
      containers:
      - name: treomor
        image: gitdeeper/treomor:latest
        ports:
        - containerPort: 8050
        env:
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: treomor-secrets
              key: db-host
        volumeMounts:
        - name: treomor-data
          mountPath: /data/treomor
      volumes:
      - name: treomor-data
        persistentVolumeClaim:
          claimName: treomor-pvc
```

```bash
# Apply to cluster
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

6. Cloud Platforms

AWS (EC2 + RDS)

```bash
# Launch EC2 instance (Ubuntu 22.04)
# Install Docker and Docker Compose
sudo apt update && sudo apt install docker.io docker-compose -y

# Clone and run
git clone https://github.com/gitdeeper9/treomor.git
cd treomor
docker-compose up -d

# Configure RDS PostgreSQL and update .env
```

Google Cloud Run

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/treomor

# Deploy to Cloud Run
gcloud run deploy treomor \
  --image gcr.io/PROJECT_ID/treomor \
  --platform managed \
  --allow-unauthenticated \
  --port 8050
```

Heroku

```bash
# Create heroku.yml
echo "build:
  docker:
    web: Dockerfile
run:
  web: treomor-dashboard" > heroku.yml

# Deploy
heroku create treomor
heroku stack:set container
git push heroku main
```

Configuration

Environment Variables

Copy .env.example to .env and modify:

```bash
cp .env.example .env
# Edit .env with your configuration
```

Key variables:

· TREEMOR_DATA_DIR: Data storage path
· DB_HOST, DB_USER, DB_PASSWORD: PostgreSQL connection
· SENTINEL_CLIENT_ID: For InSAR data (optional)
· MAPBOX_TOKEN: For interactive maps (optional)

Database Setup

```bash
# Initialize PostgreSQL
psql -U treomor -d treomor -f database/schema.sql

# Run migrations
alembic upgrade head

# Load validation data
treomor load-data --catalog validation/847_events.h5
```

Monitoring & Logging

Prometheus Metrics

Metrics available at http://localhost:9090/metrics:

```python
# Example metrics
treomor_detections_total{type="earthquake"} 847
treomor_tssi_average{site="PNSN"} 0.73
treomor_lead_time_seconds 8.5
```

Grafana Dashboard

1. Access Grafana: http://localhost:3000 (admin/admin)
2. Add Prometheus data source: http://prometheus:9090
3. Import dashboard from grafana/dashboards/treomor.json

Logging

```bash
# Docker logs
docker logs -f treomor

# Kubernetes logs
kubectl logs -f deployment/treomor

# File logs (if configured)
tail -f /data/treomor/logs/treomor.log
```

Scaling

Horizontal Scaling

```bash
# Docker Compose scale
docker-compose up -d --scale dashboard=3

# Kubernetes horizontal autoscaling
kubectl autoscale deployment treomor --cpu-percent=70 --min=3 --max=10
```

Database Scaling

· Use TimescaleDB for time-series optimization
· Enable connection pooling with PgBouncer
· Consider read replicas for query-heavy workloads

Backup & Recovery

Backup Database

```bash
# PostgreSQL
pg_dump -U treomor treomor > backup_$(date +%Y%m%d).sql

# TimescaleDB
pg_dump -U treomor treomor_ts > backup_ts_$(date +%Y%m%d).sql

# Data volumes
tar -czf treomor_data_$(date +%Y%m%d).tar.gz /data/treomor
```

Restore

```bash
# Restore database
psql -U treomor treomor < backup_20260323.sql

# Restore data
tar -xzf treomor_data_20260323.tar.gz -C /
```

Security Hardening

SSL/TLS (Nginx)

```nginx
server {
    listen 443 ssl http2;
    server_name treomor.example.com;
    
    ssl_certificate /etc/ssl/certs/treomor.crt;
    ssl_certificate_key /etc/ssl/private/treomor.key;
    
    location / {
        proxy_pass http://dashboard:8050;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

API Authentication

```bash
# Generate JWT token
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Set in .env
JWT_SECRET_KEY=your_generated_key
```

Firewall Rules

```bash
# Allow only necessary ports
ufw allow 22/tcp    # SSH
ufw allow 443/tcp   # HTTPS
ufw allow 80/tcp    # HTTP redirect
ufw enable
```

Troubleshooting

Common Issues

1. Dashboard won't start: Check port 8050 availability
   ```bash
   lsof -i :8050
   ```
2. Database connection failed: Verify credentials
   ```bash
   psql -h localhost -U treomor -d treomor
   ```
3. Memory issues: Increase Docker memory limit
   ```bash
   docker run -m 4g treomor
   ```
4. Permission denied: Fix data directory permissions
   ```bash
   sudo chown -R 1000:1000 /data/treomor
   ```

Health Check

```bash
# Dashboard health
curl http://localhost:8050/health

# Database health
treomor db-status

# Full system check
treomor health-check --verbose
```

Performance Tuning

PostgreSQL

```sql
-- Increase shared buffers
ALTER SYSTEM SET shared_buffers = '1GB';

-- Enable query logging
ALTER SYSTEM SET log_min_duration_statement = '100ms';
```

TimescaleDB

```sql
-- Create hypertable for sensor data
SELECT create_hypertable('sensor_data', 'time');

-- Add compression policy
SELECT add_compression_policy('sensor_data', INTERVAL '7 days');
```

Python

```python
# Use multiple processes
N_JOBS = 4

# Enable caching
CACHE_SIZE_MB = 1024
```

Support

For deployment issues:

· GitHub Issues: https://github.com/gitdeeper9/treomor/issues
· Email: gitdeeper@gmail.com
· Documentation: https://treomor.readthedocs.io
