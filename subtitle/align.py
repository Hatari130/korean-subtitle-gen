import json
import tempfile
from difflib import SequenceMatcher

from subtitle.srt import ms_to_time, normalize, parse_srt, read_srt_input, time_to_ms
from subtitle.srt import parse_bilingual_segments, parse_plain_segments


def load_words_json(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    words = []
    for seg in data.get("segments", []):
        for w in seg.get("words", []) or []:
            text = (w.get("text") or "").strip()
            if not text:
                continue
            words.append({
                "text": text,
                "start": float(w.get("start", 0) or 0),
                "end": float(w.get("end", 0) or 0),
            })
    return words


def merge_bilingual_with_words(pairs, words):
    """Word-level align bilingual pairs against Whisper word timestamps."""
    if not pairs or not words:
        return None, "文本或词级 JSON 为空，请检查输入"

    word_flat = ""
    word_char_times = []
    for w in words:
        s_ms = int(w["start"] * 1000)
        e_ms = int(w["end"] * 1000)
        norm = normalize(w["text"])
        n = len(norm)
        for k in range(n):
            if n <= 1:
                cs, ce = s_ms, e_ms
            else:
                cs = s_ms + (e_ms - s_ms) * k // n
                ce = s_ms + (e_ms - s_ms) * (k + 1) // n
            word_char_times.append((cs, ce))
        word_flat += norm

    anchor_flat = ""
    anchor_positions = []
    for pair in pairs:
        anchor = pair["source"] or pair["translation"]
        norm = normalize(anchor)
        if not norm:
            anchor_positions.append(None)
            continue
        s = len(anchor_flat)
        anchor_flat += norm
        anchor_positions.append((s, len(anchor_flat)))

    if not anchor_flat or not word_flat:
        return None, "文本或词级 JSON 中没有可对齐的内容"

    matcher = SequenceMatcher(None, anchor_flat, word_flat, autojunk=False)
    text_to_word = {}
    for a, b, size in matcher.get_matching_blocks():
        for i in range(size):
            text_to_word[a + i] = b + i

    out_lines = []
    last_end_ms = 0
    for i, (pair, pos) in enumerate(zip(pairs, anchor_positions)):
        if pos is None:
            start_ms = last_end_ms
            end_ms = last_end_ms + 1500
        else:
            s, e = pos
            mapped = [text_to_word[j] for j in range(s, e) if j in text_to_word]
            if mapped:
                start_ms = word_char_times[min(mapped)][0]
                end_ms = word_char_times[max(mapped)][1]
            else:
                start_ms = last_end_ms
                end_ms = last_end_ms + 1500
        if end_ms <= start_ms:
            end_ms = start_ms + 500
        last_end_ms = end_ms

        body_lines = []
        if pair["source"]:
            body_lines.append(pair["source"])
        if pair["translation"]:
            body_lines.append(pair["translation"])
        body = "\n".join(body_lines) if body_lines else ""
        out_lines.append(
            f"{i+1}\n{ms_to_time(start_ms)} --> {ms_to_time(end_ms)}\n{body}\n"
        )

    return write_merge_result(out_lines)


def merge_srt_segments(old_segs, new_segs):
    if not old_segs or not new_segs:
        return None, "SRT 文件解析失败，请检查格式"

    new_flat = ""
    new_char_times = []
    for seg in new_segs:
        s_ms = time_to_ms(seg["start"])
        e_ms = time_to_ms(seg["end"])
        norm = normalize(seg["text"])
        for _ in norm:
            new_char_times.append((s_ms, e_ms))
        new_flat += norm

    old_flat = ""
    old_positions = []
    for seg in old_segs:
        norm = normalize(seg["text"])
        s = len(old_flat)
        old_flat += norm
        old_positions.append((s, len(old_flat)))

    matcher = SequenceMatcher(None, old_flat, new_flat, autojunk=False)
    old_to_new = {}
    for a, b, size in matcher.get_matching_blocks():
        for i in range(size):
            old_to_new[a + i] = b + i

    out_lines = []
    for i, (seg, (s, e)) in enumerate(zip(old_segs, old_positions)):
        mapped = [old_to_new[j] for j in range(s, e) if j in old_to_new]
        if mapped:
            start_ms = new_char_times[min(mapped)][0]
            end_ms = new_char_times[max(mapped)][1]
        else:
            start_ms = time_to_ms(seg["start"])
            end_ms = time_to_ms(seg["end"])
        out_lines.append(
            f"{i+1}\n{ms_to_time(start_ms)} --> {ms_to_time(end_ms)}\n{seg['text']}\n"
        )

    return write_merge_result(out_lines)


def merge_text_segments_with_srt(text_segs, new_segs):
    if not text_segs or not new_segs:
        return None, "文本或 SRT 解析失败，请检查内容"

    new_flat = ""
    new_char_times = []
    for seg in new_segs:
        s_ms = time_to_ms(seg["start"])
        e_ms = time_to_ms(seg["end"])
        norm = normalize(seg["text"])
        for _ in norm:
            new_char_times.append((s_ms, e_ms))
        new_flat += norm

    text_flat = ""
    text_positions = []
    for seg in text_segs:
        norm = normalize(seg["text"])
        if not norm:
            continue
        s = len(text_flat)
        text_flat += norm
        text_positions.append((seg["text"], s, len(text_flat)))

    if not text_flat or not new_flat:
        return None, "文本或 SRT 中没有可对齐的字幕内容"

    matcher = SequenceMatcher(None, text_flat, new_flat, autojunk=False)
    text_to_new = {}
    for a, b, size in matcher.get_matching_blocks():
        for i in range(size):
            text_to_new[a + i] = b + i

    out_lines = []
    last_end_ms = 0
    for i, (text, s, e) in enumerate(text_positions):
        mapped = [text_to_new[j] for j in range(s, e) if j in text_to_new]
        if mapped:
            start_ms = new_char_times[min(mapped)][0]
            end_ms = new_char_times[max(mapped)][1]
            last_end_ms = end_ms
        else:
            start_ms = last_end_ms
            end_ms = last_end_ms + 1500
            last_end_ms = end_ms
        out_lines.append(
            f"{i+1}\n{ms_to_time(start_ms)} --> {ms_to_time(end_ms)}\n{text}\n"
        )

    return write_merge_result(out_lines)


def merge_bilingual_with_srt(pairs, new_segs):
    """Align bilingual (source + translation) text against a source-only SRT.

    Each pair becomes ONE SRT block: source line + translation line, sharing
    the timestamps that come from matching the source line to new_segs.
    """
    if not pairs or not new_segs:
        return None, "文本或 SRT 解析失败，请检查内容"

    new_flat = ""
    new_char_times = []
    for seg in new_segs:
        s_ms = time_to_ms(seg["start"])
        e_ms = time_to_ms(seg["end"])
        norm = normalize(seg["text"])
        for _ in norm:
            new_char_times.append((s_ms, e_ms))
        new_flat += norm

    anchor_flat = ""
    anchor_positions = []
    for pair in pairs:
        anchor = pair["source"] or pair["translation"]
        norm = normalize(anchor)
        if not norm:
            anchor_positions.append(None)
            continue
        s = len(anchor_flat)
        anchor_flat += norm
        anchor_positions.append((s, len(anchor_flat)))

    if not anchor_flat or not new_flat:
        return None, "文本或 SRT 中没有可对齐的字幕内容"

    matcher = SequenceMatcher(None, anchor_flat, new_flat, autojunk=False)
    text_to_new = {}
    for a, b, size in matcher.get_matching_blocks():
        for i in range(size):
            text_to_new[a + i] = b + i

    out_lines = []
    last_end_ms = 0
    for i, (pair, pos) in enumerate(zip(pairs, anchor_positions)):
        if pos is None:
            start_ms = last_end_ms
            end_ms = last_end_ms + 1500
        else:
            s, e = pos
            mapped = [text_to_new[j] for j in range(s, e) if j in text_to_new]
            if mapped:
                start_ms = new_char_times[min(mapped)][0]
                end_ms = new_char_times[max(mapped)][1]
            else:
                start_ms = last_end_ms
                end_ms = last_end_ms + 1500
        last_end_ms = end_ms

        body_lines = []
        if pair["source"]:
            body_lines.append(pair["source"])
        if pair["translation"]:
            body_lines.append(pair["translation"])
        body = "\n".join(body_lines) if body_lines else ""
        out_lines.append(
            f"{i+1}\n{ms_to_time(start_ms)} --> {ms_to_time(end_ms)}\n{body}\n"
        )

    return write_merge_result(out_lines)


def write_merge_result(out_lines):
    out_file = tempfile.NamedTemporaryFile(
        delete=False, suffix=".srt", mode="w", encoding="utf-8"
    )
    out_file.write("\n".join(out_lines))
    out_file.close()

    preview = "\n".join(out_lines[:10])
    return out_file.name, f"完成！共 {len(out_lines)} 段\n\n{preview}{'...' if len(out_lines) > 10 else ''}"


def merge_srt_files(old_path, new_path):
    return merge_srt_segments(parse_srt(old_path), parse_srt(new_path))


def process_merge(old_srt, new_srt, old_srt_text, new_srt_text):
    old_segs = read_srt_input(old_srt, old_srt_text)
    new_segs = read_srt_input(new_srt, new_srt_text)
    if not old_segs or not new_segs:
        return None, "请上传两个 SRT 文件，或在两个文本框里粘贴 SRT 内容"
    return merge_srt_segments(old_segs, new_segs)


def process_merge_paste_and_upload(accurate_text, words_json_file):
    pairs = parse_bilingual_segments(accurate_text or "")
    if not pairs:
        return None, "请在左侧粘贴断句准确的双语文本"
    if not words_json_file:
        return None, "请在右侧上传 words.json 词级时间戳文件"
    try:
        words = load_words_json(words_json_file)
    except Exception as e:
        return None, f"读取词级 JSON 失败：{e}"
    if not words:
        return None, "词级 JSON 中没有词时间戳"
    return merge_bilingual_with_words(pairs, words)
