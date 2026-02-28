@echo off
REM ============================================================
REM  Yourdio – Start Fish Speech 1.5 Narration Server
REM ============================================================
REM  Activates the fish-speech conda environment (tag v1.5.1)
REM  and launches the TTS API server on http://127.0.0.1:8080
REM
REM  Uses the firefly_gan_vq decoder (correct for fish-speech-1.5
REM  checkpoints). Runs on CUDA with half-precision (RTX 4090).
REM ============================================================

SET FISH_DIR=%~dp0fish-speech
SET API_SCRIPT=%FISH_DIR%\tools\api_server.py

echo.
echo ======================================================
echo  Yourdio Fish Speech 1.5 - Narration Server
echo  Listening on: http://127.0.0.1:8080
echo ======================================================
echo.

cd /d "%FISH_DIR%"
conda run -n fish-speech --no-capture-output python tools\api_server.py ^
    --listen 127.0.0.1:8080 ^
    --llama-checkpoint-path checkpoints\fish-speech-1.5 ^
    --decoder-checkpoint-path checkpoints\fish-speech-1.5\firefly-gan-vq-fsq-8x1024-21hz-generator.pth ^
    --decoder-config-name firefly_gan_vq ^
    --device cuda ^
    --half

pause
