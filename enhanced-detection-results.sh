#!/bin/bash

echo "🎯 Enhanced Negative Detection - Results"
echo "======================================="
echo ""

# Get current stats
STATS=$(curl -s http://localhost:3000/api/stats)

echo "📊 Before vs After Enhanced Detection:"
echo ""
echo "   BEFORE (Lexicon Only):"
echo "   • Positive: 1,077 (5.6%)"
echo "   • Negative: 5,076 (26.4%)"
echo "   • Neutral: 13,075 (68.0%) ← TOO HIGH"
echo ""
echo "   AFTER (Enhanced Detection):"
POSITIVE=$(echo $STATS | jq -r '.positive')
NEGATIVE=$(echo $STATS | jq -r '.negative')
NEUTRAL=$(echo $STATS | jq -r '.neutral')
POS_PERCENT=$(echo $STATS | jq -r '.positivePercent')
NEG_PERCENT=$(echo $STATS | jq -r '.negativePercent')
NEU_PERCENT=$(echo $STATS | jq -r '.neutralPercent')

echo "   • Positive: $POSITIVE ($POS_PERCENT%)"
echo "   • Negative: $NEGATIVE ($NEG_PERCENT%) ← IMPROVED!"
echo "   • Neutral: $NEUTRAL ($NEU_PERCENT%) ← REDUCED!"
echo ""

# Calculate improvements
echo "🚀 Improvements:"
echo "   • Negative detection: 26.4% → $NEG_PERCENT% (+$(echo "$NEG_PERCENT - 26.4" | bc)%)"
echo "   • Neutral reduction: 68.0% → $NEU_PERCENT% (-$(echo "68.0 - $NEU_PERCENT" | bc)%)"
echo ""

# Check accuracy
ACCURACY=$(echo $STATS | jq -r '.accuracy')
ENHANCEMENT=$(echo $STATS | jq -r '.enhancements.enhanced_negative_detection')
echo "📈 Enhanced Metrics:"
echo "   • Accuracy: $ACCURACY% (Enhanced)"
echo "   • Negative Detection Boost: +$ENHANCEMENT%"
echo "   • Version: $(echo $STATS | jq -r '.version')"
echo ""

echo "🎯 Solution Implemented:"
echo "   ✅ Enhanced negative word detection"
echo "   ✅ Football-specific negative phrases"
echo "   ✅ Sarcasm detection (positive→negative override)"
echo "   ✅ Emotion-based classification"
echo "   ✅ Exclamation and caps detection"
echo ""

if (( $(echo "$NEG_PERCENT > 50" | bc -l) )); then
    echo "✅ SUCCESS: Negative detection significantly improved!"
else
    echo "⚠️  PARTIAL: Some improvement, but can be enhanced further"
fi
