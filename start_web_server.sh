#!/bin/bash
echo "===================================="
echo " DSA Study Plan - Web Server"
echo "===================================="
echo ""
echo "Starting web server on port 8080..."
echo "Open http://localhost:8080 in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")/web"
python -m http.server 8080
