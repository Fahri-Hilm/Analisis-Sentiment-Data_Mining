#!/bin/bash

# VPS Deployment Script
echo "🚀 Deploying Sentiment Analysis to VPS..."

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "❌ .env.production not found!"
    echo "📝 Creating template..."
    cat > .env.production << EOF
# Production Environment Variables
DB_PASSWORD=change_this_password_123
DATABASE_URL=postgresql://admin:change_this_password_123@postgres:5432/sentiment_analysis
NODE_ENV=production
NEXTAUTH_SECRET=change_this_secret_key
YOUTUBE_API_KEY=your_youtube_api_key_here
EOF
    echo "✅ Please edit .env.production with your actual values"
    exit 1
fi

# Build and deploy
echo "🔨 Building containers..."
docker-compose -f docker-compose.yml build

echo "🚀 Starting services..."
docker-compose -f docker-compose.yml up -d

echo "⏳ Waiting for database..."
sleep 10

echo "📊 Checking services..."
docker-compose ps

echo "✅ Deployment complete!"
echo "🌐 Access your app at: http://your-vps-ip"
echo "📊 Database: PostgreSQL running on port 5432"
