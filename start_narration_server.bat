@echo off
REM ============================================================
REM  Yourdio – Start Fish Speech 1.5 Narration Server
REM ============================================================
REM  Activates the fish-speech conda environment and launches
REM  the TTS API server on http://127.0.0.1:8080
REM ============================================================

SET FISH_DIR=%~dp0fish-speech
SET LLAMA_CKPT=%FISH_DIR%\checkpoints\fish-speech-1.5\model.pth
SET DECODER_CKPT=%FISH_DIR%\checkpoints\fish-speech-1.5\firefly-gan-vq-fsq-8x1024-21hz-generator.pth
SET API_SCRIPT=%FISH_DIR%\tools\api_server.py

echo.
echo ======================================================
echo  Yourdio Fish Speech 1.5 - Narration Server
echo  Listening on: http://127.0.0.1:8080
echo ======================================================
echo.

conda run -n fish-speech --no-capture-output python "%API_SCRIPT%" ^
    --listen 127.0.0.1:8080 ^
    --llama-checkpoint-path "%LLAMA_CKPT%" ^
    --decoder-checkpoint-path "%DECODER_CKPT%" ^
    --device cuda ^
    --half

pause
