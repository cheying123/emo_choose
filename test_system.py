"""
语音情绪识别系统测试脚本
用于验证系统各组件是否正常工作
"""
import os
import sys
import tempfile
import numpy as np
import soundfile as sf


def test_imports():
    """测试依赖库导入"""
    print("=" * 50)
    print("测试依赖库导入...")
    print("=" * 50)

    libraries = [
        ("torch", "torch"),
        ("transformers", "transformers"),
        ("librosa", "librosa"),
        ("soundfile", "sf"),
        ("numpy", "np"),
        ("pandas", "pd"),
    ]

    all_ok = True
    for lib_name, alias in libraries:
        try:
            __import__(lib_name)
            print(f"✓ {lib_name} 导入成功")
        except ImportError as e:
            print(f"✗ {lib_name} 导入失败: {e}")
            all_ok = False

    return all_ok


def test_emotion_recognizer():
    """测试情绪识别器基本功能"""
    print("\n" + "=" * 50)
    print("测试情绪识别器...")
    print("=" * 50)

    try:
        from emotion_recognizer import EmotionRecognizer, FeatureExtractor

        # 测试 FeatureExtractor（无需模型）
        print("测试 FeatureExtractor...")
        extractor = FeatureExtractor()
        sample_rate = 16000
        duration = 2
        sample_signal = np.random.randn(sample_rate * duration)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
            sf.write(tmp_path, sample_signal, sample_rate)

        try:
            features = extractor.extract(tmp_path)
            print(f"✓ 特征提取成功，特征维度: {features.shape}")
        finally:
            os.unlink(tmp_path)

        # 测试 EmotionRecognizer 初始化
        # 注意：这个测试会尝试连接 HuggingFace 下载模型
        print("\n测试 EmotionRecognizer（需要网络下载模型）...")
        print("按 Ctrl+C 跳过模型加载测试")

        try:
            recognizer = EmotionRecognizer()
            print(f"✓ EmotionRecognizer 初始化成功")
            print(f"  模型: {recognizer.model_name}")
            print(f"  设备: {recognizer.device}")
            print(f"  支持的情绪: {recognizer.emotions}")

            # 用随机音频测试预测（不检查结果准确性，只检查 API 是否正常）
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                test_path = tmp.name
                sf.write(test_path, np.random.randn(sample_rate * 2), sample_rate)

            try:
                emotion, confidence = recognizer.predict_emotion(test_path)
                print(f"✓ 预测API正常: {emotion} ({confidence:.4f})")
            finally:
                os.unlink(test_path)

            return True

        except Exception as e:
            print(f"  EmotionRecognizer 加载失败（可能是网络问题）: {e}")
            print("  提示: 首次使用需要联网下载模型（约 1.5GB）")
            return False

    except Exception as e:
        print(f"✗ 情绪识别器测试失败: {e}")
        return False


def test_custom_modules():
    """测试自定义模块导入"""
    print("\n" + "=" * 50)
    print("测试自定义模块导入...")
    print("=" * 50)

    modules = ["emotion_recognizer", "batch_process", "gui_app"]

    all_ok = True
    for module_name in modules:
        try:
            __import__(module_name)
            print(f"✓ {module_name} 导入成功")
        except ImportError as e:
            print(f"✗ {module_name} 导入失败: {e}")
            all_ok = False

    return all_ok


def main():
    """运行所有测试"""
    print("语音情绪识别系统 v2.0 测试")
    print("=" * 50)

    tests = [
        ("依赖库导入测试", test_imports),
        ("自定义模块导入测试", test_custom_modules),
        ("情绪识别器功能测试", test_emotion_recognizer),
    ]

    passed = 0
    for name, func in tests:
        print()
        if func():
            passed += 1
        else:
            print(f"  ⚠ {name} 未通过")

    print("\n" + "=" * 50)
    print(f"测试总结: {passed}/{len(tests)} 通过")
    print("=" * 50)

    if passed == len(tests):
        print("\n✓ 所有测试通过！系统工作正常。")
        print("\n您可以：")
        print("  1. python gui_app.py          # 启动图形界面")
        print("  2. python batch_process.py ... # 批量处理")
        print("  3. python demo.py             # 查看演示")
    else:
        print(f"\n请确保已安装所有依赖: pip install -r requirements.txt")
        print("首次使用需要联网下载模型（约 1.5GB）")


if __name__ == "__main__":
    main()
