#!/bin/bash

echo "🚀 Starting Complete Multi-Layer Timnas Sentiment Analysis System"
echo "=================================================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Start Backend API
echo "🔧 Starting Multi-Layer API Server..."
cd "$(dirname "$0")"

# Install Python dependencies if needed
if [ ! -f "requirements_installed.flag" ]; then
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
    touch requirements_installed.flag
fi

# Start API server in background
python run_gemini_api.py &
API_PID=$!
echo "✅ API Server started (PID: $API_PID)"
echo "📍 API: http://localhost:8000"
echo "📖 Docs: http://localhost:8000/docs"
echo ""

# Wait for API to be ready
echo "⏳ Waiting for API to be ready..."
sleep 5

# Test API health
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ API is healthy and ready"
else
    echo "❌ API failed to start properly"
    kill $API_PID 2>/dev/null
    exit 1
fi

# Start Frontend Dashboard
echo ""
echo "🎨 Starting Dashboard..."
cd dashboard-next

# Install Node dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Start dashboard in background
npm run dev &
DASHBOARD_PID=$!
echo "✅ Dashboard started (PID: $DASHBOARD_PID)"
echo "📍 Dashboard: http://localhost:3000"
echo ""

# Wait for dashboard to be ready
echo "⏳ Waiting for dashboard to be ready..."
sleep 10

echo "🎉 SYSTEM READY!"
echo "=================================================================="
echo "📊 Multi-Layer Sentiment Analysis System v10.0"
echo ""
echo "🔗 Access Points:"
echo "   • Dashboard: http://localhost:3000"
echo "   • Live Analysis: http://localhost:3000/realtime"
echo "   • API: http://localhost:8000"
echo "   • API Docs: http://localhost:8000/docs"
echo ""
echo "🧠 Analysis Layers:"
echo "   • Layer 1: Core Sentiment (1,500 words)"
echo "   • Layer 2: Basic Emotions (2,000 words)"
echo "   • Layer 3: Football-Specific (3,000 words)"
echo "   • Total: 6,500 words lexicon"
echo ""
echo "⚡ Features:"
echo "   • Real-time YouTube comment analysis"
echo "   • Multi-layer sentiment detection"
echo "   • Football-specific emotion recognition"
echo "   • Indonesian slang support"
echo "   • Interactive dashboard"
echo ""
echo "Press Ctrl+C to stop all services"
echo "=================================================================="

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill $API_PID 2>/dev/null
    kill $DASHBOARD_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Keep script running
while true; do
    sleep 1
done
