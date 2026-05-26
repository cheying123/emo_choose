"""
语音情绪识别系统 v2.0 - 图形用户界面
现代 Windows 桌面风格 · 带下载进度条 · 即开即用

注意：重型依赖（torch/transformers）为懒加载，窗口立即弹出
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import subprocess
import sys

APP_NAME = "语音情绪识别系统"
APP_VERSION = "2.0.0"


class EmotionRecognitionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("860x680")
        self.root.minsize(720, 560)

        # 应用样式
        self._setup_style()

        # 状态
        self.recognizer = None
        self.model_loaded = False

        # 先创建界面（窗口立即弹出），再后台加载模型
        self.create_widgets()
        self.root.after(100, self.init_recognizer)

    def _setup_style(self):
        """设置现代 Windows 风格"""
        self.style = ttk.Style()
        for theme in ("vista", "clam", "default"):
            try:
                self.style.theme_use(theme)
                break
            except Exception:
                continue

        self.title_font = ("微软雅黑", 18, "bold")
        self.section_font = ("微软雅黑", 10, "bold")
        self.mono_font = ("Consolas", 10)

    # ==================== 模型加载 ====================

    def init_recognizer(self):
        """后台初始化识别器（检测依赖 + 懒加载 + 下载进度）"""
        self._set_loading_state()

        def load():
            try:
                # 第一步：自动检测并安装缺失的依赖
                self._ensure_dependencies()

                # 第二步：懒导入并加载模型
                from emotion_recognizer import EmotionRecognizer
                self.recognizer = EmotionRecognizer(
                    progress_callback=self._on_download_progress,
                )
                self.root.after(0, self._on_model_loaded)
            except Exception as e:
                self.root.after(0, lambda: self._on_model_failed(str(e)))

        threading.Thread(target=load, daemon=True).start()

    def _on_download_progress(self, file_name, current_bytes, total_bytes):
        """下载进度回调"""
        if total_bytes > 0:
            pct = min(current_bytes / total_bytes * 100, 99.9)
            mb_done = current_bytes / (1024 * 1024)
            mb_total = total_bytes / (1024 * 1024)
            msg = f"下载中: {file_name}  ({mb_done:.0f}/{mb_total:.0f} MB, {pct:.0f}%)"
            self.root.after(0, lambda: self._update_download_ui(pct, msg))

    def _update_download_ui(self, pct, msg):
        self.progress_bar["value"] = pct
        self.progress_bar["mode"] = "determinate"
        self.status_var.set(msg)
        self.download_label.config(text=f"模型下载中... {pct:.0f}%")
        self.download_sub_label.config(
            text="首次使用需要下载预训练模型，下载后自动缓存，后续离线可用"
        )

    def _set_loading_state(self):
        self.progress_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        self.main_content.grid_remove()
        self.progress_bar["mode"] = "indeterminate"
        self.progress_bar.start(15)
        self.download_label.config(text="正在初始化（导入依赖库）...")
        self.download_sub_label.config(text="")

    def _on_model_loaded(self):
        self.model_loaded = True
        self.progress_bar.stop()
        self.progress_bar["value"] = 100

        self.progress_frame.grid_remove()
        self.main_content.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(0, 8))

        self._update_status(
            f"就绪 · 模型: {self.recognizer.model_name} · 设备: {self.recognizer.device}"
        )
        self.recognize_btn.config(state=tk.NORMAL)
        self.batch_recognize_btn.config(state=tk.NORMAL)

        # 后台检查更新
        try:
            from update_checker import auto_check
            auto_check(self.root)
        except Exception:
            pass

    def _on_model_failed(self, error_msg):
        self.progress_bar.stop()
        self._update_status("模型加载失败")
        self.download_label.config(text="下载失败", foreground="red")
        self.download_sub_label.config(
            text="已自动尝试国内镜像，若仍有问题请检查网络", foreground="red"
        )
        messagebox.showerror(
            "模型加载失败",
            f"无法加载情绪识别模型。\n\n错误: {error_msg}\n\n"
            f"可能的原因及解决方法：\n"
            f"1. 网络问题 — 已自动切换国内镜像 hf-mirror.com，请重试\n"
            f"2. 防火墙/代理 — 请确保网络可以访问 HuggingFace\n"
            f"3. 磁盘空间 — 模型约 1.5GB，请确保有足够空间\n\n"
            f"也可以手动设置镜像:\n"
            f"  在命令行执行: set HF_ENDPOINT=https://hf-mirror.com\n"
            f"  然后重新启动程序",
        )

    def _ensure_dependencies(self):
        """自动检查并安装缺失的 Python 依赖"""
        missing = []
        for pkg in ["torch", "transformers", "librosa", "soundfile"]:
            try:
                __import__(pkg.replace("-", "_"))
            except ImportError:
                missing.append(pkg)

        if not missing:
            return

        self._update_status(f"正在安装依赖（{', '.join(missing)}）...")
        self.root.after(0, lambda: self.download_label.config(
            text=f"正在安装依赖库（{', '.join(missing)}）..."
        ))
        self.root.after(0, lambda: self.download_sub_label.config(
            text="首次运行需要安装 PyTorch 等（约需 3-5 分钟）"
        ))

        req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", req_path],
                capture_output=True, text=True, timeout=600,
            )
            if result.returncode != 0:
                raise RuntimeError(f"安装失败:\n{result.stderr[-500:]}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("安装超时，请检查网络后重试")
        except RuntimeError:
            raise
        except Exception as e:
            raise RuntimeError(f"自动安装失败: {e}\n请手动运行: pip install -r requirements.txt")

    # ==================== 界面 ====================

    def create_widgets(self):
        """创建界面（窗口立即弹出，不阻塞）"""
        # 菜单栏
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        fm = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=fm)
        fm.add_command(label="退出", command=self.root.quit)

        hm = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=hm)
        hm.add_command(label="检查更新", command=self._manual_check)
        hm.add_separator()
        hm.add_command(label="使用说明", command=self.show_help)
        hm.add_command(label="关于", command=self.show_about)

        # 主容器
        c = ttk.Frame(self.root, padding="16")
        c.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        c.columnconfigure(0, weight=1)
        c.rowconfigure(3, weight=1)

        # 标题区
        hdr = ttk.Frame(c)
        hdr.grid(row=0, column=0, columnspan=2, pady=(0, 16), sticky="ew")
        ttk.Label(hdr, text=APP_NAME, font=self.title_font).pack(anchor="center")

        # ===== 下载进度页面 =====
        self.progress_frame = ttk.Frame(c, padding="20")
        self.progress_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        self.progress_frame.columnconfigure(0, weight=1)

        pf = ttk.LabelFrame(self.progress_frame, text="模型初始化", padding="20")
        pf.pack(fill="x", expand=True)

        self.download_label = ttk.Label(
            pf, text="正在初始化...", font=("微软雅黑", 11),
        )
        self.download_label.pack(pady=(0, 8))

        self.progress_bar = ttk.Progressbar(pf, mode="indeterminate", length=500)
        self.progress_bar.pack(fill="x", pady=(0, 8))

        self.download_sub_label = ttk.Label(pf, text="", font=("微软雅黑", 9), foreground="#888")
        self.download_sub_label.pack()

        # ===== 主功能界面（初始隐藏） =====
        self.main_content = ttk.Frame(c)

        # 卡片1: 单文件识别
        c1 = ttk.LabelFrame(self.main_content, text="单个音频识别", padding="12")
        c1.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=(0, 10))
        c1.columnconfigure(1, weight=1)

        ttk.Label(c1, text="音频文件:", font=self.section_font).grid(
            row=0, column=0, sticky="w", padx=(0, 6)
        )
        self.file_path_var = tk.StringVar()
        ttk.Entry(c1, textvariable=self.file_path_var).grid(
            row=0, column=1, sticky="ew", padx=(0, 6)
        )
        ttk.Button(c1, text="浏览...", command=self.browse_file).grid(row=0, column=2)

        self.recognize_btn = ttk.Button(
            c1, text="识别情绪", command=self.recognize_single_file, state=tk.DISABLED,
        )
        self.recognize_btn.grid(row=1, column=0, columnspan=3, pady=(10, 0), ipadx=10)

        # 卡片2: 批量处理
        c2 = ttk.LabelFrame(self.main_content, text="批量处理", padding="12")
        c2.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=(0, 10))
        c2.columnconfigure(1, weight=1)

        ttk.Label(c2, text="音频文件夹:", font=self.section_font).grid(
            row=0, column=0, sticky="w", padx=(0, 6)
        )
        self.folder_path_var = tk.StringVar()
        ttk.Entry(c2, textvariable=self.folder_path_var).grid(
            row=0, column=1, sticky="ew", padx=(0, 6)
        )
        ttk.Button(c2, text="浏览...", command=self.browse_folder).grid(row=0, column=2)

        ttk.Label(c2, text="输出 CSV:").grid(
            row=1, column=0, sticky="w", padx=(0, 6), pady=(6, 0)
        )
        self.output_path_var = tk.StringVar()
        ttk.Entry(c2, textvariable=self.output_path_var).grid(
            row=1, column=1, sticky="ew", padx=(0, 6), pady=(6, 0)
        )
        ttk.Button(c2, text="选择...", command=self.select_output_file).grid(
            row=1, column=2, pady=(6, 0)
        )

        self.batch_recognize_btn = ttk.Button(
            c2, text="批量识别", command=self.recognize_batch_files, state=tk.DISABLED,
        )
        self.batch_recognize_btn.grid(row=2, column=0, columnspan=3, pady=(10, 0), ipadx=10)

        # 卡片3: 结果
        c3 = ttk.LabelFrame(self.main_content, text="识别结果", padding="8")
        c3.grid(row=1, column=0, columnspan=2, sticky="nsew")
        c3.columnconfigure(0, weight=1)
        c3.rowconfigure(0, weight=1)
        self.main_content.rowconfigure(1, weight=1)

        self.result_text = scrolledtext.ScrolledText(
            c3, height=10, font=self.mono_font, wrap=tk.WORD,
            relief=tk.FLAT, borderwidth=1,
        )
        self.result_text.grid(row=0, column=0, sticky="nsew")

        # 状态栏
        ttk.Separator(c, orient="horizontal").grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=(4, 4)
        )
        self.status_var = tk.StringVar(value="正在初始化...")
        ttk.Label(
            c, textvariable=self.status_var,
            font=("微软雅黑", 9), foreground="#555",
            anchor="w", padding=(4, 2),
        ).grid(row=5, column=0, columnspan=2, sticky="ew")

    def _manual_check(self):
        """手动检查更新"""
        try:
            from update_checker import manual_check
            manual_check(self.root)
        except Exception:
            messagebox.showinfo("检查更新", "当前已是最新版本")

    def show_about(self):
        messagebox.showinfo(
            f"关于 {APP_NAME}",
            f"{APP_NAME} v{APP_VERSION}\n\n"
            f"基于 HuggingFace 预训练模型的多语种语音情绪识别系统。\n\n"
            f"核心模型: CAiRE/SER-wav2vec2-large-xlsr-53-eng-zho-all-age\n"
            f"运行框架: PyTorch + Transformers\n"
            f"支持语种: 中文、粤语、英语、日语等\n"
            f"支持格式: WAV / MP3 / FLAC / M4A / AAC\n\n"
            f"© 2026 EmoChoose",
        )

    def show_help(self):
        messagebox.showinfo(
            "使用说明",
            "1. 启动程序后等待模型下载完成\n"
            "2. 选择音频文件，点击「识别情绪」\n"
            "3. 或选择文件夹进行批量处理\n\n"
            "提示：\n"
            "• 首次使用需联网下载模型（约1.5GB）\n"
            "• 支持中文、粤语、英语、日语等\n"
            "• 情绪识别基于语调/语速/音高等声学特征\n"
            "• 结果中会显示 Top-3 置信度",
        )

    # ==================== 文件操作 ====================

    def browse_file(self):
        path = filedialog.askopenfilename(
            title="选择音频文件",
            filetypes=[("音频文件", "*.wav *.mp3 *.flac *.m4a *.aac"), ("所有文件", "*.*")],
        )
        if path:
            self.file_path_var.set(path)

    def browse_folder(self):
        path = filedialog.askdirectory(title="选择音频文件夹")
        if path:
            self.folder_path_var.set(path)

    def select_output_file(self):
        path = filedialog.asksaveasfilename(
            title="保存结果", defaultextension=".csv",
            filetypes=[("CSV 文件", "*.csv"), ("所有文件", "*.*")],
        )
        if path:
            self.output_path_var.set(path)

    # ==================== 单文件识别 ====================

    def recognize_single_file(self):
        path = self.file_path_var.get().strip()
        if not path:
            messagebox.showwarning("提示", "请先选择音频文件")
            return
        if not os.path.exists(path):
            messagebox.showerror("错误", "文件不存在")
            return
        if not self.model_loaded:
            messagebox.showinfo("提示", "模型还在加载中，请稍候...")
            return

        threading.Thread(target=self._recognize_single_thread, args=(path,), daemon=True).start()

    def _recognize_single_thread(self, file_path):
        try:
            self._update_status("正在识别...")
            self._start_progress()

            emotion, confidence = self.recognizer.predict_emotion(file_path)
            top_k = self.recognizer.predict_emotions(file_path, top_k=3)

            lines = [
                f"文件: {os.path.basename(file_path)}",
                "=" * 44,
                f"识别情绪: {emotion}",
                f"置信度: {confidence:.4f}  ({confidence*100:.1f}%)",
                "",
                "Top-3 预测:",
            ]
            for emo, score in top_k:
                bar = "█" * int(score * 28)
                lines.append(f"  {emo:<12s}  {score:.4f}  {bar}")

            lines.append("=" * 44 + "\n")
            self._insert_result("\n".join(lines))
            self._update_status(f"识别完成: {emotion} ({confidence*100:.1f}%)")

        except Exception as e:
            self._insert_result(f"识别出错: {e}\n")
            self._update_status("识别失败")
        finally:
            self._stop_progress()

    # ==================== 批量处理 ====================

    def recognize_batch_files(self):
        folder = self.folder_path_var.get().strip()
        output = self.output_path_var.get().strip()

        if not folder:
            messagebox.showwarning("提示", "请先选择音频文件夹")
            return
        if not output:
            messagebox.showwarning("提示", "请先选择输出 CSV 路径")
            return
        if not os.path.exists(folder):
            messagebox.showerror("错误", "文件夹不存在")
            return
        if not self.model_loaded:
            messagebox.showinfo("提示", "模型还在加载中，请稍候...")
            return

        threading.Thread(target=self._recognize_batch_thread, args=(folder, output), daemon=True).start()

    def _recognize_batch_thread(self, folder_path, output_path):
        try:
            self._update_status("正在批量识别...")
            self._start_progress()

            supported = {".wav", ".mp3", ".flac", ".m4a", ".aac"}
            audio_files = [
                f for f in os.listdir(folder_path)
                if any(f.lower().endswith(ext) for ext in supported)
            ]

            if not audio_files:
                self._insert_result("未找到支持的音频文件\n")
                self._update_status("无音频文件")
                return

            results = []
            for i, name in enumerate(audio_files):
                ap = os.path.join(folder_path, name)
                try:
                    self._update_status(f"处理 [{i+1}/{len(audio_files)}]: {name}")
                    emotion, confidence = self.recognizer.predict_emotion(ap)
                    results.append({
                        "filename": name, "emotion": emotion,
                        "confidence": round(confidence, 4),
                    })
                    self._insert_result(f"[{i+1}/{len(audio_files)}] {name} -> {emotion} ({confidence:.1%})\n")
                except Exception as e:
                    results.append({
                        "filename": name, "emotion": "error",
                        "confidence": 0.0, "error": str(e),
                    })
                    self._insert_result(f"[{i+1}/{len(audio_files)}] {name} -> 失败: {e}\n")

            if results:
                import pandas as pd
                pd.DataFrame(results).to_csv(output_path, index=False, encoding="utf-8-sig")

                ok = [r for r in results if r["emotion"] != "error"]
                if ok:
                    from collections import Counter
                    counter = Counter(r["emotion"] for r in ok)
                    self._insert_result(f"\n{'='*44}\n处理完成! 共 {len(results)} 个文件\n")
                    self._insert_result("情绪统计:\n")
                    for emo, count in counter.most_common():
                        pct = count / len(ok) * 100
                        bar = "█" * int(pct / 4)
                        self._insert_result(f"  {emo:<12s}  {count:3d}个 ({pct:.1f}%)  {bar}\n")

            self._update_status(f"批量处理完成，共 {len(results)} 个文件")

        except Exception as e:
            self._insert_result(f"批量处理出错: {e}\n")
            self._update_status("批量处理失败")
        finally:
            self._stop_progress()

    # ==================== 辅助方法 ====================

    def _update_status(self, msg):
        self.root.after(0, lambda: self.status_var.set(msg))

    def _start_progress(self):
        self.root.after(0, lambda: self.progress_bar.start(10))

    def _stop_progress(self):
        self.root.after(0, lambda: self.progress_bar.stop())

    def _insert_result(self, text):
        self.root.after(0, lambda: self.result_text.insert(tk.END, text))
        self.root.after(0, lambda: self.result_text.see(tk.END))


def main():
    root = tk.Tk()
    app = EmotionRecognitionGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
