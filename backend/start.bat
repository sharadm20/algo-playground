@echo off
echo Starting DSA Code Runner backend...
cd /d "%~dp0"
uvicorn backend.main:app --host 127.0.0.1 --port 8001 --reload
