import os

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


def transcribe_local(media_path, language=None, initial_prompt=None):
    m = load_model()
    kwargs = {
        "beam_size": 5,
        "word_timestamps": True,
        "vad_filter": True,
        "condition_on_previous_text": False,
    }
    if language:
        kwargs["language"] = language
    if initial_prompt and initial_prompt.strip():
        kwargs["initial_prompt"] = initial_prompt.strip()
    segments, _ = m.transcribe(media_path, **kwargs)
    out = []
    for seg in segments:
        words = []
        for w in (seg.words or []):
            text = (w.word or "").strip()
            if not text:
                continue
            words.append({"text": text, "start": float(w.start), "end": float(w.end)})
        out.append({
            "start": seg.start,
            "end": seg.end,
            "text": seg.text.strip(),
            "words": words,
        })
    return out


def value_from(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def transcribe_openai(media_path, api_key, language=None, initial_prompt=None):
    if not api_key or not api_key.strip():
        raise ValueError("请选择 OpenAI API Key 模式时，需要填写 API Key")

    try:
        upload_path = extract_audio_for_api(media_path)
    except Exception:
        upload_path = media_path

    client = OpenAI(api_key=api_key.strip())
    with open(upload_path, "rb") as audio_file:
        kwargs = {
            "model": "whisper-1",
            "file": audio_file,
            "response_format": "verbose_json",
            "timestamp_granularities": ["segment", "word"],
        }
        if language:
            kwargs["language"] = language
        if initial_prompt and initial_prompt.strip():
            kwargs["prompt"] = initial_prompt.strip()
        result = client.audio.transcriptions.create(**kwargs)

    raw_words_all = value_from(result, "words", None) or []
    word_lookup = []
    for w in raw_words_all:
        text = (value_from(w, "word", "") or "").strip()
        if not text:
            continue
        word_lookup.append({
            "text": text,
            "start": float(value_from(w, "start", 0)),
            "end": float(value_from(w, "end", 0)),
        })

    raw_segments = value_from(result, "segments", None)
    if raw_segments:
        out = []
        for seg in raw_segments:
            seg_text = (value_from(seg, "text", "") or "").strip()
            if not seg_text:
                continue
            seg_start = float(value_from(seg, "start", 0))
            seg_end = float(value_from(seg, "end", 0))
            words_in = [
                w for w in word_lookup
                if w["start"] >= seg_start - 0.01 and w["end"] <= seg_end + 0.01
            ]
            out.append({
                "start": seg_start,
                "end": seg_end,
                "text": seg_text,
                "words": words_in,
            })
        return out

    text = (value_from(result, "text", "") or "").strip()
    if not text:
        return []
    if word_lookup:
        return [{
            "start": word_lookup[0]["start"],
            "end": word_lookup[-1]["end"],
            "text": text,
            "words": word_lookup,
        }]
    return [{"start": 0, "end": 0, "text": text, "words": []}]


def transcribe_ggml(media_path, model_path, language=None, initial_prompt=None):
    try:
        from pywhispercpp.model import Model
    except ImportError:
        raise RuntimeError("请先安装 pywhispercpp：pip install pywhispercpp")

    model_path = (model_path or "").strip()
    if not model_path:
        raise ValueError("请填写 GGML 模型文件路径")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"找不到模型文件：{model_path}")

    m = Model(model_path)

    kwargs = {"token_timestamps": True}
    if language:
        kwargs["language"] = language
    if initial_prompt and initial_prompt.strip():
        kwargs["prompt"] = initial_prompt.strip()

    segments = m.transcribe(media_path, **kwargs)

    out = []
    for seg in segments:
        words = []
        for token in (seg.tokens or []):
            text = (token.text or "").strip()
            if not text or text.startswith("["):
                continue
            words.append({
                "text": text,
                "start": token.t0 / 100.0,
                "end": token.t1 / 100.0,
            })
        out.append({
            "start": seg.t0 / 100.0,
            "end": seg.t1 / 100.0,
            "text": seg.text.strip(),
            "words": words,
        })
    return out
