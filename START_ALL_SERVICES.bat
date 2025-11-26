@echo off
echo ========================================
echo CONSCIOUSNESS REVOLUTION - Service Launcher
echo ========================================
echo.

echo Starting services...
echo.

:: Start Onboarding API (port 5050)
start "Onboarding API" cmd /k "cd /d C:\Users\dwrek\100X_DEPLOYMENT && python ONBOARDING_API.py"

:: Start Analytics API (port 5055)
start "Analytics API" cmd /k "cd /d C:\Users\dwrek\100X_DEPLOYMENT && python ANALYTICS_API.py"

:: Start Tool Discovery API (port 5100)
start "Tool Discovery API" cmd /k "cd /d C:\Users\dwrek\100X_DEPLOYMENT && python TOOL_DISCOVERY_API.py"

echo.
echo ========================================
echo Services starting in new windows:
echo   - Onboarding API    : http://localhost:5050
echo   - Analytics API     : http://localhost:5055
echo   - Tool Discovery API: http://localhost:5100
echo ========================================
echo.

:: Wait a moment for services to start
timeout /t 3 /nobreak > nul

:: Open dashboards in browser
echo Opening dashboards...
start "" "C:\Users\dwrek\100X_DEPLOYMENT\analytics_dashboard.html"
start "" "C:\Users\dwrek\100X_DEPLOYMENT\tool_discovery.html"
start "" "C:\Users\dwrek\100X_DEPLOYMENT\onboarding.html"

echo.
echo All services launched!
echo Press any key to exit this window...
pause > nul
