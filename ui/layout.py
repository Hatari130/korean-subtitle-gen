import gradio as gr

from config import LOCAL_BACKEND, OPENAI_BACKEND
from services.tts import process_voiceover
from services.workflows import process_auto, switch_backend, switch_source
from subtitle.align import process_merge_paste_and_upload
from subtitle.segment import process_segment
from ui.styles import CSS


with gr.Blocks(title="韩文双语字幕 Studio", css=CSS) as demo:
    gr.HTML("""
    <header class="app-hero">
        <div class="brand-lockup">
            <div class="brand-mark">▣</div>
            <div>
                <h1>韩文双语字幕 <span>Studio</span></h1>
                <p>视频链接 / 本地视频 / 音频文件 → 自动识别韩文 → 翻译为中文 → 生成 SRT</p>
            </div>
        </div>
        <div class="hero-actions">
            <div class="model-pill"><span>模型</span><strong>large-v3</strong></div>
            <div class="status-pill"><i></i>本地模型就绪</div>
            <button class="icon-pill" type="button">◐</button>
            <button class="icon-pill" type="button">⚙</button>
        </div>
    </header>
    """)

    with gr.Tabs(elem_classes=["main-tabs"]):
        with gr.Tab("生成字幕"):
            with gr.Row(equal_height=False, elem_classes=["studio-grid"]):
                with gr.Column(scale=2, elem_classes=["studio-card", "input-card"]):
                    gr.HTML("""
                    <div class="card-heading">
                        <div class="step-icon">✓</div>
                        <div>
                            <h2>1. 输入素材</h2>
                            <p>选择视频或音频素材，开始生成双语字幕</p>
                        </div>
                    </div>
                    """)
                    source_type = gr.Radio(
                        choices=["视频链接", "上传视频", "上传音频"],
                        value="视频链接",
                        show_label=False,
                        elem_classes=["source-switch"],
                    )
                    with gr.Group(visible=True, elem_classes=["source-panel"]) as url_group:
                        gr.HTML('<div class="field-title">视频链接</div>')
                        url_input = gr.Textbox(
                            show_label=False,
                            placeholder="粘贴 TikTok / YouTube / 抖音 / B站 视频链接...",
                            lines=1,
                        )
                    with gr.Group(visible=False, elem_classes=["source-panel"]) as video_group:
                        file_input = gr.File(
                            label="上传视频",
                            file_types=[".mp4", ".mkv", ".avi", ".mov", ".webm"],
                        )
                    with gr.Group(visible=False, elem_classes=["source-panel"]) as audio_group:
                        audio_input = gr.File(
                            label="上传音频",
                            file_types=[".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"],
                        )
                    gr.HTML('<p class="support-note">支持 YouTube、TikTok、抖音、Bilibili 等主流视频平台。</p>')

                with gr.Column(scale=1, elem_classes=["studio-card", "action-card"]):
                    gr.HTML("""
                    <div class="card-heading compact">
                        <div class="step-icon bars">▮</div>
                        <div>
                            <h2>2. 识别方式</h2>
                        </div>
                    </div>
                    """)
                    backend_input = gr.Radio(
                        choices=[LOCAL_BACKEND, OPENAI_BACKEND],
                        value=LOCAL_BACKEND,
                        show_label=False,
                        elem_classes=["backend-switch"],
                    )
                    gr.HTML('<p class="support-note">本地模型免费但首次需下载；OpenAI API 无需下载模型。</p>')
                    with gr.Group(visible=False, elem_classes=["api-key-panel"]) as api_key_group:
                        gr.HTML('<div class="field-title">OpenAI API Key</div>')
                        api_key_input = gr.Textbox(
                            show_label=False,
                            placeholder="填写 sk-...",
                            type="password",
                            lines=1,
                        )
                    gr.HTML('<h2 class="section-title">3. 开始处理</h2>')
                    gen_btn = gr.Button("生成字幕", variant="primary", elem_id="run-btn")
                    gr.HTML('<p class="legal-note">请确保拥有视频的合法使用权</p>')

            gr.HTML('<div class="section-divider"><span>输出结果</span></div>')
            with gr.Row(equal_height=True, elem_classes=["result-grid"]):
                with gr.Column(scale=1, elem_classes=["studio-card"]):
                    video_preview = gr.Video(label="字幕预览", interactive=False)
                    audio_preview = gr.Audio(label="音频播放", interactive=False, visible=False)
                with gr.Column(scale=1, elem_classes=["studio-card"]):
                    srt_output = gr.File(label="下载 SRT 字幕文件", elem_id="srt-download", visible=False)
                    gr.HTML('<div class="field-title">字幕内容</div>')
                    log_output = gr.Textbox(
                        show_label=False,
                        lines=16,
                        elem_id="subtitle-text",
                        placeholder="字幕将在处理完成后显示在这里...",
                    )

        with gr.Tab("智能断句"):
            gr.HTML("""
            <div class="page-title">
                <span>Smart Segmentation</span>
                <h2>智能断句与翻译</h2>
                <p>输入韩文长文本，生成适合短视频字幕的双语分段。</p>
            </div>
            """)
            with gr.Row(elem_classes=["studio-grid"]):
                with gr.Column(scale=2, elem_classes=["studio-card"]):
                    gr.HTML('<div class="field-title">韩文原文</div>')
                    seg_input = gr.Textbox(
                        show_label=False,
                        lines=10,
                        placeholder="粘贴一整段韩文...",
                    )
                with gr.Column(scale=1, elem_classes=["studio-card", "action-card"]):
                    gr.HTML('<div class="field-title">DeepSeek API Key</div>')
                    seg_api_key = gr.Textbox(
                        show_label=False,
                        placeholder="sk-...",
                        type="password",
                        lines=1,
                    )
                    seg_max_len = gr.Slider(
                        minimum=10, maximum=40, value=20, step=1,
                        label="每段最多字数",
                    )
                    seg_btn = gr.Button("AI 断句 + 翻译", variant="primary", elem_id="run-btn")
            with gr.Row(elem_classes=["result-grid"]):
                with gr.Column(scale=2, elem_classes=["studio-card"]):
                    gr.HTML('<div class="field-title">双语对照结果</div>')
                    seg_output = gr.Textbox(
                        show_label=False,
                        lines=16,
                        elem_id="subtitle-text",
                    )
                with gr.Column(scale=1, elem_classes=["studio-card"]):
                    gr.HTML('<div class="field-title">统计</div>')
                    seg_info = gr.Textbox(show_label=False, lines=1, interactive=False)

        with gr.Tab("口播音频生成"):
            gr.HTML("""
            <div class="page-title">
                <span>Voiceover Studio</span>
                <h2>口播音频生成</h2>
                <p>输入口播文案，选择声音和语速，生成可下载的 MP3 音频。</p>
            </div>
            """)
            with gr.Row(elem_classes=["studio-grid"]):
                with gr.Column(scale=2, elem_classes=["studio-card"]):
                    gr.HTML('<div class="field-title">口播文案</div>')
                    voice_text = gr.Textbox(
                        show_label=False,
                        lines=12,
                        placeholder="粘贴要生成口播的文案...",
                    )
                    gr.HTML('<div class="field-title">口播风格提示</div>')
                    voice_instructions = gr.Textbox(
                        show_label=False,
                        lines=3,
                        placeholder="例如：自然、亲切、短视频口播风格，语气有节奏感。",
                    )
                with gr.Column(scale=1, elem_classes=["studio-card", "action-card"]):
                    gr.HTML('<div class="field-title">OpenAI API Key</div>')
                    voice_api_key = gr.Textbox(
                        show_label=False,
                        placeholder="填写 sk-...",
                        type="password",
                        lines=1,
                    )
                    voice_select = gr.Dropdown(
                        choices=["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
                        value="nova",
                        label="声音",
                    )
                    voice_speed = gr.Slider(
                        minimum=0.75,
                        maximum=1.5,
                        value=1.0,
                        step=0.05,
                        label="语速",
                    )
                    voice_btn = gr.Button("生成口播音频", variant="primary", elem_id="run-btn")
            with gr.Row(elem_classes=["result-grid"]):
                with gr.Column(scale=1, elem_classes=["studio-card"]):
                    gr.HTML('<div class="field-title">音频预览</div>')
                    voice_audio = gr.Audio(label="口播音频", interactive=False)
                with gr.Column(scale=1, elem_classes=["studio-card"]):
                    voice_file = gr.File(label="下载 MP3 音频")
                    voice_status = gr.Textbox(show_label=False, lines=3, placeholder="生成状态...")

        with gr.Tab("合并 SRT"):
            gr.HTML("""
            <div class="page-title">
                <span>SRT Alignment</span>
                <h2>合并字幕时间轴</h2>
                <p>左侧粘贴断句准确的文本，右侧上传带时间轴的 SRT，生成新的 SRT。</p>
            </div>
            """)
            with gr.Row(elem_classes=["studio-grid"]):
                with gr.Column(scale=1, elem_classes=["studio-card"]):
                    gr.HTML('<div class="field-title">断句准确的文本</div>')
                    old_srt_text_input = gr.Textbox(
                        show_label=False,
                        lines=18,
                        placeholder="每行一段字幕文本，例如：\n第一段字幕\n第二段字幕\n第三段字幕",
                    )
                with gr.Column(scale=1, elem_classes=["studio-card"]):
                    gr.HTML('<div class="field-title">新时间轴 SRT</div>')
                    new_srt_input = gr.File(label="上传 ElevenLabs 导出的 SRT", file_types=[".srt"])
                    gr.HTML('<p class="hint">右侧只需要上传带时间轴的 SRT 文件。</p>')
            merge_btn = gr.Button("开始合并", variant="primary", elem_id="run-btn")

            with gr.Row(elem_classes=["result-grid"]):
                with gr.Column(scale=1, elem_classes=["studio-card"]):
                    merge_srt_output = gr.File(label="下载合并后的 SRT", elem_id="srt-download")
                with gr.Column(scale=1, elem_classes=["studio-card"]):
                    gr.HTML('<div class="field-title">合并结果预览</div>')
                    merge_log_output = gr.Textbox(
                        show_label=False,
                        lines=16,
                        elem_id="subtitle-text",
                        placeholder="合并完成后在这里预览...",
                    )

    source_type.change(fn=switch_source, inputs=source_type, outputs=[url_group, video_group, audio_group])
    backend_input.change(fn=switch_backend, inputs=backend_input, outputs=api_key_group)
    gen_btn.click(fn=process_auto, inputs=[url_input, file_input, audio_input, backend_input, api_key_input],
                  outputs=[video_preview, audio_preview, srt_output, log_output])
    merge_btn.click(fn=process_merge_paste_and_upload, inputs=[old_srt_text_input, new_srt_input],
                    outputs=[merge_srt_output, merge_log_output])
    seg_btn.click(fn=process_segment, inputs=[seg_input, seg_max_len, seg_api_key],
                  outputs=[seg_output, seg_info])
    voice_btn.click(
        fn=process_voiceover,
        inputs=[voice_text, voice_api_key, voice_select, voice_speed, voice_instructions],
        outputs=[voice_audio, voice_file, voice_status],
    )
