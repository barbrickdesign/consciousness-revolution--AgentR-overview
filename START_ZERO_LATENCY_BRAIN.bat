@echo off
echo ================================================================
echo    ZERO-LATENCY BRAIN SYSTEM LAUNCHER
echo    Cyclotron + FAST_HUB + Ollama Warm Keeper
echo ================================================================
echo.

cd /d C:\Users\dwrek\.consciousness

echo [1/3] Starting Ollama Warm Keeper...
start "Ollama Warm Keeper" cmd /k "python OLLAMA_WARM_KEEPER.py"
timeout /t 2 >nul

echo [2/3] Starting Fast Nerve Center...
start "Fast Nerve Center" cmd /k "python NERVE_CENTER_FAST.py --instance C3-NerveCenter"
timeout /t 2 >nul

echo [3/3] Running FAST_HUB benchmark...
python FAST_HUB.py

echo.
echo ================================================================
echo    ZERO-LATENCY BRAIN ACTIVE
echo ================================================================
echo.
echo Windows open:
echo   - Ollama Warm Keeper: Keeps LLMs ready (~2s response)
echo   - Fast Nerve Center: Sub-5ms cycle time
echo.
echo Performance targets:
echo   - Wake signal: <0.1ms (was 100ms)
echo   - Memory lookup: <1ms (was 20ms)
echo   - Event cycle: <5ms (was 500ms)
echo.
echo Press any key to exit this window (workers keep running)...
pause >nul
