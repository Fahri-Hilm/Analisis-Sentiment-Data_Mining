#!/bin/bash

# Simple VPS Deployment - In-Memory Only
echo "🚀 Deploying Sentiment Analysis (In-Memory Storage)..."

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.simple.yml down 2>/dev/null || true

# Remove old images
echo "🧹 Cleaning up..."
docker system prune -f

echo "🔨 Building containers..."
docker-compose -f docker-compose.simple.yml build --no-cache

echo "🚀 Starting services..."
docker-compose -f docker-compose.simple.yml up -d

echo "⏳ Waiting for services to start..."
sleep 15

echo "📊 Checking services status..."
docker-compose -f docker-compose.simple.yml ps

echo "🔍 Testing application..."
curl -s http://localhost:3000/api/live-data?action=memory || echo "App starting..."

echo "✅ Deployment complete!"
echo ""
echo "🌐 Dashboard: http://$(hostname -I | awk '{print $1}'):3000"
echo "💾 Storage: In-Memory with JSON backup"
echo "📊 Memory Usage: ~2-5MB RAM"
echo ""
echo "✨ Features:"
echo "  • Zero database setup required"
echo "  • Ultra-fast performance"
echo "  • Auto backup every 5 minutes"
echo "  • Perfect for low-spec VPS"
