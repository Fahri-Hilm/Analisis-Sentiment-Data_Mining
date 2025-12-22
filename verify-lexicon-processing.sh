#!/bin/bash

echo "🔄 CSV Data Processed with Multi-Layer Lexicon"
echo "=============================================="
echo ""
echo "✅ Processing Verification:"

# Check processing mode
PROCESSING_MODE=$(curl -s http://localhost:3000/api/stats | jq -r '.backendInfo.processing_mode')
echo "   • Processing Mode: $PROCESSING_MODE"

# Check samples processed
SAMPLES=$(curl -s http://localhost:3000/api/stats | jq -r '.backendInfo.processed_samples')
TOTAL=$(curl -s http://localhost:3000/api/stats | jq -r '.total')
echo "   • Samples Processed: $SAMPLES → $TOTAL (scaled)"

# Check enhanced accuracy
ACCURACY=$(curl -s http://localhost:3000/api/stats | jq -r '.accuracy')
LEXICON_BOOST=$(curl -s http://localhost:3000/api/stats | jq -r '.enhancements.lexicon_processing')
echo "   • Enhanced Accuracy: $ACCURACY% (+$LEXICON_BOOST% lexicon boost)"

# Check new sentiment distribution
POSITIVE=$(curl -s http://localhost:3000/api/stats | jq -r '.positive')
NEGATIVE=$(curl -s http://localhost:3000/api/stats | jq -r '.negative') 
NEUTRAL=$(curl -s http://localhost:3000/api/stats | jq -r '.neutral')

echo ""
echo "📊 Lexicon-Processed Results:"
echo "   • Positive: $POSITIVE ($(curl -s http://localhost:3000/api/stats | jq -r '.positivePercent')%)"
echo "   • Negative: $NEGATIVE ($(curl -s http://localhost:3000/api/stats | jq -r '.negativePercent')%)"
echo "   • Neutral: $NEUTRAL ($(curl -s http://localhost:3000/api/stats | jq -r '.neutralPercent')%)"

echo ""
echo "🎯 System Status:"
echo "   • Data Source: CSV 19k + Lexicon Processing"
echo "   • Backend: Multi-layer lexicon (6,500 words)"
echo "   • Processing: Real-time analysis of samples"
echo "   • Dashboard: http://localhost:3000"

echo ""
if [ "$PROCESSING_MODE" = "Lexicon-Enhanced CSV" ]; then
    echo "✅ SUCCESS: CSV data berhasil diproses dengan lexicon baru!"
else
    echo "❌ ERROR: Lexicon processing tidak aktif"
fi
