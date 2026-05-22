import sys
import time
sys.stdout.reconfigure(encoding="utf-8")
from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator


def safe_translate(translator, text, retries=3):
    for _ in range(retries):
        try:
            return translator.translate(text)
        except Exception as e:
            print(f"  翻译重试: {e}")
            time.sleep(1)
    return text


def fmt(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = int(s % 60)
    ms = int((s % 1) * 1000)
    return f"{h:02}:{m:02}:{sec:02},{ms:03}"


def run(video_path, output=None, model_size="medium"):
    if output is None:
        output = video_path.rsplit(".", 1)[0] + ".srt"

    print(f"模型: {model_size}")
    print(f"输入: {video_path}")
    print(f"输出: {output}")

    print("\n[1/3] 加载 Whisper 模型...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    translator = GoogleTranslator(source="ko", target="zh-CN")

    print("[2/3] 识别韩文...")
    segments, info = model.transcribe(
        video_path,
        language="ko",
        beam_size=5,
    )
    segments = list(segments)
    print(f"  识别完成，共 {len(segments)} 段")

    print("[3/3] 翻译为中文...")
    with open(output, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            zh = safe_translate(translator, seg.text.strip())
            start = fmt(seg.start)
            end = fmt(seg.end)
            f.write(f"{i}\n{start} --> {end}\n{seg.text.strip()}\n{zh}\n\n")
            print(f"  [{i}/{len(segments)}] {seg.text.strip()} → {zh}")

    print(f"\n完成 → {output}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python bilingual.py <视频文件路径>")
        sys.exit(1)
    run(sys.argv[1])
