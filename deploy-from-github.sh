#!/bin/bash

REPO_URL="https://github.com/Fahri-Hilm/Analisis-Sentiment-Data_Mining.git"

echo "🚀 Deploying from GitHub..."

# Install Docker if not exists
if ! command -v docker &> /dev/null; then
    echo "📦 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
fi

# Install Docker Compose if not exists
if ! command -v docker-compose &> /dev/null; then
    echo "📦 Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Clone or pull latest
if [ -d "sentiment-project" ]; then
    echo "📥 Updating existing project..."
    cd sentiment-project
    git pull origin main
else
    echo "📥 Cloning project..."
    git clone $REPO_URL sentiment-project
    cd sentiment-project
fi

# Build and run
echo "🔨 Building and starting containers..."
docker-compose down
docker-compose build --no-cache
docker-compose up -d

echo "✅ Deployment complete!"
echo "🌐 Dashboard: http://$(curl -s ifconfig.me)"
echo "🔍 API: http://$(curl -s ifconfig.me)/api/predict"

# Show logs
docker-compose logs -f
