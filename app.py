import sys
import re
import time
import tempfile
import subprocess
import os
from difflib import SequenceMatcher
from openai import OpenAI
sys.stdout.reconfigure(encoding="utf-8")

import gradio as gr
import yt_dlp
from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator

model = None


def load_model():
    global model
    if model is None:
        print("加载模型中...")
        model = WhisperModel("large-v3", device="cpu", compute_type="int8")
        print("模型加载完成")
    return model


def fmt_srt(s):
    h, m = int(s // 3600), int((s % 3600) // 60)
    sec, ms = int(s % 60), int((s % 1) * 1000)
    return f"{h:02}:{m:02}:{sec:02},{ms:03}"


def safe_translate(translator, text, retries=3):
    for _ in range(retries):
        try:
            return translator.translate(text)
        except Exception:
            time.sleep(1)
    return text


def download_video(url):
    """用 yt-dlp 下载视频到临时目录，返回文件路径"""
    tmp_dir = tempfile.mkdtemp()
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": os.path.join(tmp_dir, "video.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        ext = info.get("ext", "mp4")
    return os.path.join(tmp_dir, f"video.{ext}")


def burn_subtitles(video_path, srt_path):
    out = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    out.close()
    srt_escaped = srt_path.replace("\\", "/").replace(":", "\\:")
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"subtitles='{srt_escaped}'",
        "-c:a", "copy",
        out.name,
    ]
    subprocess.run(cmd, capture_output=True)
    return out.name


def transcribe_and_translate(video_path, progress, is_audio=False):
    m = load_model()
    translator = GoogleTranslator(source="ko", target="zh-CN")

    progress(0.3, desc="识别韩文中...")
    segments, _ = m.transcribe(video_path, language="ko", beam_size=5)
    segments = list(segments)

    if not segments:
        return None, None, None, "未识别到语音内容"

    progress(0.6, desc=f"翻译 {len(segments)} 段字幕...")
    srt_lines = []
    for i, seg in enumerate(segments):
        zh = safe_translate(translator, seg.text.strip())
        srt_lines.append(
            f"{i+1}\n{fmt_srt(seg.start)} --> {fmt_srt(seg.end)}\n{seg.text.strip()}\n{zh}\n"
        )
        progress(0.6 + 0.3 * (i + 1) / len(segments),
                 desc=f"翻译中 {i+1}/{len(segments)}")

    srt_file = tempfile.NamedTemporaryFile(
        delete=False, suffix=".srt", mode="w", encoding="utf-8"
    )
    srt_file.write("\n".join(srt_lines))
    srt_file.close()

    preview_text = "\n".join(srt_lines)

    if is_audio:
        # 音频模式：返回音频播放器，不烧录视频
        return (
            gr.Video(visible=False),
            gr.Audio(value=video_path, visible=True),
            srt_file.name,
            f"完成！共 {len(segments)} 段字幕\n\n{preview_text}",
        )
    else:
        progress(0.92, desc="生成预览视频...")
        preview_video = burn_subtitles(video_path, srt_file.name)
        return (
            gr.Video(value=preview_video, visible=True),
            gr.Audio(visible=False),
            srt_file.name,
            f"完成！共 {len(segments)} 段字幕\n\n{preview_text}",
        )


def process_file(video_path, progress=gr.Progress()):
    if video_path is None:
        return None, None, None, "请先上传视频文件"
    progress(0.1, desc="加载模型...")
    return transcribe_and_translate(video_path, progress, is_audio=False)


def process_url(url, progress=gr.Progress()):
    if not url or not url.strip():
        return None, None, None, "请输入视频链接"
    progress(0.05, desc="下载视频中...")
    try:
        video_path = download_video(url.strip())
    except Exception as e:
        return None, None, None, f"下载失败：{e}"
    progress(0.2, desc="下载完成，加载模型...")
    return transcribe_and_translate(video_path, progress, is_audio=False)


def process_auto(url, video_path, audio_path, progress=gr.Progress()):
    if url and url.strip():
        return process_url(url, progress)
    elif video_path:
        return process_file(video_path, progress)
    elif audio_path:
        return process_audio(audio_path, progress)
    else:
        return None, None, None, "请填写链接或上传视频/音频文件"


# ── SRT 合并：旧断句 + 新时间轴 ─────────────────────────────────────
def parse_srt(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    segments = []
    for block in re.split(r"\n\n+", content.strip()):
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        m = re.match(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", lines[1])
        if not m:
            continue
        segments.append({
            "start": m.group(1),
            "end":   m.group(2),
            "text":  "\n".join(lines[2:]).strip(),
        })
    return segments


def time_to_ms(t):
    h, m, s_ms = t.split(":")
    s, ms = s_ms.split(",")
    return int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms)


def ms_to_time(ms):
    h = ms // 3600000; ms %= 3600000
    m = ms // 60000;   ms %= 60000
    s = ms // 1000;    ms %= 1000
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def normalize(text):
    return re.sub(r"[\s\W]", "", text)


def merge_srt_files(old_path, new_path):
    old_segs = parse_srt(old_path)
    new_segs = parse_srt(new_path)

    if not old_segs or not new_segs:
        return None, "SRT 文件解析失败，请检查格式"

    # 新 SRT：每个字符 → (start_ms, end_ms)
    new_flat = ""
    new_char_times = []
    for seg in new_segs:
        s_ms = time_to_ms(seg["start"])
        e_ms = time_to_ms(seg["end"])
        norm = normalize(seg["text"])
        for _ in norm:
            new_char_times.append((s_ms, e_ms))
        new_flat += norm

    # 旧 SRT：每段在拼接文本中的起止位置
    old_flat = ""
    old_positions = []
    for seg in old_segs:
        norm = normalize(seg["text"])
        s = len(old_flat)
        old_flat += norm
        old_positions.append((s, len(old_flat)))

    # 字符级对齐
    matcher = SequenceMatcher(None, old_flat, new_flat, autojunk=False)
    old_to_new = {}
    for a, b, size in matcher.get_matching_blocks():
        for i in range(size):
            old_to_new[a + i] = b + i

    # 生成第三份 SRT
    out_lines = []
    for i, (seg, (s, e)) in enumerate(zip(old_segs, old_positions)):
        mapped = [old_to_new[j] for j in range(s, e) if j in old_to_new]
        if mapped:
            start_ms = new_char_times[min(mapped)][0]
            end_ms   = new_char_times[max(mapped)][1]
        else:
            # 对齐失败时保留旧时间轴
            start_ms = time_to_ms(seg["start"])
            end_ms   = time_to_ms(seg["end"])
        out_lines.append(
            f"{i+1}\n{ms_to_time(start_ms)} --> {ms_to_time(end_ms)}\n{seg['text']}\n"
        )

    out_file = tempfile.NamedTemporaryFile(
        delete=False, suffix=".srt", mode="w", encoding="utf-8"
    )
    out_file.write("\n".join(out_lines))
    out_file.close()

    preview = "\n".join(out_lines[:10])
    return out_file.name, f"完成！共 {len(out_lines)} 段\n\n{preview}{'...' if len(out_lines) > 10 else ''}"


def process_merge(old_srt, new_srt):
    if old_srt is None or new_srt is None:
        return None, "请同时上传两个 SRT 文件"
    return merge_srt_files(old_srt, new_srt)


# ── 智能断句：长韩文 → 适配短视频字幕的分行 ─────────────────────────
def smart_segment_korean(text, max_len=20, min_len=4):
    """
    韩语智能断句：
    - 优先按强终止（句末标点 + 终结语尾 다/까/요/네）切大块
    - 长句再按次级断点切（逗号 > 连接语尾 > 空格）
    - 合并过短的相邻行
    """
    text = text.strip()
    if not text:
        return []

    # 第一步：强终止断点
    strong_breaks = set()
    for m in re.finditer(r"[.!?。！？]\s*", text):
        strong_breaks.add(m.end())
    for m in re.finditer(r"(니다|습니다|ㅂ니다|어요|아요|세요|네요|지요|군요|까요)([\s。.!?，,])", text):
        strong_breaks.add(m.end(1))
    for m in re.finditer(r"(다|까|네)(?=\s)", text):
        strong_breaks.add(m.end())
    strong_breaks = sorted(strong_breaks)

    chunks = []
    last = 0
    for pos in strong_breaks:
        seg = text[last:pos].strip()
        if seg:
            chunks.append(seg)
        last = pos
    tail = text[last:].strip()
    if tail:
        chunks.append(tail)

    # 第二步：长块再切
    result = []
    for chunk in chunks:
        if len(chunk) <= max_len:
            result.append(chunk)
        else:
            result.extend(_secondary_split(chunk, max_len))

    # 第三步：合并过短行
    return _merge_short(result, min_len, max_len)


def _secondary_split(text, max_len):
    """次级切分：标点 > 连接语尾 > 空格"""
    breaks = []
    for m in re.finditer(r"[,，;；]\s*", text):
        breaks.append((m.end(), 1))
    for m in re.finditer(r"(고|며|면서|지만|면|아서|어서|는데|은데|거든|니까|므로|라서)\s+", text):
        breaks.append((m.end(), 2))
    for m in re.finditer(r"\s+", text):
        breaks.append((m.end(), 3))
    breaks.sort()

    result = []
    start = 0
    while start < len(text):
        # 在 [start, start+max_len] 内找最优断点
        candidates = [(pos, prio) for pos, prio in breaks if start < pos <= start + max_len]
        if candidates:
            # 优先级高 + 越靠右（每行尽量饱满）
            candidates.sort(key=lambda x: (x[1], -x[0]))
            end = candidates[0][0]
        else:
            end = min(start + max_len, len(text))
        seg = text[start:end].strip()
        if seg:
            result.append(seg)
        start = end
    return result


def _merge_short(lines, min_len, max_len):
    result = []
    for line in lines:
        if result and len(result[-1]) < min_len and len(result[-1]) + len(line) + 1 <= max_len:
            result[-1] = result[-1] + " " + line
        else:
            result.append(line)
    return result


def process_segment(text, max_len, api_key):
    if not text or not text.strip():
        return "", "请输入韩文文本"
    if not api_key or not api_key.strip():
        return "", "请输入 DeepSeek API Key"

    client = OpenAI(
        api_key=api_key.strip(),
        base_url="https://api.deepseek.com",
    )

    prompt = f"""你是韩语短视频字幕专家。请将以下韩文按短视频字幕规则断句并翻译为中文。

要求：
1. 每段韩文不超过 {int(max_len)} 个字符
2. 按韩语自然语义断句，保持语义完整，不要切断词组
3. 每段配对应的中文翻译（重新翻译，不要直译）
4. 输出格式严格如下，每对之间空一行：

韩文原句
对应中文

只输出断句结果，不要任何解释或标号。

韩文原文：
{text.strip()}"""

    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        result = resp.choices[0].message.content.strip()
        lines = [l for l in result.split("\n") if l.strip()]
        count = len(lines) // 2
        info = f"共 {count} 段"
        return result, info
    except Exception as e:
        return "", f"调用失败：{e}"


# ── UI ──────────────────────────────────────────────────────────────
CSS = """
/* 全局字体 */
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }

/* 顶部 Banner */
#banner {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 8px;
    text-align: center;
    border: none;
}
#banner h1 {
    color: #ffffff;
    font-size: 28px;
    font-weight: 700;
    margin: 0 0 8px 0;
    letter-spacing: -0.5px;
}
#banner p {
    color: #a0aec0;
    font-size: 15px;
    margin: 0;
}

/* Tab 样式 */
.tab-nav button {
    font-size: 15px !important;
    font-weight: 500 !important;
    padding: 10px 24px !important;
    border-radius: 10px !important;
}
.tab-nav button.selected {
    background: #0f3460 !important;
    color: #ffffff !important;
}

/* 主按钮 */
#run-btn {
    background: linear-gradient(135deg, #0f3460, #533483) !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    height: 52px !important;
    color: white !important;
    margin-top: 8px;
    transition: opacity 0.2s;
}
#run-btn:hover { opacity: 0.85; }

/* 卡片容器 */
.gr-panel, .gr-box {
    border-radius: 12px !important;
    border: 1px solid #e2e8f0 !important;
}

/* 输入框 */
textarea, input[type="text"] {
    border-radius: 10px !important;
    font-size: 14px !important;
}

/* 下载按钮区 */
#srt-download .wrap { border-radius: 12px !important; }

/* 字幕文本框 */
#subtitle-text textarea {
    font-family: "SF Mono", "Consolas", monospace !important;
    font-size: 13px !important;
    line-height: 1.7 !important;
    color: #2d3748 !important;
    background: #f8fafc !important;
}

/* 隐藏 Gradio 底部 footer */
footer { display: none !important; }
"""

with gr.Blocks(title="韩文字幕生成器") as demo:

    # Banner
    gr.HTML("""
    <div id="banner">
        <h1>🎬 韩文视频双语字幕生成器</h1>
        <p>支持视频链接 / 本地视频 / 音频文件 → 自动识别韩文 + 翻译为中文</p>
    </div>
    """)

    with gr.Tabs():
        # ── Tab 1: 生成字幕（链接/视频/音频三合一）────
        with gr.Tab("🎬 生成字幕"):
            with gr.Row():
                with gr.Column(scale=2):
                    url_input = gr.Textbox(
                        label="视频链接",
                        placeholder="粘贴 TikTok / YouTube / 抖音 / B站 链接...",
                        lines=1,
                    )
                with gr.Column(scale=1):
                    file_input = gr.File(
                        label="上传视频",
                        file_types=[".mp4", ".mkv", ".avi", ".mov", ".webm"],
                    )
                with gr.Column(scale=1):
                    audio_input = gr.File(
                        label="上传音频",
                        file_types=[".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"],
                    )
            gr.HTML('<p style="color:#999;font-size:12px;margin:4px 0 0 2px;">三选一：填写链接 或 上传视频 或 上传音频</p>')
            gen_btn = gr.Button("生成字幕", variant="primary", elem_id="run-btn")

            # 结果区（在 Tab 内）
            gr.HTML("<div style='height:8px'></div>")
            with gr.Row(equal_height=True):
                with gr.Column(scale=1):
                    video_preview = gr.Video(label="字幕预览", interactive=False)
                    audio_preview = gr.Audio(label="音频播放", interactive=False, visible=False)
                with gr.Column(scale=1):
                    srt_output = gr.File(label="下载 SRT 字幕文件", elem_id="srt-download")
                    log_output = gr.Textbox(
                        label="字幕内容",
                        lines=16,
                        elem_id="subtitle-text",
                        placeholder="字幕将在处理完成后显示在这里...",
                    )

        with gr.Tab("✂️ 智能断句"):
            gr.Markdown("输入韩文长文本，AI 自动断句 + 翻译为中文，输出双语对照。")
            seg_api_key = gr.Textbox(
                label="DeepSeek API Key",
                placeholder="sk-...",
                type="password",
                lines=1,
            )
            with gr.Row():
                seg_input = gr.Textbox(
                    label="韩文原文",
                    lines=8,
                    placeholder="粘贴一整段韩文...",
                    scale=3,
                )
                with gr.Column(scale=1):
                    seg_max_len = gr.Slider(
                        minimum=10, maximum=40, value=20, step=1,
                        label="每段最多字数",
                    )
                    seg_btn = gr.Button("AI 断句 + 翻译", variant="primary", elem_id="run-btn")
            seg_output = gr.Textbox(
                label="双语对照结果（韩文可直接复制到 ElevenLabs）",
                lines=16,
                elem_id="subtitle-text",
            )
            seg_info = gr.Textbox(label="统计", lines=1, interactive=False)

        with gr.Tab("🔀 合并 SRT"):
            gr.Markdown("上传**旧 SRT**（断句准确）和**新 SRT**（ElevenLabs 时间轴），生成断句正确 + 时间轴对齐的第三份 SRT。")
            with gr.Row():
                old_srt_input = gr.File(label="断句准确的文本", file_types=[".srt"])
                new_srt_input = gr.File(label="新 SRT（ElevenLabs 时间轴）", file_types=[".srt"])
            merge_btn = gr.Button("开始合并", variant="primary", elem_id="run-btn")

            # 合并结果区（在 Tab 内）
            gr.HTML("<div style='height:8px'></div>")
            with gr.Row():
                with gr.Column(scale=1):
                    merge_srt_output = gr.File(label="下载合并后的 SRT", elem_id="srt-download")
                with gr.Column(scale=1):
                    merge_log_output = gr.Textbox(
                        label="合并结果预览",
                        lines=16,
                        elem_id="subtitle-text",
                        placeholder="合并完成后在这里预览...",
                    )

    gen_btn.click(fn=process_auto, inputs=[url_input, file_input, audio_input],
                  outputs=[video_preview, audio_preview, srt_output, log_output])
    merge_btn.click(fn=process_merge, inputs=[old_srt_input, new_srt_input],
                    outputs=[merge_srt_output, merge_log_output])
    seg_btn.click(fn=process_segment, inputs=[seg_input, seg_max_len, seg_api_key],
                  outputs=[seg_output, seg_info])

if __name__ == "__main__":
    os.environ["no_proxy"] = "localhost,127.0.0.1"
    os.environ["NO_PROXY"] = "localhost,127.0.0.1"
    print("启动中...")
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False,
                theme=gr.themes.Soft(), css=CSS)
