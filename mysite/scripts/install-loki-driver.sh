#!/bin/bash

# Script to install Grafana Loki Docker logging driver
# For Mac and Linux users

echo "Installing Grafana Loki Docker logging driver..."

# Check if Docker is running
if ! docker ps > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Check if plugin is already installed
if docker plugin ls | grep -q "grafana/loki"; then
    echo "Grafana Loki driver is already installed."
    exit 0
fi

# Install the plugin
echo "Installing plugin..."
docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions

if [ $? -eq 0 ]; then
    echo "✓ Grafana Loki driver installed successfully!"
    docker plugin ls | grep loki
else
    echo "✗ Failed to install Grafana Loki driver."
    exit 1
fi

echo ""
echo "Next steps:"
echo "1. cd mysite/"
echo "2. docker-compose up --build"
echo "3. Access Grafana at http://localhost:3000"
