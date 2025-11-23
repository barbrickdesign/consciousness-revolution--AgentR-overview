@echo off
REM TEST_WAKE_CHAIN.bat
REM Test cross-computer wake chain: PC1 → PC2 → PC3

echo ========================================
echo TRINITY WAKE CHAIN TEST
echo ========================================
echo.
echo This script tests the auto-wake system
echo by sending wake signals in sequence:
echo.
echo   PC1 --wake--^> PC2 --wake--^> PC3
echo.
echo Requirements:
echo   - AUTO_WAKE_DAEMON.py running on all PCs
echo   - Git push/pull working
echo   - Tailscale network connected
echo.
echo ========================================
echo.

cd /d C:\Users\darri\100X_DEPLOYMENT

echo [1/5] Checking network connectivity...
echo.

ping -n 2 100.70.208.75 >nul
if errorlevel 1 (
    echo WARNING: PC1 not reachable
) else (
    echo   PC1: ONLINE (100.70.208.75)
)

ping -n 2 100.85.71.74 >nul
if errorlevel 1 (
    echo WARNING: PC2 not reachable
) else (
    echo   PC2: ONLINE (100.85.71.74)
)

ping -n 2 100.101.209.1 >nul
if errorlevel 1 (
    echo WARNING: PC3 not reachable
) else (
    echo   PC3: ONLINE (100.101.209.1)
)

echo.
echo [2/5] Pulling latest changes...
git pull

echo.
echo [3/5] Sending wake to PC2...
python .trinity\automation\AUTO_WAKE_DAEMON.py --send PC2 --task "wake_chain_test" --message "Wake chain test - please wake PC3 after you wake"

if errorlevel 1 (
    echo ERROR: Failed to send wake to PC2
    exit /b 1
)

echo Wake signal created for PC2
echo.

echo [4/5] Committing and pushing...
git add .trinity\wake\PC2.json
git commit -m "test: wake chain PC2"
git push

echo.
echo [5/5] Wake chain initiated!
echo.
echo ========================================
echo NEXT STEPS
echo ========================================
echo.
echo 1. Wait 30-60 seconds for PC2 to wake
echo 2. PC2 should open Claude Code automatically
echo 3. PC2 should then wake PC3
echo 4. Check results:
echo.
echo    git pull
echo    cat .trinity\heartbeat\PC2.json
echo    cat .trinity\heartbeat\PC3.json
echo.
echo 5. View wake history:
echo.
echo    ls .trinity\wake_archive\
echo.
echo ========================================
echo.
echo Monitoring wake chain...
echo Press Ctrl+C to stop monitoring
echo.

:monitor_loop
timeout /t 10 >nul
git pull >nul 2>&1

if exist .trinity\heartbeat\PC2.json (
    echo [PC2] Wake detected - checking status...
    type .trinity\heartbeat\PC2.json
    echo.
)

if exist .trinity\heartbeat\PC3.json (
    echo [PC3] Wake detected - checking status...
    type .trinity\heartbeat\PC3.json
    echo.
    echo ========================================
    echo WAKE CHAIN COMPLETE!
    echo ========================================
    exit /b 0
)

goto monitor_loop
