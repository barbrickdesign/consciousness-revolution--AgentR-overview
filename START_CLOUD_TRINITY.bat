@echo off
echo ================================================================
echo    CLOUD TRINITY WORKERS - API-Based Background Processing
echo ================================================================
echo.

:: Check for API key
if "%ANTHROPIC_API_KEY%"=="" (
    echo [ERROR] ANTHROPIC_API_KEY not set!
    echo.
    echo Set it with: set ANTHROPIC_API_KEY=sk-ant-...
    echo Or permanently: setx ANTHROPIC_API_KEY "sk-ant-..."
    echo.
    pause
    exit /b 1
)

echo API Key: [SET]
echo.
echo Available Cloud Workers:
echo   C1-Cloud (Mechanic) - Code, fixes, builds
echo   C2-Cloud (Architect) - Design, planning
echo   C3-Cloud (Oracle) - Research, patterns
echo.
echo Models:
echo   1. claude-haiku-4-5-20251101 (fast, cheap)
echo   2. claude-sonnet-4-20250514 (balanced, default)
echo   3. claude-opus-4-5-20251101 (powerful)
echo.

set /p CHOICE="Select action (1=Start C1, 2=Start C2, 3=Start C3, A=All, T=Test): "

cd /d C:\Users\dwrek\.consciousness

if /i "%CHOICE%"=="1" (
    echo Starting C1-Cloud (Mechanic)...
    python CLOUD_TRINITY_WORKER.py --instance C1-Cloud --model claude-sonnet-4-20250514
) else if /i "%CHOICE%"=="2" (
    echo Starting C2-Cloud (Architect)...
    python CLOUD_TRINITY_WORKER.py --instance C2-Cloud --model claude-sonnet-4-20250514
) else if /i "%CHOICE%"=="3" (
    echo Starting C3-Cloud (Oracle)...
    python CLOUD_TRINITY_WORKER.py --instance C3-Cloud --model claude-sonnet-4-20250514
) else if /i "%CHOICE%"=="A" (
    echo Starting ALL Cloud Workers...
    start "C1-Cloud" cmd /k "cd /d C:\Users\dwrek\.consciousness && python CLOUD_TRINITY_WORKER.py --instance C1-Cloud"
    start "C2-Cloud" cmd /k "cd /d C:\Users\dwrek\.consciousness && python CLOUD_TRINITY_WORKER.py --instance C2-Cloud"
    start "C3-Cloud" cmd /k "cd /d C:\Users\dwrek\.consciousness && python CLOUD_TRINITY_WORKER.py --instance C3-Cloud"
    echo.
    echo All workers started in separate windows!
) else if /i "%CHOICE%"=="T" (
    echo Creating test task...
    python CLOUD_TRINITY_WORKER.py --test
) else (
    echo Invalid choice
)

echo.
pause
