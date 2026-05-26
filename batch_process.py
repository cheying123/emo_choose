"""
批量处理音频文件的情绪识别脚本
基于 HuggingFace 预训练模型，即开即用
"""
import os
import argparse
import pandas as pd
from datetime import datetime
from emotion_recognizer import EmotionRecognizer


def batch_predict_from_folder(audio_folder_path, output_csv_path=None):
    """
    批量处理指定文件夹中的音频文件

    Args:
        audio_folder_path: 音频文件所在的文件夹路径
        output_csv_path: 输出CSV文件路径（可选）
    """
    # 创建识别器实例（自动加载预训练模型）
    print("正在初始化情绪识别器...")
    recognizer = EmotionRecognizer()
    print(f"模型加载完成: {recognizer.model_name}")

    # 支持的音频文件扩展名
    supported_extensions = {".wav", ".mp3", ".flac", ".m4a", ".aac"}

    # 获取文件夹中的所有音频文件
    audio_files = [
        os.path.join(audio_folder_path, f)
        for f in os.listdir(audio_folder_path)
        if any(f.lower().endswith(ext) for ext in supported_extensions)
    ]

    if not audio_files:
        print(f"在 {audio_folder_path} 中没有找到支持的音频文件")
        print(f"支持的格式: {', '.join(supported_extensions)}")
        return

    print(f"找到 {len(audio_files)} 个音频文件\n")

    # 存储结果
    results = []

    # 处理每个音频文件
    for i, audio_path in enumerate(audio_files):
        filename = os.path.basename(audio_path)
        print(f"处理 [{i+1}/{len(audio_files)}]: {filename}")

        try:
            emotion, confidence = recognizer.predict_emotion(audio_path)

            result = {
                "filename": filename,
                "emotion": emotion,
                "confidence": round(confidence, 4),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            results.append(result)
            print(f"  -> 情绪: {emotion}, 置信度: {confidence:.4f}")

        except Exception as e:
            print(f"  -> 处理失败: {e}")
            result = {
                "filename": filename,
                "emotion": "error",
                "confidence": 0.0,
                "error_message": str(e),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            results.append(result)

    # 保存结果到CSV文件
    if output_csv_path:
        df = pd.DataFrame(results)
        df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
        print(f"\n结果已保存到: {output_csv_path}")

    # 显示统计摘要
    emotions_found = [r["emotion"] for r in results if r["emotion"] != "error"]
    if emotions_found:
        print(f"\n情绪分布统计:")
        from collections import Counter
        counter = Counter(emotions_found)
        for emotion, count in counter.most_common():
            percentage = (count / len(emotions_found)) * 100
            print(f"  {emotion}: {count} 个文件 ({percentage:.1f}%)")

    return results


def create_sample_dataset_structure():
    """创建示例数据集目录结构"""
    base_dir = "sample_dataset"
    emotions = ["neutral", "calm", "happy", "sad", "angry", "fearful", "disgust", "surprised"]

    os.makedirs(base_dir, exist_ok=True)

    for emotion in emotions:
        emotion_dir = os.path.join(base_dir, emotion)
        os.makedirs(emotion_dir, exist_ok=True)
        print(f"创建目录: {emotion_dir}")

    print(f"\n示例数据集结构已创建在 '{base_dir}' 目录中")
    print("请将您的音频文件按情绪分类放入相应的子目录中")


def main():
    parser = argparse.ArgumentParser(description="语音情绪识别 - 批量处理工具（即开即用，无需训练）")
    parser.add_argument("--input", "-i", type=str, help="输入音频文件夹路径")
    parser.add_argument("--output", "-o", type=str, help="输出CSV文件路径（可选，默认自动生成）")
    parser.add_argument("--create-dirs", action="store_true", help="创建示例数据集目录结构")

    args = parser.parse_args()

    if args.create_dirs:
        create_sample_dataset_structure()
        return

    if args.input:
        if not os.path.exists(args.input):
            print(f"错误: 输入文件夹不存在 - {args.input}")
            return

        output_path = args.output or f"emotion_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        batch_predict_from_folder(args.input, output_path)
    else:
        print("语音情绪识别 - 批量处理工具")
        print("=" * 40)
        print("基于 HuggingFace 预训练模型，即开即用，无需训练")
        print()
        print("使用方法:")
        print("  python batch_process.py --input <音频文件夹路径>")
        print()
        print("参数说明:")
        print("  --input, -i    输入音频文件夹路径（必选）")
        print("  --output, -o   输出CSV文件路径（可选，默认自动生成）")
        print("  --create-dirs  创建示例数据集目录结构")
        print()
        print("示例:")
        print("  python batch_process.py --input ./my_audios")
        print("  python batch_process.py --create-dirs")


if __name__ == "__main__":
    main()
