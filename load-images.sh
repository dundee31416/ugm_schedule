#!/bin/bash

# UGM Schedule - Load Docker Images
# This script loads Docker images from tar files on the target server

set -e

echo "========================================="
echo "UGM Schedule - Loading Docker Images"
echo "========================================="
echo ""

# Check if docker-images directory exists
if [ ! -d "docker-images" ]; then
    echo "Error: docker-images directory not found!"
    echo "Please ensure you have copied the docker-images directory to this location."
    exit 1
fi

# Load backend image
if [ -f "docker-images/ugm_schedule_backend.tar" ]; then
    echo "[1/3] Loading backend image..."
    docker load -i docker-images/ugm_schedule_backend.tar
else
    echo "Warning: ugm_schedule_backend.tar not found, skipping..."
fi

# Load frontend image
if [ -f "docker-images/ugm_schedule_frontend.tar" ]; then
    echo "[2/3] Loading frontend image..."
    docker load -i docker-images/ugm_schedule_frontend.tar
else
    echo "Warning: ugm_schedule_frontend.tar not found, skipping..."
fi

# Load postgres image
if [ -f "docker-images/postgres_14-alpine.tar" ]; then
    echo "[3/3] Loading postgres image..."
    docker load -i docker-images/postgres_14-alpine.tar
else
    echo "Warning: postgres_14-alpine.tar not found, will pull from Docker Hub when needed..."
fi

echo ""
echo "========================================="
echo "Images Loaded Successfully!"
echo "========================================="
echo ""
echo "Loaded images:"
docker images | grep -E "ugm_schedule|postgres.*14-alpine" || echo "No images found"
echo ""
echo "Next steps:"
echo "1. Create a .env file from .env.production.example"
echo "2. Edit .env with your configuration (passwords, ports, etc.)"
echo "3. Start the application:"
echo "   docker-compose -f docker-compose.prod.yml up -d"
echo ""
echo "4. Check logs:"
echo "   docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "5. Access the application:"
echo "   http://your-server-ip (or the port specified in FRONTEND_PORT)"
echo ""
