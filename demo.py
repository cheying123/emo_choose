"""
语音情绪识别系统使用示例
演示如何使用 EmotionRecognizer 识别音频文件的情绪
"""
import os
from emotion_recognizer import EmotionRecognizer


def demo_basic_usage():
    """演示基本用法"""
    print("=" * 50)
    print("语音情绪识别系统 v2.0 演示")
    print("基于 HuggingFace 预训练模型，支持多语种")
    print("=" * 50)

    # 创建识别器实例（自动下载并加载预训练模型）
    print("\n正在初始化情绪识别器（首次使用会自动下载模型）...")
    recognizer = EmotionRecognizer()

    print(f"\n✓ 识别器就绪")
    print(f"  模型: {recognizer.model_name}")
    print(f"  设备: {recognizer.device}")
    print(f"  支持的情绪: {recognizer.emotions}")


def demo_predict_real_file():
    """演示如何识别真实音频文件"""
    print("\n" + "=" * 50)
    print("情绪识别演示")
    print("=" * 50)

    recognizer = EmotionRecognizer()

    # 示例1: 基本预测
    print("\n【示例1】预测单个音频文件:")
    print("  from emotion_recognizer import EmotionRecognizer")
    print("  recognizer = EmotionRecognizer()")
    print("  emotion, confidence = recognizer.predict_emotion('audio.wav')")
    print(f"  # 返回: ('happy', 0.95)")

    # 示例2: Top-K 预测
    print("\n【示例2】获取 Top-3 情绪预测:")
    print("  results = recognizer.predict_emotions('audio.wav', top_k=3)")
    print("  for emotion, score in results:")
    print("      print(f'{emotion}: {score:.4f}')")
    print("  # 返回: [('happy', 0.85), ('surprised', 0.08), ('neutral', 0.03)]")

    # 示例3: 批量处理
    print("\n【示例3】批量处理文件夹中的音频:")
    print("  python batch_process.py --input ./audio_folder --output results.csv")

    # 示例4: 使用 GUI
    print("\n【示例4】启动图形界面:")
    print("  python gui_app.py")


def demo_real_audio_steps():
    """使用说明"""
    print("\n" + "=" * 50)
    print("使用步骤")
    print("=" * 50)
    print("1. 安装依赖：pip install -r requirements.txt")
    print("2. 运行本演示：python demo.py")
    print("3. 识别单个音频：")
    print("   python -c \"from emotion_recognizer import EmotionRecognizer;")
    print("   r = EmotionRecognizer(); print(r.predict_emotion('音频文件.wav'))\"")
    print("4. 批量处理：")
    print("   python batch_process.py --input ./音频文件夹")
    print("5. 启动图形界面：")
    print("   python gui_app.py")
    print()
    print("注意：首次使用会自动下载预训练模型（约 1.5GB）")
    print("下载后会自动缓存，后续无需网络")


def main():
    demo_basic_usage()
    demo_predict_real_file()
    demo_real_audio_steps()

    print("\n" + "=" * 50)
    print("演示完成！系统已就绪，可直接用于情绪识别。")
    print("=" * 50)


if __name__ == "__main__":
    main()
