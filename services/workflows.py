import json
import tempfile

import gradio as gr
from deep_translator import GoogleTranslator

from config import LOCAL_BACKEND, OPENAI_BACKEND, GGML_BACKEND
from services.media import burn_subtitles, download_video
from services.transcription import transcribe_local, transcribe_openai, transcribe_ggml
from services.translation import safe_translate
from subtitle.srt import fmt_srt


def _write_words_json(segments):
    payload = {
        "segments": [
            {
                "start": float(seg.get("start", 0) or 0),
                "end": float(seg.get("end", 0) or 0),
                "text": seg.get("text", ""),
                "words": seg.get("words", []),
            }
            for seg in segments
        ]
    }
    f = tempfile.NamedTemporaryFile(
        delete=False, suffix=".words.json", mode="w", encoding="utf-8"
    )
    json.dump(payload, f, ensure_ascii=False, indent=2)
    f.close()
    return f.name


LANG_LABEL_TO_CODE = {
    "自动检测": None,
    "韩文": "ko",
    "日文": "ja",
    "英文": "en",
    "中文": "zh",
}


def transcribe_and_translate(video_path, progress, is_audio=False, backend=LOCAL_BACKEND, api_key="", ggml_model_path="", source_lang_label="自动检测", initial_prompt=""):
    lang_code = LANG_LABEL_TO_CODE.get(source_lang_label)
    translator_source = lang_code if lang_code else "auto"
    translator = GoogleTranslator(source=translator_source, target="zh-CN")

    progress(0.3, desc="识别音频中...")
    try:
        if backend == OPENAI_BACKEND:
            segments = transcribe_openai(video_path, api_key, language=lang_code, initial_prompt=initial_prompt)
        elif backend == GGML_BACKEND:
            segments = transcribe_ggml(video_path, ggml_model_path, language=lang_code, initial_prompt=initial_prompt)
        else:
            segments = transcribe_local(video_path, language=lang_code, initial_prompt=initial_prompt)
    except Exception as e:
        return None, None, None, None, f"识别失败：{e}"

    if not segments:
        return None, None, None, None, "未识别到语音内容"

    words_json_path = _write_words_json(segments)

    progress(0.6, desc=f"翻译 {len(segments)} 段字幕...")
    srt_lines = []
    for i, seg in enumerate(segments):
        text = seg["text"].strip()
        zh = safe_translate(translator, text)
        srt_lines.append(
            f"{i+1}\n{fmt_srt(seg['start'])} --> {fmt_srt(seg['end'])}\n{text}\n{zh}\n"
        )
        progress(
            0.6 + 0.3 * (i + 1) / len(segments),
            desc=f"翻译中 {i+1}/{len(segments)}",
        )

    srt_file = tempfile.NamedTemporaryFile(
        delete=False, suffix=".srt", mode="w", encoding="utf-8"
    )
    srt_file.write("\n".join(srt_lines))
    srt_file.close()

    preview_text = "\n".join(srt_lines)
    summary = f"完成！共 {len(segments)} 段字幕\n\n{preview_text}"

    if is_audio:
        return (
            gr.Video(visible=False),
            gr.Audio(value=video_path, visible=True),
            gr.File(value=srt_file.name, visible=True),
            gr.File(value=words_json_path, visible=True),
            summary,
        )

    progress(0.92, desc="生成预览视频...")
    preview_video = burn_subtitles(video_path, srt_file.name)
    return (
        gr.Video(value=preview_video, visible=True),
        gr.Audio(visible=False),
        gr.File(value=srt_file.name, visible=True),
        gr.File(value=words_json_path, visible=True),
        summary,
    )


def process_file(video_path, backend, api_key, ggml_model_path, source_lang_label, initial_prompt, progress=gr.Progress()):
    if video_path is None:
        return None, None, None, None, "请先上传视频文件"
    progress(0.1, desc="准备识别...")
    return transcribe_and_translate(video_path, progress, is_audio=False, backend=backend, api_key=api_key, ggml_model_path=ggml_model_path, source_lang_label=source_lang_label, initial_prompt=initial_prompt)


def process_audio(audio_path, backend, api_key, ggml_model_path, source_lang_label, initial_prompt, progress=gr.Progress()):
    if audio_path is None:
        return None, None, None, None, "请先上传音频文件"
    progress(0.1, desc="准备识别...")
    return transcribe_and_translate(audio_path, progress, is_audio=True, backend=backend, api_key=api_key, ggml_model_path=ggml_model_path, source_lang_label=source_lang_label, initial_prompt=initial_prompt)


def process_url(url, backend, api_key, ggml_model_path, source_lang_label, initial_prompt, progress=gr.Progress()):
    if not url or not url.strip():
        return None, None, None, None, "请输入视频链接"
    progress(0.05, desc="下载视频中...")
    try:
        video_path = download_video(url.strip())
    except Exception as e:
        return None, None, None, None, f"下载失败：{e}"
    progress(0.2, desc="下载完成，准备识别...")
    return transcribe_and_translate(video_path, progress, is_audio=False, backend=backend, api_key=api_key, ggml_model_path=ggml_model_path, source_lang_label=source_lang_label, initial_prompt=initial_prompt)


def process_auto(url, video_path, audio_path, backend, api_key, ggml_model_path, source_lang_label, initial_prompt="", progress=gr.Progress()):
    if url and url.strip():
        return process_url(url, backend, api_key, ggml_model_path, source_lang_label, initial_prompt, progress)
    if video_path:
        return process_file(video_path, backend, api_key, ggml_model_path, source_lang_label, initial_prompt, progress)
    if audio_path:
        return process_audio(audio_path, backend, api_key, ggml_model_path, source_lang_label, initial_prompt, progress)
    return None, None, None, None, "请填写链接或上传视频/音频文件"


def switch_source(source_type):
    return (
        gr.update(visible=source_type == "视频链接"),
        gr.update(visible=source_type == "上传视频"),
        gr.update(visible=source_type == "上传音频"),
    )


def switch_backend(backend):
    return (
        gr.update(visible=backend == OPENAI_BACKEND),
        gr.update(visible=backend == GGML_BACKEND),
    )
