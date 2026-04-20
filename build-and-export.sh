#!/bin/bash

# UGM Schedule - Build and Export Docker Images
# This script builds production images and saves them to tar files for transfer

set -e

echo "========================================="
echo "UGM Schedule - Building Docker Images"
echo "========================================="
echo ""

# Create output directory for tar files
mkdir -p docker-images

# Build backend image
echo "[1/2] Building backend image..."
docker build -t ugm_schedule_backend:latest ./backend

# Build frontend image (production target)
echo "[2/2] Building frontend image..."
docker build -t ugm_schedule_frontend:latest --target production ./frontend

echo ""
echo "========================================="
echo "Exporting Images to Tar Files"
echo "========================================="
echo ""

# Save backend image
echo "Exporting backend image..."
docker save ugm_schedule_backend:latest -o docker-images/ugm_schedule_backend.tar

# Save frontend image
echo "Exporting frontend image..."
docker save ugm_schedule_frontend:latest -o docker-images/ugm_schedule_frontend.tar

# Save postgres image (optional - can be pulled on target server)
echo "Exporting postgres image..."
docker pull postgres:14-alpine
docker save postgres:14-alpine -o docker-images/postgres_14-alpine.tar

echo ""
echo "========================================="
echo "Build Complete!"
echo "========================================="
echo ""
echo "Docker images have been saved to the 'docker-images' directory:"
echo "  - ugm_schedule_backend.tar"
echo "  - ugm_schedule_frontend.tar"
echo "  - postgres_14-alpine.tar"
echo ""
echo "Total size:"
du -h docker-images/*.tar | awk '{print "  - " $2 ": " $1}'
echo ""
echo "Next steps:"
echo "1. Copy the 'docker-images' directory to your target server"
echo "2. Copy docker-compose.prod.yml to your target server"
echo "3. Create a .env file from .env.production.example"
echo "4. Run the load-images script on the target server"
echo "5. Start the application with: docker-compose -f docker-compose.prod.yml up -d"
echo ""
