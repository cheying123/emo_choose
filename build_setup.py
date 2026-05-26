"""
编译安装程序
"""
import os
import sys
import subprocess

# 确保 PyInstaller 安装
try:
    import PyInstaller
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

# 编译 setup.py 为独立 EXE
# 注意：不把 dist/ 打包进 exe，而是安装时从同级目录读取
cmd = [
    sys.executable, "-m", "PyInstaller",
    "setup.py",
    "--name=语音情绪识别系统_安装程序",
    "--onefile",
    "--windowed",
    "--add-data=setup.py;.",
    "--clean",
    "--noconfirm",
]

print("编译安装程序...")
subprocess.check_call(cmd)
print("\n[OK] 安装程序生成成功!")
print(f"  位置: dist/语音情绪识别系统_安装程序.exe")
print(f"\n使用方法:")
print(f"  1. 把安装程序放到 dist/ 同级目录")
print(f"  2. 双击运行即可安装到系统")
