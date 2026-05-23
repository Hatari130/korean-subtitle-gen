import tempfile

from openai import OpenAI


def generate_voiceover(text, api_key, voice="alloy", speed=1.0, instructions=""):
    if not text or not text.strip():
        return None, None, "请输入口播文案"
    if not api_key or not api_key.strip():
        return None, None, "请输入 OpenAI API Key"

    out = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    out.close()

    client = OpenAI(api_key=api_key.strip())
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text.strip(),
        speed=float(speed),
        response_format="mp3",
        instructions=instructions.strip() or "自然、清晰、适合短视频口播。",
    )
    response.write_to_file(out.name)
    return out.name, out.name, "生成完成"


def process_voiceover(text, api_key, voice, speed, instructions):
    try:
        return generate_voiceover(text, api_key, voice, speed, instructions)
    except Exception as e:
        return None, None, f"生成失败：{e}"
