@echo off
REM Start complete ARAYA system
REM 1. File Writer (port 5001)
REM 2. ARAYA Bridge (port 5002)
REM 3. Open browser to chat interface

echo ========================================
echo ARAYA LIVE EDITING SYSTEM
echo ========================================
echo.
echo Starting components...
echo.

cd /d C:\Users\dwrek\100X_DEPLOYMENT

REM Check if ANTHROPIC_API_KEY is set
if "%ANTHROPIC_API_KEY%"=="" (
    echo Checking for .env file...
    if exist .env (
        echo Found .env file
    ) else (
        echo WARNING: No ANTHROPIC_API_KEY found!
        echo Set it in .env file or environment variable
        echo.
    )
)

REM Start File Writer in new window
echo [1/3] Starting File Writer (port 5001)...
start "ARAYA File Writer" cmd /k "python ARAYA_FILE_WRITER.py"
timeout /t 2 /nobreak > nul

REM Start Bridge in new window
echo [2/3] Starting ARAYA Bridge (port 5002)...
start "ARAYA Bridge" cmd /k "python ARAYA_BRIDGE.py"
timeout /t 3 /nobreak > nul

REM Open browser
echo [3/3] Opening chat interface...
start http://localhost:5002/health
timeout /t 1 /nobreak > nul
start araya-chat.html

echo.
echo ========================================
echo SYSTEM STARTED!
echo ========================================
echo.
echo File Writer:  http://localhost:5001
echo ARAYA Bridge: http://localhost:5002
echo Chat UI:      araya-chat.html
echo.
echo Two terminal windows opened.
echo Keep them running!
echo.
pause
