@echo off
REM SEND_WAKE_SIGNAL.bat
REM Send wake signal to another PC in Trinity network

if "%1"=="" (
    echo ========================================
    echo SEND WAKE SIGNAL
    echo ========================================
    echo.
    echo Usage: SEND_WAKE_SIGNAL.bat ^<TARGET_PC^> [TASK] [MESSAGE]
    echo.
    echo Examples:
    echo   SEND_WAKE_SIGNAL.bat PC2
    echo   SEND_WAKE_SIGNAL.bat PC2 "process_queue"
    echo   SEND_WAKE_SIGNAL.bat PC3 "autonomous_work" "Check spawn queue"
    echo.
    echo Available targets: PC1, PC2, PC3
    echo.
    exit /b 1
)

set TARGET=%1
set TASK=%~2
set MESSAGE=%~3

if "%TASK%"=="" set TASK=wake_up
if "%MESSAGE%"=="" set MESSAGE=Wake signal from %COMPUTERNAME%

echo ========================================
echo SENDING WAKE SIGNAL
echo ========================================
echo.
echo From: %COMPUTERNAME%
echo To: %TARGET%
echo Task: %TASK%
echo Message: %MESSAGE%
echo.

cd /d C:\Users\darri\100X_DEPLOYMENT

echo Sending wake signal...
python .trinity\automation\AUTO_WAKE_DAEMON.py --send %TARGET% --task "%TASK%" --message "%MESSAGE%"

if errorlevel 1 (
    echo.
    echo ERROR: Failed to send wake signal!
    exit /b 1
)

echo.
echo Wake signal created in .trinity\wake\%TARGET%.json
echo.

echo Committing to git...
git add .trinity\wake\%TARGET%.json
git commit -m "wake %TARGET%: %TASK%"

if errorlevel 1 (
    echo Note: Nothing to commit or commit failed
)

echo.
echo Pushing to remote...
git push

if errorlevel 1 (
    echo WARNING: Git push failed - wake signal may not reach %TARGET%
    echo Try: git pull, then git push
    exit /b 1
)

echo.
echo ========================================
echo WAKE SIGNAL SENT SUCCESSFULLY
echo ========================================
echo.
echo %TARGET% should wake within 30 seconds
echo Monitor: .trinity\heartbeat\%TARGET%.json
echo.
