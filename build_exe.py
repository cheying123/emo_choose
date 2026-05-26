"""
语音情绪识别系统 v2.0 - 打包脚本
生成可直接双击运行的 Windows EXE

注意：PyTorch/Transformers 体积太大（~2.5GB），不嵌入 EXE
EXE 首次运行时自动通过 pip 安装依赖 + 下载模型
"""
import os
import sys
import shutil
import subprocess


def build_exe():
    """打包生成 EXE（不含 PyTorch，启动时自动安装）"""
    print("=" * 50)
    print("语音情绪识别系统 v2.0 - EXE 打包")
    print("=" * 50)
    print("说明: PyTorch(~2GB) 不嵌入 EXE，首次启动自动安装")
    print()

    # 检查 PyInstaller
    try:
        import PyInstaller
        print(f"[OK] PyInstaller {PyInstaller.__version__}")
    except ImportError:
        print("正在安装 PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # 清理旧构建
    for d in ["dist", "build"]:
        if os.path.exists(d):
            shutil.rmtree(d)

    out_dir = "语音情绪识别系统"
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "gui_app.py",
        f"--name={out_dir}",
        "--onedir",                     # 目录模式（比单文件更稳定）
        "--windowed",                   # 无控制台窗口
        "--add-data=emotion_recognizer.py;.",
        "--add-data=update_checker.py;.",
        "--add-data=requirements.txt;.",  # 用于自动安装依赖
        "--collect-all=librosa",
        "--collect-all=scipy",
        "--collect-all=sklearn",
        "--collect-all=soundfile",
        # 显式排除 PyTorch/Transformers（太大，首次运行自动 pip 安装）
        "--exclude-module=torch",
        "--exclude-module=torch.nn",
        "--exclude-module=transformers",
        "--exclude-module=tokenizers",
        "--exclude-module=huggingface_hub",
        "--exclude-module=matplotlib",
        "--exclude-module=seaborn",
        "--exclude-module=tensorflow",
        "--exclude-module=PIL",
        "--exclude-module=packaging",
        "--clean",
        "--noconfirm",
    ]

    print("开始打包，请稍候...")
    print(f"打包命令: {' '.join(cmd)}")
    print()

    try:
        subprocess.check_call(cmd)
        exe_path = os.path.join("dist", out_dir, f"{out_dir}.exe")
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)

        print("\n" + "=" * 50)
        print(f"[OK] EXE 打包成功！")
        print(f"  位置: {exe_path}")
        print(f"  大小: {size_mb:.0f} MB")
        print(f"\n使用说明:")
        print(f"  1. 双击 {out_dir}.exe 启动")
        print(f"  2. 首次运行自动安装 PyTorch（~2GB，仅一次）")
        print(f"  3. 安装后自动下载模型（~1.5GB，仅一次）")
        print(f"  4. 后续离线可用")
        print("=" * 50)

        # 复制 requirements.txt 到 EXE 目录
        shutil.copy("requirements.txt", os.path.join("dist", out_dir, "requirements.txt"))
        print(f"\n[OK] 已复制 requirements.txt 到输出目录")

    except subprocess.CalledProcessError as e:
        print(f"\n[FAIL] 打包失败: {e}")
        sys.exit(1)


def build_msi():
    """使用 Inno Setup 编译 MSI 安装包"""
    iss_path = os.path.join("installer", "installer.iss")
    if not os.path.exists(iss_path):
        print(f"\n[FAIL] 找不到安装脚本: {iss_path}")
        return

    # 尝试各种可能的 Inno Setup 路径
    iscc_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
    ]

    iscc = None
    for p in iscc_paths:
        if os.path.exists(p):
            iscc = p
            break

    if not iscc:
        print(f"\n[SKIP] 未检测到 Inno Setup 编译器")
        print(f"  如需制作 MSI 安装包，请安装 Inno Setup:")
        print(f"  https://jrsoftware.org/isinfo.php")
        print(f"  安装后运行: ISCC installer/installer.iss")
        return

    print(f"\n编译 MSI 安装包...")
    print(f"  ISCC: {iscc}")
    print(f"  脚本: {iss_path}")

    try:
        subprocess.check_call([iscc, iss_path])
        print(f"\n[OK] MSI 安装包生成成功！")
        print(f"  请查看 installer/ 目录")
    except subprocess.CalledProcessError as e:
        print(f"\n[FAIL] MSI 编译失败: {e}")


def main():
    print("语音情绪识别系统 v2.0 - 打包工具")
    print("=" * 50)

    if len(sys.argv) > 1:
        if sys.argv[1] == "--msi":
            build_msi()
            return
        elif sys.argv[1] == "--all":
            build_exe()
            build_msi()
            return

    build_exe()


if __name__ == "__main__":
    main()
