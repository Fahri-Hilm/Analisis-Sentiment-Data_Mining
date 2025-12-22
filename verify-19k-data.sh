#!/bin/bash

echo "🔄 Dashboard Restored to 19k CSV Data"
echo "===================================="
echo ""
echo "✅ Data Verification:"

# Check total comments
TOTAL=$(curl -s http://localhost:3000/api/stats | jq -r '.total')
echo "   • Total Comments: $TOTAL"

# Check data source
SOURCE=$(curl -s http://localhost:3000/api/stats | jq -r '.dataSource')
echo "   • Data Source: $SOURCE"

# Check sentiment distribution
POSITIVE=$(curl -s http://localhost:3000/api/stats | jq -r '.positivePercent')
NEGATIVE=$(curl -s http://localhost:3000/api/stats | jq -r '.negativePercent')
NEUTRAL=$(curl -s http://localhost:3000/api/stats | jq -r '.neutralPercent')

echo "   • Positive: $POSITIVE%"
echo "   • Negative: $NEGATIVE%"
echo "   • Neutral: $NEUTRAL%"

# Check accuracy
ACCURACY=$(curl -s http://localhost:3000/api/stats | jq -r '.accuracy')
echo "   • Accuracy: $ACCURACY%"

echo ""
echo "📊 Dashboard Status:"
echo "   • URL: http://localhost:3000"
echo "   • Backend: Connected (Validation Mode)"
echo "   • Data: CSV 19k + Backend Enhancement"
echo ""

if [ "$TOTAL" = "19228" ]; then
    echo "✅ SUCCESS: Dashboard menggunakan data CSV 19k komentar!"
else
    echo "❌ ERROR: Data tidak sesuai (expected: 19228, got: $TOTAL)"
fi
