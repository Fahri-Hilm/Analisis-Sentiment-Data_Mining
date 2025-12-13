#!/bin/bash
# Dashboard optimization script

cd dashboard-next

# Remove development dependencies
npm prune --production

# Clean build artifacts
rm -rf .next/cache
rm -rf .next/static/chunks/webpack*

# Remove unnecessary files
find node_modules -name "*.md" -delete
find node_modules -name "*.txt" -delete
find node_modules -name "test*" -type d -exec rm -rf {} + 2>/dev/null || true
find node_modules -name "example*" -type d -exec rm -rf {} + 2>/dev/null || true

echo "✅ Dashboard optimized"
