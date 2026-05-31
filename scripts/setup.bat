@echo off
echo ==============================================
echo GCRIN Initial Setup
echo ==============================================

echo [1/3] Setting up Python Backend Environment...
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
python -m spacy download en_core_web_sm
cd ..

echo.
echo [2/3] Setting up Node.js Frontend Environment...
cd frontend
npm install
cd ..

echo.
echo [3/3] Database Initialization
echo Ensure PostgreSQL is running locally on port 5432.
echo The backend will automatically create the database and tables on startup.

echo.
echo Setup Complete!
echo Run 'scripts\run.bat' to start the application.
