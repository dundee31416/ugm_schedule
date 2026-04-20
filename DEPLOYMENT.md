# UGM Schedule - Deployment Guide

This guide explains how to build Docker images and deploy the UGM Schedule application on another server.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Building Images (Source Server)](#building-images-source-server)
3. [Transferring to Target Server](#transferring-to-target-server)
4. [Loading and Running (Target Server)](#loading-and-running-target-server)
5. [Configuration](#configuration)
6. [Maintenance](#maintenance)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### Source Server (Where you build images)
- Docker installed
- Git (to clone the repository)
- Sufficient disk space (~2-3 GB for images)

### Target Server (Where you deploy)
- Docker installed
- Docker Compose installed
- Sufficient disk space (~2-3 GB for images + database)
- Open ports: 80 (frontend), 8000 (backend), 5432 (postgres - optional if not exposing externally)

## Building Images (Source Server)

### Step 1: Build and Export Images

On your development machine or build server:

**Linux/Mac:**
```bash
chmod +x build-and-export.sh
./build-and-export.sh
```

**Windows:**
```cmd
build-and-export.bat
```

This script will:
1. Build the backend Docker image
2. Build the frontend Docker image (production mode with nginx)
3. Pull and save the PostgreSQL image
4. Export all images to `docker-images/` directory as .tar files

### Step 2: Verify Build

Check that the following files were created in the `docker-images/` directory:
- `ugm_schedule_backend.tar` (~500-800 MB)
- `ugm_schedule_frontend.tar` (~50-100 MB)
- `postgres_14-alpine.tar` (~200 MB)

## Transferring to Target Server

### Option 1: Using SCP (Linux/Mac to Linux Server)

```bash
# Create a deployment package
tar -czf ugm_schedule_deployment.tar.gz \
    docker-images/ \
    docker-compose.prod.yml \
    .env.production.example \
    load-images.sh

# Copy to target server
scp ugm_schedule_deployment.tar.gz user@target-server:/path/to/deployment/

# On target server
ssh user@target-server
cd /path/to/deployment/
tar -xzf ugm_schedule_deployment.tar.gz
```

### Option 2: Using USB Drive or Network Share

1. Copy these files/folders to your transfer medium:
   - `docker-images/` (entire directory)
   - `docker-compose.prod.yml`
   - `.env.production.example`
   - `load-images.sh` (Linux/Mac) or `load-images.bat` (Windows)

2. Transfer to target server

### Option 3: Cloud Storage

Upload the deployment package to cloud storage (Google Drive, Dropbox, etc.) and download on target server.

## Loading and Running (Target Server)

### Step 1: Load Docker Images

**Linux/Mac:**
```bash
chmod +x load-images.sh
./load-images.sh
```

**Windows:**
```cmd
load-images.bat
```

### Step 2: Configure Environment

Create your production environment file:

```bash
# Copy the example file
cp .env.production.example .env

# Edit with your settings
nano .env  # or vim, or any text editor
```

**Important settings to configure:**

```env
# Change this to a strong password!
POSTGRES_PASSWORD=your_secure_password_here

# If using a different port for frontend
FRONTEND_PORT=80

# Add your domain/IP for CORS
CORS_ORIGINS=http://your-domain.com,http://your-server-ip

# Optional: TopScore API credentials (only if you need to sync data)
TOPSCORE_CLIENT_ID=your_client_id
TOPSCORE_CLIENT_SECRET=your_client_secret
TOPSCORE_CSRF_TOKEN=your_csrf_token
```

### Step 3: Start the Application

```bash
# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Check that all services are running
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Step 4: Verify Deployment

1. **Check frontend**: Open browser to `http://your-server-ip`
2. **Check backend API**: `http://your-server-ip:8000/api/v1/health`
3. **Check database**: `docker-compose -f docker-compose.prod.yml exec postgres psql -U ugm_schedule -c '\dt'`

### Step 5: Initial Database Setup

The database will be automatically initialized when the backend starts. If you need to sync data:

```bash
# Access the backend container
docker-compose -f docker-compose.prod.yml exec backend bash

# Inside the container, you can run Python scripts to sync data
# For example:
python -m src.scripts.sync_events
```

## Configuration

### Port Configuration

By default:
- **Frontend**: Port 80
- **Backend**: Port 8000
- **PostgreSQL**: Port 5432

To change ports, edit the `.env` file:

```env
FRONTEND_PORT=8080
BACKEND_PORT=8001
POSTGRES_PORT=5433
```

### CORS Configuration

If accessing from different domains, update CORS settings:

```env
CORS_ORIGINS=http://localhost,http://app.example.com,http://192.168.1.100
```

### Database Persistence

Data is stored in a Docker volume named `postgres_data`. This persists even if containers are removed.

To backup the database:

```bash
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U ugm_schedule ugm_schedule > backup.sql
```

To restore:

```bash
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U ugm_schedule ugm_schedule < backup.sql
```

## Maintenance

### Viewing Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
docker-compose -f docker-compose.prod.yml logs -f postgres
```

### Restarting Services

```bash
# Restart all services
docker-compose -f docker-compose.prod.yml restart

# Restart specific service
docker-compose -f docker-compose.prod.yml restart backend
```

### Stopping the Application

```bash
# Stop all services (keeps data)
docker-compose -f docker-compose.prod.yml down

# Stop and remove volumes (deletes data!)
docker-compose -f docker-compose.prod.yml down -v
```

### Updating the Application

1. Build new images on source server
2. Export and transfer to target server
3. Load new images
4. Restart services:

```bash
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Frontend shows "Cannot connect to backend"

**Check backend is running:**
```bash
docker-compose -f docker-compose.prod.yml ps backend
docker-compose -f docker-compose.prod.yml logs backend
```

**Check CORS configuration** in `.env` file

**Test backend directly:**
```bash
curl http://localhost:8000/api/v1/health
```

### Database connection errors

**Check postgres is healthy:**
```bash
docker-compose -f docker-compose.prod.yml ps postgres
```

**Check connection string** in `.env` matches postgres settings

**View postgres logs:**
```bash
docker-compose -f docker-compose.prod.yml logs postgres
```

### Port already in use

Change the port in `.env`:
```env
FRONTEND_PORT=8080  # Instead of 80
BACKEND_PORT=8001   # Instead of 8000
```

Then restart:
```bash
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

### Out of disk space

**Check Docker disk usage:**
```bash
docker system df
```

**Clean up unused images and containers:**
```bash
docker system prune -a
```

**Note:** This will remove all unused images, so you may need to reload your application images.

### Images fail to load

**Verify tar files exist and aren't corrupted:**
```bash
ls -lh docker-images/
tar -tzf docker-images/ugm_schedule_backend.tar | head
```

**Try loading manually:**
```bash
docker load -i docker-images/ugm_schedule_backend.tar
docker load -i docker-images/ugm_schedule_frontend.tar
docker load -i docker-images/postgres_14-alpine.tar
```

## Production Best Practices

1. **Use strong passwords** - Change all default passwords in `.env`
2. **Regular backups** - Schedule automatic database backups
3. **Monitor logs** - Set up log rotation and monitoring
4. **HTTPS/SSL** - Use a reverse proxy (nginx, Caddy, Traefik) with SSL certificates
5. **Firewall** - Only expose necessary ports (80/443 for web, close 5432 if not needed externally)
6. **Resource limits** - Set memory/CPU limits in docker-compose.prod.yml if needed
7. **Updates** - Keep Docker and OS updated with security patches

## Support

For issues or questions:
- Check logs: `docker-compose -f docker-compose.prod.yml logs -f`
- Review this documentation
- Check Docker and system resources
- Verify network connectivity and firewall rules
