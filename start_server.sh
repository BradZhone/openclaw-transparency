#!/bin/bash
# Start OpenClaw Transparency API Server

cd "$(dirname "$0")"

echo "🚀 Starting OpenClaw Transparency API Server..."
echo "📍 API: http://localhost:8000"
echo "📄 Docs: http://localhost:8000/docs"
echo "🌐 Web: http://localhost:8000/"
echo ""

# Start server
python3 -m uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
