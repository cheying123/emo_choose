"""
语音情绪识别系统 v2.0 - 安装程序
把 EXE 安装到系统，创建桌面快捷方式 + 开始菜单 + 卸载入口
编译: python build_setup.py
"""
import os
import sys
import shutil
import subprocess
import json
from pathlib import Path

APP_NAME = "语音情绪识别系统"
APP_VERSION = "2.0.0"
COMPANY = "EmoChoose"

# 安装路径
INSTALL_DIR = os.path.join(os.environ.get("LOCALAPPDATA", "C:\\Users\\Default"), APP_NAME)
DESKTOP_DIR = os.path.join(os.environ["USERPROFILE"], "Desktop")
STARTMENU_DIR = os.path.join(
    os.environ["APPDATA"],
    "Microsoft\\Windows\\Start Menu\\Programs", APP_NAME,
)

HERE = Path(__file__).parent

# 安装程序所在目录（处理被移动的情况）
_EXE_DIR = Path(sys.executable).parent if getattr(sys, 'frozen', False) else HERE


def _find_app_dir():
    """查找 EXE 程序所在目录"""
    candidates = [
        _EXE_DIR / APP_NAME,
        _EXE_DIR / "dist" / APP_NAME,
        HERE / APP_NAME,
        HERE / "dist" / APP_NAME,
    ]
    for p in candidates:
        if (p / f"{APP_NAME}.exe").exists():
            return p
    return None


def install():
    """执行安装"""
    print(f"{APP_NAME} v{APP_VERSION} - 安装程序")
    print("=" * 50)

    # 找到 EXE 源目录
    app_dir = _find_app_dir()
    if not app_dir:
        print("[FAIL] 找不到应用文件")
        print(f"  请把安装程序放在「{APP_NAME}」文件夹旁边")
        print(f"  目录结构:")
        print(f"    {APP_NAME}/")
        print(f"      {APP_NAME}.exe")
        print(f"      ...")
        print(f"    {APP_NAME}_安装程序.exe")
        input("\n按回车键退出...")
        return False

    src_exe = app_dir / f"{APP_NAME}.exe"
    src_dir = app_dir

    print(f"\n源文件: {src_dir}")
    print(f"安装目标: {INSTALL_DIR}")

    # 1. 复制文件
    print("\n[1/4] 复制程序文件...")
    if os.path.exists(INSTALL_DIR):
        shutil.rmtree(INSTALL_DIR)
    shutil.copytree(src_dir, INSTALL_DIR)
    print(f"  ✓ 已安装到: {INSTALL_DIR}")

    # 2. 创建桌面快捷方式
    print("\n[2/4] 创建桌面快捷方式...")
    _create_shortcut(
        os.path.join(DESKTOP_DIR, f"{APP_NAME}.lnk"),
        os.path.join(INSTALL_DIR, f"{APP_NAME}.exe"),
        "基于深度学习的多语种语音情绪识别系统",
    )
    print(f"  ✓ 桌面快捷方式已创建")

    # 3. 创建开始菜单
    print("\n[3/4] 创建开始菜单...")
    os.makedirs(STARTMENU_DIR, exist_ok=True)
    _create_shortcut(
        os.path.join(STARTMENU_DIR, f"{APP_NAME}.lnk"),
        os.path.join(INSTALL_DIR, f"{APP_NAME}.exe"),
    )
    _create_shortcut(
        os.path.join(STARTMENU_DIR, "卸载.lnk"),
        os.path.join(INSTALL_DIR, "卸载.exe") if False else _create_uninstall_script(),
    )
    print(f"  ✓ 开始菜单已创建")

    # 4. 注册卸载信息
    print("\n[4/4] 注册卸载信息...")
    _register_uninstall()
    print(f"  ✓ 已添加到「控制面板 → 程序和功能」")

    print("\n" + "=" * 50)
    print("安装完成！")
    print(f"  桌面快捷方式: {DESKTOP_DIR}\\{APP_NAME}.lnk")
    print(f"  安装位置: {INSTALL_DIR}")
    print(f"\n首次启动会自动安装 PyTorch（约 2GB）+ 下载模型（约 1.5GB）")
    print("=" * 50)
    input("\n按回车键退出...")
    return True


def uninstall():
    """执行卸载"""
    print(f"正在卸载 {APP_NAME}...")

    # 删除安装目录
    if os.path.exists(INSTALL_DIR):
        shutil.rmtree(INSTALL_DIR)
        print(f"  ✓ 已删除: {INSTALL_DIR}")

    # 删除桌面快捷方式
    desktop_lnk = os.path.join(DESKTOP_DIR, f"{APP_NAME}.lnk")
    if os.path.exists(desktop_lnk):
        os.remove(desktop_lnk)
        print(f"  ✓ 已删除桌面快捷方式")

    # 删除开始菜单
    if os.path.exists(STARTMENU_DIR):
        shutil.rmtree(STARTMENU_DIR)
        print(f"  ✓ 已删除开始菜单")

    # 删除卸载信息
    _unregister_uninstall()

    # 删除 HuggingFace 模型缓存
    hf_cache = os.path.join(
        os.environ.get("HF_HOME", os.path.join(os.environ["USERPROFILE"], ".cache", "huggingface")),
        "hub",
    )
    if os.path.exists(hf_cache):
        shutil.rmtree(hf_cache, ignore_errors=True)
        print(f"  ✓ 已清理模型缓存")

    print(f"\n卸载完成。")
    input("\n按回车键退出...")


def _create_shortcut(lnk_path, target_path, description=""):
    """用 VBS 创建 Windows 快捷方式"""
    vbs_content = f'''
Set WshShell = CreateObject("WScript.Shell")
Set Shortcut = WshShell.CreateShortcut("{lnk_path}")
Shortcut.TargetPath = "{target_path}"
Shortcut.WorkingDirectory = "{os.path.dirname(target_path)}"
Shortcut.Description = "{description or APP_NAME}"
Shortcut.WindowStyle = 1
Shortcut.Save
'''
    vbs_path = os.path.join(os.environ["TEMP"], "create_shortcut.vbs")
    with open(vbs_path, "w", encoding="utf-8") as f:
        f.write(vbs_content)
    subprocess.run(["cscript", "//nologo", vbs_path], capture_output=True, timeout=10)
    os.remove(vbs_path)


def _create_uninstall_script():
    """创建卸载脚本"""
    uninstall_path = os.path.join(INSTALL_DIR, "卸载.bat")
    bat_content = f'''@echo off
chcp 65001 >nul
title 卸载 {APP_NAME}
echo 正在卸载 {APP_NAME}...
python -c "
import subprocess, sys
subprocess.run([sys.executable, '-m', 'pip', 'uninstall', '-y', 'torch', 'transformers', 'librosa'])
"
rmdir /s /q "{INSTALL_DIR}"
reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{APP_NAME}" /f
echo 卸载完成！
pause
'''
    with open(uninstall_path, "w", encoding="utf-8") as f:
        f.write(bat_content)
    return uninstall_path


def _register_uninstall():
    """注册卸载信息到注册表"""
    uninstall_key = (
        f"HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{APP_NAME}"
    )
    install_date = subprocess.run(
        ["powershell", "-Command", "Get-Date -Format yyyyMMdd"],
        capture_output=True, text=True, timeout=5,
    ).stdout.strip()

    reg_entries = {
        "DisplayName": APP_NAME,
        "DisplayVersion": APP_VERSION,
        "Publisher": COMPANY,
        "InstallDate": install_date,
        "UninstallString": f'wmic product where "name like \'{APP_NAME}%\'" call uninstall /nointeractive',
        "DisplayIcon": os.path.join(INSTALL_DIR, f"{APP_NAME}.exe"),
        "InstallLocation": INSTALL_DIR,
        "NoModify": 1,
        "NoRepair": 1,
        "EstimatedSize": _get_dir_size(INSTALL_DIR) // 1024,
    }

    for key, value in reg_entries.items():
        if isinstance(value, int):
            subprocess.run(
                ["reg", "add", uninstall_key, "/v", key, "/t", "REG_DWORD", "/d", str(value), "/f"],
                capture_output=True, timeout=5,
            )
        else:
            subprocess.run(
                ["reg", "add", uninstall_key, "/v", key, "/t", "REG_SZ", "/d", str(value), "/f"],
                capture_output=True, timeout=5,
            )


def _unregister_uninstall():
    """删除卸载信息"""
    subprocess.run(
        ["reg", "delete", f"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{APP_NAME}", "/f"],
        capture_output=True, timeout=5,
    )


def _get_dir_size(path):
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            try:
                total += os.path.getsize(os.path.join(dirpath, f))
            except OSError:
                pass
    return total


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--uninstall":
        uninstall()
    else:
        install()
