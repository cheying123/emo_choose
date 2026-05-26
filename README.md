# 语音情绪识别系统 v2.0

基于 HuggingFace 预训练模型的多语种语音情绪识别系统。

🌍 支持中文、粤语、英语、日语等 · 🚀 即开即用 · 🖥️ 浏览器界面

---

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动 Web 服务
python web_app.py

# 3. 浏览器打开 http://localhost:5000
```

首次启动会自动下载模型（约 1.5GB），请保持网络畅通。

## 支持的情绪

中性 · 平静 · 快乐 · 悲伤 · 愤怒 · 恐惧 · 厌恶 · 惊讶

## 多语种支持

基于 XLSR-53 多语种预训练（覆盖 53 种语言），通过声学特征（语调、语速、音高）识别情绪，与语言内容无关。

## 技术栈

| 组件 | 说明 |
|------|------|
| **推理模型** | CAiRE/SER-wav2vec2-large-xlsr-53-eng-zho-all-age |
| **推理框架** | PyTorch + HuggingFace Transformers |
| **后端** | Flask |
| **前端** | 原生 HTML/CSS/JS（单页） |
| **音频** | librosa（16kHz 重采样） |

## 项目文件

```
emo_choose/
├── web_app.py                 Web 服务（主入口）
├── emotion_recognizer.py      核心推理引擎
├── gui_app.py                 桌面版 GUI（备选）
├── batch_process.py           命令行批量处理
├── requirements.txt           依赖清单
├── start_app.bat              Windows 启动脚本
└── README.md                  本文件
```

## 国内网络

自动检测并使用 `hf-mirror.com` 镜像，无需手动配置。
