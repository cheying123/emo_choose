@echo off
chcp 65001 >nul
title 语音情绪识别系统 v2.0
echo ============================================
echo   语音情绪识别系统 v2.0
echo   基于 HuggingFace 预训练模型，即开即用
echo ============================================
echo.

REM 设置 HuggingFace 国内镜像（中国用户加速）
set HF_ENDPOINT=https://hf-mirror.com

REM 检查 Python
where python >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python！
    echo 请先安装 Python 3.8+，下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查依赖
echo [检查] 正在验证依赖...
python -c "import torch, transformers, librosa" >nul 2>&1
if errorlevel 1 (
    echo [提示] 首次运行需要安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败，请手动运行: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

echo [启动] 正在启动图形界面...
echo [提示] 首次启动会自动下载模型（约 1.5GB），请耐心等待
echo.
start /B python gui_app.py
exit
