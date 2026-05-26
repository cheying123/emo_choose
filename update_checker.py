"""
语音情绪识别系统 v2.0 - 更新检查器
支持自动检查 GitHub Releases 更新
"""
import json
import os
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from packaging import version
import urllib.request
import urllib.error

APP_NAME = "语音情绪识别系统"
APP_VERSION = "2.0.0"
# 默认更新检查地址（可配置）
DEFAULT_UPDATE_URL = "https://api.github.com/repos/emo-choose/emo-choose/releases/latest"
LAST_CHECK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "last_update_check.json")
CHECK_INTERVAL_HOURS = 24


class UpdateChecker:
    def __init__(self, current_version=APP_VERSION, update_url=None):
        self.current_version = current_version
        self.update_url = update_url or DEFAULT_UPDATE_URL
        self.last_check_file = LAST_CHECK_FILE

    def should_check(self):
        """判断是否到了检查更新的时间"""
        try:
            if os.path.exists(self.last_check_file):
                with open(self.last_check_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    last = datetime.fromisoformat(data.get("last_check", "2000-01-01"))
                    if datetime.now() - last < timedelta(hours=CHECK_INTERVAL_HOURS):
                        return False
        except Exception:
            pass
        return True

    def save_check_time(self):
        """保存检查时间"""
        try:
            with open(self.last_check_file, "w", encoding="utf-8") as f:
                json.dump({
                    "last_check": datetime.now().isoformat(),
                    "version": self.current_version,
                }, f)
        except Exception:
            pass

    def check(self):
        """
        检查更新
        Returns:
            dict: {"has_update": bool, "latest_version": str, ...}
                  或 {"has_update": False, "error": str}
        """
        try:
            req = urllib.request.Request(
                self.update_url,
                headers={"User-Agent": f"{APP_NAME}/{self.current_version}"},
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    latest = data.get("tag_name", "").lstrip("vV")

                    if version.parse(latest) > version.parse(self.current_version):
                        return {
                            "has_update": True,
                            "latest_version": latest,
                            "current_version": self.current_version,
                            "release_notes": data.get("body", "暂无更新说明"),
                            "download_url": self._get_download_url(data),
                            "release_date": data.get("published_at", ""),
                            "html_url": data.get("html_url", ""),
                        }
                    return {"has_update": False}

                return {"has_update": False, "error": f"HTTP {resp.status}"}

        except urllib.error.HTTPError as e:
            # 404 通常意味着没有 release（正常情况）
            if e.code == 404:
                return {"has_update": False}
            return {"has_update": False, "error": f"HTTP {e.code}"}
        except urllib.error.URLError as e:
            return {"has_update": False, "error": f"网络错误: {e.reason}"}
        except Exception as e:
            return {"has_update": False, "error": str(e)}

    def _get_download_url(self, release_data):
        """从 release 数据中提取下载链接"""
        assets = release_data.get("assets", [])
        for asset in assets:
            name = asset.get("name", "")
            if name.endswith(".exe") and "安装" in name:
                return asset.get("browser_download_url", "")
        for asset in assets:
            if asset.get("name", "").endswith(".exe"):
                return asset.get("browser_download_url", "")
        return release_data.get("html_url", "")


def auto_check(parent):
    """自动检查更新（启动时调用，忽略间隔）"""
    def _do_check():
        checker = UpdateChecker()
        result = checker.check()
        if result.get("has_update"):
            parent.after(0, lambda: _show_update_dialog(parent, result))
        checker.save_check_time()

    threading.Thread(target=_do_check, daemon=True).start()


def manual_check(parent):
    """手动检查更新"""
    def _do_check():
        parent.after(0, lambda: _show_checking(parent))
        checker = UpdateChecker()
        result = checker.check()
        parent.after(0, lambda: _show_result(parent, result))
        checker.save_check_time()

    threading.Thread(target=_do_check, daemon=True).start()


def _show_checking(parent):
    """显示正在检查"""
    # 简单在状态栏显示（由调用方自行处理）
    pass


def _show_result(parent, result):
    """显示检查结果"""
    if result.get("has_update"):
        _show_update_dialog(parent, result)
    elif result.get("error"):
        try:
            messagebox.showwarning(
                "检查更新",
                f"无法检查更新。\n\n{result['error']}\n\n请稍后重试。"
            )
        except Exception:
            pass
    else:
        try:
            messagebox.showinfo("检查更新", "当前已是最新版本。")
        except Exception:
            pass


def _show_update_dialog(parent, info):
    """显示更新对话框"""
    dialog = tk.Toplevel(parent)
    dialog.title("发现新版本")
    dialog.geometry("520x450")
    dialog.minsize(400, 300)
    dialog.transient(parent)
    dialog.grab_set()

    # 版本信息
    frame = ttk.Frame(dialog, padding="15")
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text=f"当前版本: v{info.get('current_version', '')}",
              font=("", 10)).pack(anchor="w")
    ttk.Label(frame, text=f"最新版本: v{info['latest_version']}",
              font=("", 12, "bold"), foreground="blue").pack(anchor="w", pady=(5, 10))

    # 更新内容
    ttk.Label(frame, text="更新内容:", font=("", 10, "bold")).pack(anchor="w")
    text = tk.Text(frame, height=10, wrap="word", font=("", 9))
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
    text.configure(yscrollcommand=scrollbar.set)

    content = info.get("release_notes", "暂无更新说明")
    text.insert("1.0", content)
    text.config(state="disabled")

    text.pack(fill="both", expand=True, side="left")
    scrollbar.pack(fill="y", side="right")

    # 按钮
    btn_frame = ttk.Frame(frame)
    btn_frame.pack(fill="x", pady=(12, 0))

    url = info.get("download_url", "")
    if url:
        import webbrowser
        ttk.Button(
            btn_frame, text="前往下载页面",
            command=lambda: webbrowser.open(url),
        ).pack(side="left", padx=(0, 8))

    ttk.Button(btn_frame, text="稍后提醒", command=dialog.destroy).pack(side="right")


if __name__ == "__main__":
    import sys
    checker = UpdateChecker()
    result = checker.check()
    if result.get("has_update"):
        print(f"发现新版本: v{result['latest_version']}")
        print(f"下载地址: {result.get('download_url', '无')}")
    elif result.get("error"):
        print(f"检查失败: {result['error']}")
    else:
        print("当前已是最新版本")
