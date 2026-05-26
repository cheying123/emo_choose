# 语音情绪识别系统 v2.0

基于 HuggingFace 预训练模型的多语种语音情绪识别 **Windows 桌面应用**。

✅ **即开即用** · 🌍 **多语种支持**（中/粤/英/日） · 🖥️ **双击启动**

---

## 快速开始

### 方式一：双击脚本启动（推荐）

```
双击「启动语音情绪识别系统.vbs」
```

首次使用会自动安装依赖并下载模型（约 1.5GB），后续离线可用。

### 方式二：双击 EXE 启动

```
双击「dist/语音情绪识别系统/语音情绪识别系统.exe」
```

### 方式三：命令行启动

```bash
pip install -r requirements.txt
python gui_app.py
```

---

## 功能

- **单个音频识别** — 选择 WAV/MP3/FLAC 等格式，一键识别情绪
- **批量处理** — 处理整个文件夹，自动输出 CSV 统计报告
- **Top-3 概率展示** — 显示最可能的三种情绪及其置信度
- **多语种支持** — 对中文、粤语、英语、日语等均有效

### 支持的情绪

| 情绪 | 标签 | 说明 |
|------|------|------|
| 中性 | neutral | 无明显情绪 |
| 平静 | calm | 平和放松 |
| 快乐 | happy | 高兴愉快 |
| 悲伤 | sad | 难过忧伤 |
| 愤怒 | angry | 生气恼怒 |
| 恐惧 | fearful | 害怕担心 |
| 厌恶 | disgust | 反感讨厌 |
| 惊讶 | surprised | 吃惊意外 |

---

## 技术架构

| 组件 | 说明 |
|------|------|
| **推理模型** | CAiRE/SER-wav2vec2-large-xlsr-53-eng-zho-all-age |
| **模型基座** | XLSR-53（53 种语言预训练） |
| **推理框架** | PyTorch + HuggingFace Transformers |
| **音频处理** | librosa（16kHz 重采样） |
| **桌面界面** | Python Tkinter |
| **打包工具** | PyInstaller / Inno Setup |

---

## 项目文件

```
emo_choose/
├── gui_app.py                      # 桌面应用主程序（双击运行）
├── emotion_recognizer.py           # 核心推理引擎
├── batch_process.py                # 命令行批量处理
├── update_checker.py               # 自动更新检查
├── requirements.txt                # Python 依赖
│
├── 启动语音情绪识别系统.vbs        # ★ 桌面快捷启动（双击即可）
├── start_app.bat                   # 命令行启动脚本
│
├── installer/
│   ├── installer.iss              # Inno Setup 安装脚本（生成 MSI 安装包）
│   └── README.txt                 # 安装包制作说明
│
├── build_exe.py                    # PyInstaller EXE 打包脚本
├── 语音情绪识别系统.spec           # PyInstaller 配置
│
├── demo.py                         # 使用示例
├── quick_start.py                  # 交互式菜单
├── test_system.py                  # 系统测试
│
└── README.md                       # 本文件
```

---

## 常见问题

**Q: 首次启动很慢？**
A: 首次需要下载预训练模型（约 1.5GB）。下载速度取决于网络。下载后自动缓存，后续离线使用。

**Q: 需要 GPU 吗？**
A: 不需要。CPU 即可运行。有 NVIDIA 显卡会自动使用 CUDA 加速。

**Q: 支持粤语/日语吗？**
A: 支持。情绪识别依靠语调、语速、音高等声学特征，与语言种类无关。模型基座 XLSR-53 覆盖 53 种语言。

**Q: 如何制作安装包？**
A: 先运行 `python build_exe.py` 编译 EXE，再用 Inno Setup 打开 `installer/installer.iss` 编译即可。

---

## 许可证

MIT License © 2026 EmoChoose
