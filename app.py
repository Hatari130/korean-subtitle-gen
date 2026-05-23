import os
import sys

import gradio as gr

from config import DEFAULT_SERVER_NAME, DEFAULT_SERVER_PORT
from ui.layout import demo

sys.stdout.reconfigure(encoding="utf-8")


if __name__ == "__main__":
    os.environ["no_proxy"] = "localhost,127.0.0.1"
    os.environ["NO_PROXY"] = "localhost,127.0.0.1"
    print("启动中...")
    demo.launch(
        server_name=DEFAULT_SERVER_NAME,
        server_port=DEFAULT_SERVER_PORT,
        share=False,
        theme=gr.themes.Soft(),
    )
