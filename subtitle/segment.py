import re

from openai import OpenAI


def smart_segment_korean(text, max_len=20, min_len=4):
    text = text.strip()
    if not text:
        return []

    strong_breaks = set()
    for m in re.finditer(r"[.!?。！？]\s*", text):
        strong_breaks.add(m.end())
    for m in re.finditer(r"(습니다|습니까|이에요|예요|네요|어요|아요|죠|다)([\s。.!?！？])", text):
        strong_breaks.add(m.end(1))
    for m in re.finditer(r"(요|다)(?=\s)", text):
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

    result = []
    for chunk in chunks:
        if len(chunk) <= max_len:
            result.append(chunk)
        else:
            result.extend(_secondary_split(chunk, max_len))

    return _merge_short(result, min_len, max_len)


def _secondary_split(text, max_len):
    breaks = []
    for m in re.finditer(r"[,，、]\s*", text):
        breaks.append((m.end(), 1))
    for m in re.finditer(r"(지만|는데|면서|그리고|그래서|그러면|때문에|니까)\s+", text):
        breaks.append((m.end(), 2))
    for m in re.finditer(r"\s+", text):
        breaks.append((m.end(), 3))
    breaks.sort()

    result = []
    start = 0
    while start < len(text):
        candidates = [(pos, prio) for pos, prio in breaks if start < pos <= start + max_len]
        if candidates:
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
        return "", "请输入需要断句的文本"
    if not api_key or not api_key.strip():
        return "", "请输入 DeepSeek API Key"

    client = OpenAI(
        api_key=api_key.strip(),
        base_url="https://api.deepseek.com",
    )

    prompt = f"""你是短视频字幕专家。请将以下文本按短视频字幕规则断句并翻译为中文。

要求：
1. 每段原文不超过 {int(max_len)} 个字符
2. 按原文自然语义断句，保持语义完整，不要切断词组
3. 每段配对应的中文翻译（重新翻译，不要直译）
4. 输出格式严格如下，每对之间空一行：

原句
对应中文

只输出断句结果，不要任何解释或标号。

原文：
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
