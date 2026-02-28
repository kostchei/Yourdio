@echo off
REM ============================================================
REM  Yourdio - Narration Monitor
REM ============================================================
REM  Runs health checks + optional smoke synthesis checks in a loop.
REM  Logs are written to narration\monitor_logs.
REM ============================================================

SET ROOT_DIR=%~dp0

echo.
echo ======================================================
echo  Yourdio Narration Monitor
echo  Logs: narration\monitor_logs\monitor.log
echo ======================================================
echo.

cd /d "%ROOT_DIR%"
conda run -n fish-speech --no-capture-output python narration\monitor_narration.py ^
    --watch ^
    --interval-sec 30 ^
    --smoke-test

pause
