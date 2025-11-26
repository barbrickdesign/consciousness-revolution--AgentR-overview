@echo off
echo ================================================================
echo    CYCLOTRON GO-LIVE - Single Click Launch
echo    Trinity Validated: C1 (Build), C2 (Review), C3 (Approve)
echo ================================================================
echo.

:: Set environment
cd /d C:\Users\dwrek\100X_DEPLOYMENT
set CONSCIOUSNESS_HOME=C:\Users\dwrek\.consciousness

echo [1/5] Starting Cyclotron Search APIs...
start /B python CYCLOTRON_SEARCH.py
start /B python CYCLOTRON_SEARCH_V2.py
echo       Port 6668: Filename search
echo       Port 6669: Content search
echo.

echo [2/5] Starting Cyclotron Nerve Center...
start "Nerve Center" cmd /k "cd /d %CONSCIOUSNESS_HOME% && python CYCLOTRON_NERVE_CENTER.py --agent C1-NerveCenter"
echo       Sensory system active
echo.

echo [3/5] Starting Brain Agent Framework...
start "Brain Agents" cmd /k "cd /d %CONSCIOUSNESS_HOME% && python BRAIN_AGENT_FRAMEWORK.py"
echo       6 AI brain agents online
echo.

echo [4/5] Starting Cyclotron Sync (Dropbox)...
start /B python %CONSCIOUSNESS_HOME%\CYCLOTRON_SYNC.py
echo       Dropbox persistence enabled
echo.

echo [5/5] Starting Trinity Hub Monitor...
start "Hub Monitor" cmd /k "cd /d %CONSCIOUSNESS_HOME%\hub && python -c \"import time; import json; from pathlib import Path; [print(f'Hub Status: {len(list(Path(\".\").glob(\"*.json\")))} files') or time.sleep(30) for _ in iter(int, 1)]\""
echo       Hub file system monitoring
echo.

echo ================================================================
echo    CYCLOTRON GO-LIVE COMPLETE
echo ================================================================
echo.
echo Active Services:
echo   - Cyclotron Search APIs (6668, 6669)
echo   - Nerve Center (sensors active)
echo   - Brain Agents (6 AI processors)
echo   - Sync System (Dropbox backup)
echo   - Hub Monitor (Trinity coordination)
echo.
echo Check Status:
echo   - Hub: C:\Users\dwrek\.consciousness\hub\
echo   - Logs: C:\Users\dwrek\.consciousness\nerve_center.log
echo   - Atoms: C:\Users\dwrek\.consciousness\cyclotron_core\atoms\
echo.
echo Press any key to exit this launcher (services keep running)...
pause > nul
