"""
语音情绪识别系统 - 核心模块
使用 HuggingFace Transformers 预训练模型进行多语种语音情绪识别
支持中文、粤语、英语、日语等多种语言

注意：torch/transformers/librosa 为懒加载，避免阻塞 GUI 启动
"""
import os
import warnings
import urllib.request
import urllib.error

# ============================================================
# HuggingFace 镜像自动检测（仅检查连接，不解锁重型依赖）
# ============================================================
_HF_ENDPOINT_TRIED = False

def ensure_hf_endpoint():
    """确保 HF_ENDPOINT 可用，自动切换到国内镜像"""
    global _HF_ENDPOINT_TRIED
    if _HF_ENDPOINT_TRIED:
        return
    _HF_ENDPOINT_TRIED = True

    if os.environ.get("HF_ENDPOINT"):
        return

    candidates = [
        ("https://huggingface.co", "官方源"),
        ("https://hf-mirror.com", "国内镜像"),
    ]

    for url, name in candidates:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            resp = urllib.request.urlopen(req, timeout=3)
            if resp.status == 200:
                if url != "https://huggingface.co":
                    os.environ["HF_ENDPOINT"] = url
                return
        except Exception:
            continue

    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"


# ============================================================
# 情绪识别器
# ============================================================
DEFAULT_MODELS = [
    "CAiRE/SER-wav2vec2-large-xlsr-53-eng-zho-all-age",
]

LABEL_MAP = {
    "angry": "angry", "disgust": "disgust", "disgusted": "disgust",
    "fear": "fearful", "fearful": "fearful", "happy": "happy",
    "neutral": "neutral", "sad": "sad", "surprise": "surprised",
    "surprised": "surprised", "calm": "calm", "excited": "happy",
    "frustrated": "angry", "satisfied": "happy", "worried": "fearful",
    "中性": "neutral", "平静": "calm", "高兴": "happy",
    "悲伤": "sad", "生气": "angry", "害怕": "fearful",
    "厌恶": "disgust", "惊讶": "surprised",
}


class EmotionRecognizer:
    """语音情绪识别器 - 基于 HuggingFace 预训练模型"""

    def __init__(self, model_name=None, device=None, use_auth_token=None, progress_callback=None):
        self.emotions = [
            "neutral", "calm", "happy", "sad",
            "angry", "fearful", "disgust", "surprised",
        ]
        self.model = None
        self.feature_extractor = None
        self.model_name = None
        self.label_map = {}
        self.device = "cpu"

        self._load_model(model_name, use_auth_token, progress_callback)

    def _import_deps(self):
        """懒加载重型依赖（torch、transformers、librosa）"""
        import torch
        global np
        import numpy as np
        global librosa
        import librosa
        global Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor
        from transformers import (
            Wav2Vec2ForSequenceClassification,
            Wav2Vec2FeatureExtractor,
            logging as transformers_logging,
        )
        Wav2Vec2ForSequenceClassification = Wav2Vec2ForSequenceClassification
        Wav2Vec2FeatureExtractor = Wav2Vec2FeatureExtractor

        self._torch = torch
        self._np = np
        self._librosa = librosa
        self._Wav2Vec2ForSequenceClassification = Wav2Vec2ForSequenceClassification
        self._Wav2Vec2FeatureExtractor = Wav2Vec2FeatureExtractor

        # 抑制非关键警告
        try:
            transformers_logging.set_verbosity_error()
        except Exception:
            pass

    def _load_model(self, model_name=None, use_auth_token=None, progress_callback=None):
        """加载预训练模型（首次使用自动下载）"""
        # 先确保镜像检测
        ensure_hf_endpoint()

        # 懒加载重型依赖
        self._import_deps()

        models_to_try = [model_name] if model_name else DEFAULT_MODELS

        # 设备检测
        self.device = "cuda" if self._torch.cuda.is_available() else "cpu"

        # 尝试导入 huggingface_hub
        try:
            from huggingface_hub import snapshot_download, HfApi
            has_hub = True
        except ImportError:
            has_hub = False

        last_error = None
        for name in models_to_try:
            try:
                print(f"正在加载模型: {name}")
                print(f"运行设备: {self.device}")

                # 如果提供了进度回调，先用 snapshot_download 下载
                if progress_callback and has_hub:
                    try:
                        print("正在下载模型（约 1.5GB），请耐心等待...")
                        snapshot_download(
                            repo_id=name,
                            use_auth_token=use_auth_token,
                            callback=progress_callback,
                        )
                    except Exception as cb_err:
                        print(f"  下载进度回退: {cb_err}")

                self.feature_extractor = self._Wav2Vec2FeatureExtractor.from_pretrained(
                    name, use_auth_token=use_auth_token
                )
                self.model = self._Wav2Vec2ForSequenceClassification.from_pretrained(
                    name, use_auth_token=use_auth_token
                )
                self.model.to(self.device)
                self.model.eval()
                self.model_name = name

                # 构建标签映射
                model_labels = self.model.config.id2label
                if model_labels:
                    for idx, label_text in model_labels.items():
                        mapped = LABEL_MAP.get(label_text.lower(), label_text.lower())
                        self.label_map[int(idx)] = mapped
                else:
                    self.label_map = {i: e for i, e in enumerate(self.emotions)}

                print(f"✓ 模型加载成功: {name}")
                return True

            except Exception as e:
                last_error = e
                print(f"  加载 {name} 失败: {e}")
                continue

        raise RuntimeError(
            f"所有模型加载失败。\n"
            f"最后错误: {last_error}\n\n"
            f"请检查：\n"
            f"1. 网络连接是否正常\n"
            f"2. 是否设置了代理（HF_ENDPOINT）\n"
            f"3. 磁盘空间是否充足（模型约 1.5GB）"
        )

    def predict_emotion(self, audio_path):
        """预测单个音频文件的情绪"""
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"音频文件不存在: {audio_path}")

        speech, sr = self._librosa.load(audio_path, sr=16000)

        inputs = self.feature_extractor(
            speech, sampling_rate=16000, return_tensors="pt", padding=True
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with self._torch.no_grad():
            logits = self.model(**inputs).logits

        scores = self._torch.nn.functional.softmax(logits, dim=-1)
        predicted_id = self._torch.argmax(scores, dim=-1).item()
        confidence = scores[0][predicted_id].item()

        label = self.label_map.get(predicted_id, f"class_{predicted_id}")
        return label, confidence

    def predict_emotions(self, audio_path, top_k=5):
        """获取 Top-K 情绪预测"""
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"音频文件不存在: {audio_path}")

        speech, sr = self._librosa.load(audio_path, sr=16000)

        inputs = self.feature_extractor(
            speech, sampling_rate=16000, return_tensors="pt", padding=True
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with self._torch.no_grad():
            logits = self.model(**inputs).logits

        scores = self._torch.nn.functional.softmax(logits, dim=-1)
        top_scores, top_indices = self._torch.topk(scores, min(top_k, scores.size(-1)))

        results = []
        for score, idx in zip(top_scores[0], top_indices[0]):
            label = self.label_map.get(idx.item(), f"class_{idx.item()}")
            results.append((label, score.item()))

        return results

    def extract_features(self, audio_path):
        """兼容旧版 API：提取音频特征"""
        self._import_deps()
        signal, sr = self._librosa.load(audio_path, duration=3.0)

        mfccs = self._librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=13)
        mel = self._librosa.feature.melspectrogram(y=signal, sr=sr)
        chroma = self._librosa.feature.chroma_stft(y=signal, sr=sr)
        zcr = self._librosa.feature.zero_crossing_rate(signal)
        sc = self._librosa.feature.spectral_centroid(y=signal, sr=sr)
        sbw = self._librosa.feature.spectral_bandwidth(y=signal, sr=sr)

        return self._np.concatenate([
            self._np.mean(mfccs, axis=1),
            self._np.mean(self._librosa.power_to_db(mel), axis=1),
            self._np.mean(chroma, axis=1),
            [self._np.mean(zcr), self._np.mean(sc), self._np.mean(sbw)],
        ])


def main():
    """主函数 - 演示用法"""
    print("=" * 50)
    print("语音情绪识别系统 v2.0")
    print("基于 HuggingFace 预训练模型，支持多语种")
    print("=" * 50)

    recognizer = EmotionRecognizer()
    print(f"\n支持的情绪类别: {recognizer.emotions}")
    print(f"当前模型: {recognizer.model_name}")
    print(f"运行设备: {recognizer.device}")
    print("\n使用方法:")
    print("  emotion, confidence = recognizer.predict_emotion('audio.wav')")
    print("\n启动 GUI 界面:")
    print("  python gui_app.py")


if __name__ == "__main__":
    main()
