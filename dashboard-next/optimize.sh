#!/bin/bash

echo "🚀 Optimizing Dashboard Performance..."

# Clean cache
echo "🧹 Cleaning cache..."
rm -rf .next
rm -rf node_modules/.cache

# Install dependencies with production optimizations
echo "📦 Installing optimized dependencies..."
npm ci --production=false

# Build with optimizations
echo "🔨 Building optimized version..."
NODE_ENV=production npm run build

# Analyze bundle
echo "📊 Analyzing bundle size..."
npx @next/bundle-analyzer

echo "✅ Optimization complete!"
echo "💡 Tips:"
echo "   - Use 'npm run start' for production mode"
echo "   - Enable gzip compression on your server"
echo "   - Consider using CDN for static assets"
