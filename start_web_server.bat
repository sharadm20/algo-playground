@echo off
echo ====================================
echo  DSA Study Plan - Web Server
echo ====================================
echo.
echo Starting web server on port 8080...
echo Open http://localhost:8080 in your browser
echo.
echo Press Ctrl+C to stop the server
echo.

cd /d "%~dp0web"
python -m http.server 8080

pause
