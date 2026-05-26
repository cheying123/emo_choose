# 语音情绪识别系统 v2.0 使用指南

基于 HuggingFace 预训练模型，支持多语种，即开即用。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动图形界面

```bash
python gui_app.py
```

首次启动会自动下载预训练模型（约 1.5GB），请耐心等待。下载后自动缓存，后续离线可用。

### 3. 批量处理音频

```bash
python batch_process.py --input ./音频文件夹 --output results.csv
```

### 4. 查看演示

```bash
python demo.py
```

## Python API

### 单文件情绪识别

```python
from emotion_recognizer import EmotionRecognizer

# 初始化（自动加载模型）
recognizer = EmotionRecognizer()

# 预测情绪
emotion, confidence = recognizer.predict_emotion("audio.wav")
print(f"情绪: {emotion}, 置信度: {confidence:.4f}")

# 获取 Top-3 预测
results = recognizer.predict_emotions("audio.wav", top_k=3)
for emotion, score in results:
    print(f"{emotion}: {score:.4f}")
```

## 支持的情绪类别

| 情绪 | 英文标签 | 说明 |
|------|---------|------|
| 中性 | neutral | 无明显情绪 |
| 平静 | calm | 平和、放松 |
| 快乐 | happy | 高兴、愉快 |
| 悲伤 | sad | 难过、忧伤 |
| 愤怒 | angry | 生气、恼怒 |
| 恐惧 | fearful | 害怕、担心 |
| 厌恶 | disgust | 反感、讨厌 |
| 惊讶 | surprised | 吃惊、意外 |

## 支持的音频格式

- WAV（推荐）
- MP3
- FLAC
- M4A
- AAC

## 支持的语种

基于 XLSR-53 多语种预训练 + 中英文微调，对以下语种均有良好的跨语言迁移效果：

- 中文普通话
- 粤语
- 英语
- 日语
- 以及其他常见语言

原理：情绪识别主要依靠语调、语速、音高等声学特征，而非语义内容。

## 常见问题

**Q: 首次启动很慢？**
A: 首次需要下载预训练模型（约 1.5GB），下载速度取决于网络。下载后自动缓存。

**Q: 需要 GPU 吗？**
A: 不需要，CPU 即可运行。有 GPU（CUDA）会自动使用加速。

**Q: 我想用其他模型？**
A: 支持自定义 HuggingFace 模型：
```python
recognizer = EmotionRecognizer(model_name="其他模型名称")
```

**Q: 准确率如何？**
A: 采用学术界 SOTA 的 wav2vec2 + XLSR-53 架构，在公开数据集上达到领先水平。实际效果取决于音频质量。
