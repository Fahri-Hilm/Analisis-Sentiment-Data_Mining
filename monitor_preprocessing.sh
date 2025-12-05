#!/bin/bash
# Monitor preprocessing progress and auto-analyze when done

TARGET_FILE="data/processed/comments_clean_v3.csv"
CHECK_INTERVAL=30  # seconds

echo "Monitoring preprocessing..."
echo "Target: $TARGET_FILE"
echo "Checking every $CHECK_INTERVAL seconds"
echo ""

while true; do
    if [ -f "$TARGET_FILE" ]; then
        echo "✅ File created! Waiting for process to finish writing..."
        sleep 5
        
        # Check if process still running
        if ! pgrep -f "build_dataset.py.*v3" > /dev/null; then
            echo "✅ Process completed!"
            echo ""
            echo "Running analysis..."
            python3 src/analysis/analyze_labeling.py "$TARGET_FILE"
            break
        fi
    else
        # Show progress
        ELAPSED=$((SECONDS))
        MIN=$((ELAPSED / 60))
        SEC=$((ELAPSED % 60))
        printf "\r⏳ Waiting... [%02d:%02d] " $MIN $SEC
    fi
    
    sleep $CHECK_INTERVAL
done

echo ""
echo "Done!"
