# 语音情绪识别系统 v2.0 项目结构

## 概述

v2.0 使用 HuggingFace 预训练模型替代了原先的自训练模型，实现了**即开即用、多语种支持**。

## 文件结构

```
emo_choose/
├── emotion_recognizer.py     # 核心：基于预训练模型的情绪识别器
├── gui_app.py                # 图形界面（Tkinter）
├── batch_process.py          # 批量处理命令行工具
├── demo.py                   # 使用示例
├── quick_start.py            # 交互式快速启动
├── train_model.py            # 训练脚本（v2.0 已弃用，提示使用预训练模式）
├── test_system.py            # 系统组件测试
├── update_checker.py         # 更新检查器
├── build_exe.py              # PyInstaller 打包脚本
├── requirements.txt          # Python 依赖
├── README.md                 # 使用说明
├── PROJECT_STRUCTURE.md      # 项目结构说明
├── USER_GUIDE.md             # 用户指南
├── INSTALL.md                # 安装指南
└── start_app.bat             # Windows 一键启动脚本
```

## 核心模块

### emotion_recognizer.py
- `EmotionRecognizer` 类：基于 HuggingFace Transformers 的情绪识别器
  - 自动下载/加载预训练模型
  - `predict_emotion(audio_path)` → `(emotion, confidence)`
  - `predict_emotions(audio_path, top_k)` → `[(emotion, score), ...]`
- `FeatureExtractor` 类：音频特征提取器（保留兼容性）

### gui_app.py
- Tkinter 图形界面
- 支持单文件识别和文件夹批量处理
- 结果显示带置信度条形图

### batch_process.py
- 命令行批量处理
- 自动加载预训练模型，无需指定模型路径

## 技术栈变动

| 项目 | v1.0 | v2.0 |
|------|------|------|
| 深度学习框架 | TensorFlow | PyTorch |
| 模型来源 | 用户自行训练 | HuggingFace Hub |
| 模型架构 | 3层全连接网络 | Wav2Vec2 (Transformer) |
| 多语种支持 | ❌ 依赖训练数据 | ✅ XLSR-53 多语种基座 |
| 使用方法 | 训练→预测 | 即开即用 |
