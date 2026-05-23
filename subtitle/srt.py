import re


def fmt_srt(s):
    h, m = int(s // 3600), int((s % 3600) // 60)
    sec, ms = int(s % 60), int((s % 1) * 1000)
    return f"{h:02}:{m:02}:{sec:02},{ms:03}"


def parse_srt_content(content):
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
            "end": m.group(2),
            "text": "\n".join(lines[2:]).strip(),
        })
    return segments


def parse_srt(path):
    with open(path, encoding="utf-8") as f:
        return parse_srt_content(f.read())


def read_srt_input(uploaded_file, pasted_text):
    if uploaded_file is not None:
        return parse_srt(uploaded_file)
    if pasted_text and pasted_text.strip():
        return parse_srt_content(pasted_text)
    return []


def parse_plain_segments(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return [{"text": line} for line in lines]


def time_to_ms(t):
    h, m, s_ms = t.split(":")
    s, ms = s_ms.split(",")
    return int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms)


def ms_to_time(ms):
    h = ms // 3600000
    ms %= 3600000
    m = ms // 60000
    ms %= 60000
    s = ms // 1000
    ms %= 1000
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def normalize(text):
    return re.sub(r"[\s\W]", "", text)
