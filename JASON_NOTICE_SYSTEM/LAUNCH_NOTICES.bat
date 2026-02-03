@echo off
echo ============================================================
echo JASON NOTICE DISTRIBUTION SYSTEM
echo ============================================================
echo.
echo Commands:
echo   1. Initialize database
echo   2. Scrape emails
echo   3. Test email
echo   4. Dry run (preview)
echo   5. SEND NOTICES (live)
echo   6. Check status
echo   7. Open tracker dashboard
echo.
set /p choice="Enter choice (1-7): "

cd /d "C:\Users\dwrek\100X_DEPLOYMENT\JASON_NOTICE_SYSTEM"

if "%choice%"=="1" (
    echo.
    echo Initializing database...
    python diocese_database.py
    pause
)

if "%choice%"=="2" (
    echo.
    echo Scraping emails...
    python email_scraper.py
    pause
)

if "%choice%"=="3" (
    echo.
    echo Sending test email...
    python mass_email_sender.py test
    pause
)

if "%choice%"=="4" (
    echo.
    echo Running dry-run preview...
    python mass_email_sender.py dry-run
    pause
)

if "%choice%"=="5" (
    echo.
    echo *** LIVE SEND MODE ***
    echo This will send actual emails to Catholic dioceses!
    echo.
    python mass_email_sender.py send
    pause
)

if "%choice%"=="6" (
    echo.
    echo Checking status...
    python mass_email_sender.py status
    pause
)

if "%choice%"=="7" (
    echo.
    echo Opening tracker dashboard...
    start tracker.html
)

echo.
echo Done.
