# 语音情绪识别系统 v2.0 安装说明

## 概述

基于 HuggingFace 预训练模型的多语种语音情绪识别系统。即开即用，无需训练数据，支持中文、粤语、英语、日语等多种语言。

## 系统要求

- **操作系统**: Windows 10/11, macOS, Linux
- **Python**: 3.8 或更高版本
- **内存**: 4GB+（推荐 8GB）
- **磁盘空间**: 至少 3GB（含预训练模型缓存约 1.5GB）
- **网络**: 首次使用需要联网下载模型

## 安装步骤

### 方法一：从源码运行（推荐）

1. **安装 Python 3.8+**

   ```bash
   python --version
   ```

2. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

3. **启动程序**

   ```bash
   python gui_app.py
   ```

   （首次启动会自动下载预训练模型约 1.5GB，请耐心等待）

### 方法二：使用预编译 exe 文件

1. 从 `dist` 目录中找到 `语音情绪识别系统.exe`
2. 双击运行
3. 首次使用仍需联网下载模型

> **注意**: exe 版本首次运行时仍需联网下载模型（约 1.5GB），下载后自动缓存。

## 使用说明

### 单个文件识别
1. 启动程序（首次需等待模型下载）
2. 点击"浏览"选择音频文件
3. 点击"识别情绪"
4. 查看结果（含 Top-3 概率可视化）

### 批量处理
1. 选择音频文件夹
2. 指定输出 CSV 路径
3. 点击"批量识别"
4. 自动生成统计报告

## 命令行工具

```bash
# 批量处理
python batch_process.py --input ./音频文件夹 --output results.csv

# 查看演示
python demo.py
```

## GPU 加速（可选）

如有 NVIDIA 显卡：

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

## 常见问题

### 1. 首次启动很慢？
首次需要下载模型约 1.5GB。下载速度取决于网络，建议在良好网络环境下进行。下载后自动缓存，后续离线可用。

### 2. 需要 GPU 吗？
不需要。CPU 即可运行，有 GPU 自动加速。

### 3. 支持中文/粤语/日语吗？
支持。基于 XLSR-53 多语种预训练，通过声学特征（语调、语速、音高）进行情绪识别，与具体语言无关。

### 4. 模型文件在哪？
- Windows: `C:\Users\<用户名>\.cache\huggingface\hub\`
- Linux/Mac: `~/.cache/huggingface/hub/`

## 更新日志

### v2.0.0 (2026年5月)
- 🎉 改用 HuggingFace 预训练模型，即开即用
- 🌍 支持多语种情绪识别
- 🔥 去掉 TensorFlow，改用 PyTorch
- 🗑️ 移除训练流程，简化使用
- 📊 GUI 增加概率可视化
