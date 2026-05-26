"""
语音情绪识别模型训练脚本（已弃用）
====================================
v2.0 版本使用 HuggingFace 预训练模型，无需训练即可直接使用。

如需训练/微调模型，请使用 HuggingFace 标准训练流程：
  https://huggingface.co/docs/transformers/training

如只需使用情绪识别功能，请直接运行：
  python gui_app.py            # 图形界面
  python batch_process.py ...  # 批量处理
  python demo.py               # 演示
"""
import warnings
import sys


def main():
    print("=" * 60)
    print("  语音情绪识别系统 v2.0")
    print("=" * 60)
    print()
    print("本版本使用 HuggingFace 预训练模型，即开即用，无需训练。")
    print()
    print("使用方法:")
    print("  python gui_app.py                 # 启动图形界面")
    print("  python batch_process.py --input <文件夹>  # 批量处理")
    print("  python demo.py                    # 查看使用示例")
    print()
    print("如需微调模型，请参考:")
    print("  https://huggingface.co/docs/transformers/training")
    print()
    print("当前版本使用的模型:")
    print("  CAiRE/SER-wav2vec2-large-xlsr-53-eng-zho-all-age")
    print("  支持中英文等多语种语音情绪识别")
    print("=" * 60)


if __name__ == "__main__":
    main()
