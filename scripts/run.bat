@echo off
echo ==============================================
echo Starting GCRIN System
echo ==============================================

echo Starting Backend API and Scheduler...
start cmd /k "cd backend && call venv\Scripts\activate.bat && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo Starting Frontend Dashboard...
start cmd /k "cd frontend && npm run dev"

echo System is running!
echo Backend API: http://localhost:8000/docs
echo Frontend Dashboard: http://localhost:3000
