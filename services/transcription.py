from openai import OpenAI
from faster_whisper import WhisperModel

from config import DEFAULT_WHISPER_MODEL
from services.media import extract_audio_for_api

model = None


def load_model():
    global model
    if model is None:
        print("加载模型中...")
        model = WhisperModel(DEFAULT_WHISPER_MODEL, device="cpu", compute_type="int8")
        print("模型加载完成")
    return model


def transcribe_local(media_path):
    m = load_model()
    segments, _ = m.transcribe(media_path, language="ko", beam_size=5)
    return [
        {"start": seg.start, "end": seg.end, "text": seg.text.strip()}
        for seg in segments
    ]


def value_from(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def transcribe_openai(media_path, api_key):
    if not api_key or not api_key.strip():
        raise ValueError("请选择 OpenAI API Key 模式时，需要填写 API Key")

    try:
        upload_path = extract_audio_for_api(media_path)
    except Exception:
        upload_path = media_path

    client = OpenAI(api_key=api_key.strip())
    with open(upload_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="ko",
            response_format="verbose_json",
            timestamp_granularities=["segment"],
        )

    raw_segments = value_from(result, "segments", None)
    if raw_segments:
        return [
            {
                "start": float(value_from(seg, "start", 0)),
                "end": float(value_from(seg, "end", 0)),
                "text": (value_from(seg, "text", "") or "").strip(),
            }
            for seg in raw_segments
            if (value_from(seg, "text", "") or "").strip()
        ]

    text = (value_from(result, "text", "") or "").strip()
    return [{"start": 0, "end": 0, "text": text}] if text else []
