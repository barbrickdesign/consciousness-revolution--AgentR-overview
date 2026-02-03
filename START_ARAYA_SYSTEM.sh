#!/bin/bash
# Start complete ARAYA system (Linux/Mac)

echo "========================================"
echo "ARAYA LIVE EDITING SYSTEM"
echo "========================================"
echo ""

cd "$(dirname "$0")"

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    if [ -f ".env" ]; then
        echo "Loading .env file..."
        export $(cat .env | grep -v '^#' | xargs)
    else
        echo "WARNING: No ANTHROPIC_API_KEY found!"
        echo "Set it in .env file or environment variable"
        echo ""
    fi
fi

# Start File Writer in background
echo "[1/3] Starting File Writer (port 5001)..."
python3 ARAYA_FILE_WRITER.py &
FILE_WRITER_PID=$!
sleep 2

# Start Bridge in background
echo "[2/3] Starting ARAYA Bridge (port 5002)..."
python3 ARAYA_BRIDGE.py &
BRIDGE_PID=$!
sleep 3

# Open browser
echo "[3/3] Opening chat interface..."
if command -v xdg-open > /dev/null; then
    xdg-open araya-chat.html
elif command -v open > /dev/null; then
    open araya-chat.html
fi

echo ""
echo "========================================"
echo "SYSTEM STARTED!"
echo "========================================"
echo ""
echo "File Writer:  http://localhost:5001 (PID: $FILE_WRITER_PID)"
echo "ARAYA Bridge: http://localhost:5002 (PID: $BRIDGE_PID)"
echo "Chat UI:      araya-chat.html"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for interrupt
trap "kill $FILE_WRITER_PID $BRIDGE_PID; exit" INT
wait
