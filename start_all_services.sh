#!/bin/bash

echo "🚀 Starting All Services for Gemini AI Dashboard"
echo "================================================"

# Kill existing processes
echo "🔄 Stopping existing services..."
pkill -f "run_gemini_api.py" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true
pkill -f "next" 2>/dev/null || true

sleep 2

# Start Gemini API
echo "🤖 Starting Gemini AI API..."
cd /home/fj/Desktop/PROJECT/Campus/DM/Analisis-Sentiment-Data_Mining
python run_gemini_api.py &
GEMINI_PID=$!

# Wait for API to start
echo "⏳ Waiting for Gemini API to start..."
sleep 5

# Check if API is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Gemini AI API is running on http://localhost:8000"
else
    echo "❌ Failed to start Gemini AI API"
    exit 1
fi

# Start Dashboard
echo "🌐 Starting Next.js Dashboard..."
cd dashboard-next
npm run dev &
DASHBOARD_PID=$!

# Wait for dashboard to start
echo "⏳ Waiting for Dashboard to start..."
sleep 10

# Check if dashboard is running
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Dashboard is running on http://localhost:3000"
else
    echo "❌ Failed to start Dashboard"
fi

echo ""
echo "🎉 All Services Started Successfully!"
echo "================================================"
echo "📍 Gemini AI API: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo "🧪 API Test: http://localhost:8000/test"
echo ""
echo "📍 Dashboard: http://localhost:3000"
echo "🔴 Live Comments: http://localhost:3000/live-comments"
echo ""
echo "💡 Tips:"
echo "- Enable 'Gemini AI' checkbox in Live Comments"
echo "- Use Video ID: lDtSjKb_8Jo for testing"
echo "- Check sentiment analysis in real-time"
echo ""
echo "🛑 To stop all services: pkill -f 'run_gemini_api.py|uvicorn|next'"

# Keep script running
wait
