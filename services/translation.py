import time


def safe_translate(translator, text, retries=3):
    for _ in range(retries):
        try:
            return translator.translate(text)
        except Exception:
            time.sleep(1)
    return text
