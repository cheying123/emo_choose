@echo off
chcp 65001 >nul
title 语音情绪识别系统 v2.0
echo ============================================
echo   语音情绪识别系统 v2.0 - Web 版
echo   浏览器打开 http://localhost:5000
echo ============================================
echo.

set HF_ENDPOINT=https://hf-mirror.com
python web_app.py

pause
