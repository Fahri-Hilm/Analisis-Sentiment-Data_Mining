#!/usr/bin/env python3
"""Run Gemini AI Sentiment Analysis API"""
import sys
from pathlib import Path
import uvicorn

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def main():
    print("🤖 Starting Gemini AI Sentiment Analysis API...")
    print("=" * 60)
    print("📍 API: http://localhost:8000")
    print("📖 Docs: http://localhost:8000/docs")
    print("🧪 Test: http://localhost:8000/test")
    print("=" * 60)
    
    from api.aggressive_api import app
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    main()
