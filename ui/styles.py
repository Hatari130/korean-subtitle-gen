CSS = r"""
:root {
    --paper: #fbfaf6;
    --panel: rgba(255, 255, 255, 0.88);
    --ink: #172321;
    --muted: #6c7470;
    --line: #dde5dd;
    --green: #3e7a58;
    --green-soft: #e9f3ec;
    --sage: #76937d;
    --sand: #f7efe3;
    --amber: #c48755;
    --brown: #b67855;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: var(--paper);
}

.gradio-container {
    max-width: 100% !important;
    background:
        radial-gradient(circle at 55% 8%, rgba(116, 147, 124, 0.18), transparent 24%),
        radial-gradient(circle at 78% 0%, rgba(224, 197, 151, 0.18), transparent 28%),
        linear-gradient(180deg, #fffdf8 0%, #f8faf6 42%, #f5f7f2 100%) !important;
    color: var(--ink);
}

.app-hero {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    min-height: 128px;
    padding: 28px 42px;
    border: 1px solid rgba(88, 125, 96, 0.18);
    border-radius: 0 0 22px 22px;
    background:
        linear-gradient(115deg, rgba(255,255,255,.88), rgba(247,250,245,.72)),
        radial-gradient(circle at 52% 40%, rgba(91, 137, 103, .20), transparent 26%);
    box-shadow: 0 22px 60px rgba(44, 64, 53, 0.09);
    overflow: hidden;
    max-width: 1840px;
    margin: 0 auto;
}

.app-hero::after {
    content: "";
    position: absolute;
    inset: -30% -10% auto 34%;
    height: 180px;
    border: 1px solid rgba(126, 154, 132, .22);
    border-radius: 50%;
    transform: rotate(-8deg);
}

.brand-lockup {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    gap: 22px;
}

.brand-mark {
    display: grid;
    place-items: center;
    width: 60px;
    height: 60px;
    border-radius: 16px;
    background: linear-gradient(145deg, #2f6f4d, #78a982);
    color: #fff;
    font-size: 30px;
    box-shadow: 0 14px 26px rgba(47, 111, 77, .22);
}

.brand-lockup h1 {
    margin: 0 0 8px;
    color: #182421;
    font-size: 34px;
    line-height: 1.08;
    letter-spacing: 0;
}

.brand-lockup h1 span {
    color: var(--green);
}

.brand-lockup p {
    margin: 0;
    color: #5d6762;
    font-size: 15px;
}

.hero-actions {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    gap: 14px;
}

.model-pill,
.status-pill,
.icon-pill {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    min-height: 52px;
    padding: 0 18px;
    border: 1px solid rgba(50, 70, 60, .10);
    border-radius: 14px;
    background: rgba(255, 255, 255, .86);
    color: #23312d;
    box-shadow: 0 12px 26px rgba(36, 52, 44, .08);
}

.model-pill span {
    color: #68746e;
}

.status-pill i {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #4f9567;
}

.icon-pill {
    width: 52px;
    justify-content: center;
    padding: 0;
    border: 0;
    font-size: 20px;
}

div[role="tablist"], .tab-nav {
    display: flex !important;
    gap: 10px !important;
    max-width: 1840px;
    margin: 0 auto !important;
    padding: 0 38px !important;
    border-bottom: 1px solid var(--line) !important;
}

button[role="tab"], .tab-nav button {
    min-width: 190px !important;
    min-height: 56px !important;
    margin: 0 !important;
    padding: 0 34px !important;
    border: 1px solid transparent !important;
    border-radius: 16px 16px 0 0 !important;
    background: transparent !important;
    color: #4e5753 !important;
    font-size: 17px !important;
    font-weight: 750 !important;
}

button[role="tab"][aria-selected="true"], .tab-nav button.selected {
    background: rgba(255,255,255,.92) !important;
    color: var(--green) !important;
    border-color: var(--line) !important;
    border-bottom-color: rgba(255,255,255,.92) !important;
    box-shadow: 0 -6px 20px rgba(34, 62, 46, .06) !important;
}

button[role="tab"]:hover, .tab-nav button:hover {
    color: var(--green) !important;
    background: rgba(255,255,255,.62) !important;
}

.studio-grid,
.result-grid {
    gap: 28px !important;
    align-items: flex-start !important;
    max-width: 1840px;
    margin: 0 auto !important;
    padding: 28px 38px 0;
}

.studio-card {
    align-self: flex-start !important;
    height: auto !important;
    padding: 26px !important;
    border: 1px solid var(--line) !important;
    border-radius: 18px !important;
    background: var(--panel) !important;
    box-shadow: 0 22px 54px rgba(30, 45, 38, .08) !important;
}

.input-card {
    min-height: 420px;
}

.action-card {
    min-height: 420px;
}

.card-heading {
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 22px;
}

.card-heading.compact {
    margin-bottom: 22px;
}

.step-icon,
.mini-icon {
    display: grid;
    place-items: center;
    width: 42px;
    height: 42px;
    border-radius: 14px;
    background: var(--green-soft);
    color: var(--green);
    font-weight: 850;
}

.step-icon.bars {
    background: #f2efe7;
    color: var(--sage);
}

.card-heading h2,
.page-title h2,
.section-title {
    margin: 0;
    color: var(--ink);
    font-size: 23px;
    line-height: 1.2;
    letter-spacing: 0;
}

.card-heading p,
.page-title p {
    margin: 8px 0 0;
    color: var(--muted);
    font-size: 14px;
}

.source-switch .wrap,
.backend-switch .wrap {
    display: grid !important;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
    padding: 0 !important;
    background: transparent !important;
    border: 0 !important;
}

.backend-switch .wrap {
    grid-template-columns: 1fr;
}

.source-switch label,
.backend-switch label {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 10px;
    min-height: 66px;
    border: 1px solid var(--line) !important;
    border-radius: 14px !important;
    background: rgba(255,255,255,.82) !important;
    color: #35413d !important;
    box-shadow: 0 10px 22px rgba(20, 35, 28, .05) !important;
}

.backend-switch label {
    justify-content: flex-start !important;
    min-height: 82px;
    padding: 0 22px !important;
}

.source-switch label:has(input[type="radio"]:checked),
.backend-switch label:has(input[type="radio"]:checked) {
    background: linear-gradient(180deg, #f8fcf8, #eef7f0) !important;
    border-color: #8ab497 !important;
    color: #225c3c !important;
}

.gradio-container input[type="radio"] {
    appearance: none !important;
    width: 22px !important;
    height: 22px !important;
    min-width: 22px !important;
    border: 2px solid #bfc8c0 !important;
    border-radius: 50% !important;
    background: #fff !important;
}

.gradio-container input[type="radio"]:checked {
    border: 7px solid var(--green) !important;
}

.field-title {
    display: inline-flex;
    align-items: center;
    width: fit-content;
    padding: 10px 14px;
    margin: 8px 0 12px;
    border-radius: 12px;
    background: #f2f6ef;
    color: #2e6044;
    font-size: 14px;
    font-weight: 800;
}

.result-grid {
    padding-top: 18px;
}

.result-grid .studio-card {
    min-height: 320px;
}

.source-panel {
    margin-top: 16px !important;
    padding: 16px !important;
    border: 1px solid var(--line) !important;
    border-radius: 15px !important;
    background: rgba(255,255,255,.72) !important;
}

.support-note {
    margin: 18px 2px 0;
    color: var(--muted);
    font-size: 14px;
}

textarea,
input[type="text"],
input[type="password"] {
    border-radius: 14px !important;
    border-color: #d8dfd8 !important;
    background: #fff !important;
    color: var(--ink) !important;
    font-size: 15px !important;
}

textarea::placeholder,
input::placeholder {
    color: #8a948e !important;
}

.api-key-panel {
    margin-bottom: 18px !important;
}

.section-title {
    margin-top: 22px;
    margin-bottom: 16px;
}

#run-btn {
    min-height: 68px !important;
    border: 0 !important;
    border-radius: 14px !important;
    background: linear-gradient(180deg, #d49868, #b87855) !important;
    color: #fff !important;
    font-size: 18px !important;
    font-weight: 850 !important;
    box-shadow: 0 16px 30px rgba(176, 110, 76, .28) !important;
}

.section-divider {
    max-width: 1840px;
    margin: 34px auto 0;
    padding: 0 38px;
}

.section-divider span {
    display: block;
    padding-top: 18px;
    border-top: 1px solid var(--line);
    color: var(--muted);
    font-size: 14px;
    font-weight: 800;
}

.legal-note {
    margin: 14px 0 0;
    text-align: center;
    color: #8a948e;
    font-size: 13px;
}

.page-title {
    padding: 34px 44px 0;
}

.page-title span {
    color: #8e6a4f;
    font-size: 13px;
    font-weight: 850;
    letter-spacing: .08em;
    text-transform: uppercase;
}

.page-title h2 {
    margin-top: 8px;
}

#subtitle-text textarea {
    font-family: "SF Mono", "Consolas", monospace !important;
    line-height: 1.7 !important;
    background: #fbfcfb !important;
}

.upload-container,
.file-preview,
[data-testid="file-upload"] {
    border-color: var(--line) !important;
    background: rgba(255,255,255,.76) !important;
}

.gradio-container [data-testid="block-label"],
.gradio-container [data-testid="block-label"] *,
.gradio-container .block-label,
.gradio-container .block-label *,
.gradio-container .label-wrap,
.gradio-container .label-wrap * {
    background: #f2f6ef !important;
    color: #2e6044 !important;
    border-color: #d8e6d8 !important;
}

.gradio-container [data-testid="file-upload"] *,
.gradio-container .upload-container *,
.gradio-container .file-preview *,
.gradio-container .download *,
.gradio-container .download * {
    color: #2e6044 !important;
    border-color: #d8e6d8 !important;
}

.gradio-container [data-testid="file-upload"] svg,
.gradio-container .upload-container svg,
.gradio-container .file-preview svg,
.gradio-container .download svg,
.gradio-container video + button svg {
    color: #2e6044 !important;
    stroke: #2e6044 !important;
}

.gradio-container [data-testid="file-upload"] a,
.gradio-container .upload-container a,
.gradio-container .file-preview a,
.gradio-container .download a {
    color: #2e6044 !important;
}

a {
    color: #2e6044 !important;
}

footer {
    display: none !important;
}

@media (max-width: 900px) {
    .app-hero,
    .brand-lockup,
    .hero-actions {
        flex-direction: column;
        align-items: flex-start;
    }
    div[role="tablist"], .tab-nav {
        padding: 0 16px !important;
        overflow-x: auto;
    }
    .studio-grid,
    .result-grid {
        padding-left: 16px;
        padding-right: 16px;
        margin-left: 16px;
        margin-right: 16px;
    }
    .source-switch .wrap {
        grid-template-columns: 1fr;
    }
}

.dark,
.dark .gradio-container {
    background: #17201b !important;
    color: #edf5ed !important;
}

.dark .app-hero,
.dark .studio-card {
    background: rgba(28, 40, 33, .88) !important;
    border-color: #3b4a40 !important;
    box-shadow: 0 22px 54px rgba(0, 0, 0, .24) !important;
}

.dark .brand-lockup h1,
.dark .card-heading h2,
.dark .page-title h2,
.dark .section-title {
    color: #f5f8f3 !important;
}

.dark .brand-lockup p,
.dark .card-heading p,
.dark .page-title p,
.dark .legal-note {
    color: #bcc9be !important;
}

.dark button[role="tab"] {
    color: #dfe8df !important;
}

.dark button[role="tab"][aria-selected="true"] {
    background: rgba(34, 49, 40, .94) !important;
    color: #9fd0a8 !important;
    border-color: #3b4a40 !important;
}

.dark .source-switch label,
.dark .backend-switch label,
.dark .source-panel,
.dark textarea,
.dark input[type="text"],
.dark input[type="password"],
.dark #subtitle-text textarea {
    background: #1f2d24 !important;
    border-color: #3b4a40 !important;
    color: #edf5ed !important;
}

.dark .source-switch .wrap,
.dark .backend-switch .wrap,
.dark .source-panel .wrap,
.dark .source-panel .form,
.dark .api-key-panel .wrap,
.dark .api-key-panel .form,
.dark .gradio-container .block,
.dark .gradio-container .block.padded,
.dark .gradio-container .input-container,
.dark .gradio-container .container {
    background: transparent !important;
    border-color: transparent !important;
}

.dark .source-panel {
    background: rgba(21, 31, 25, .58) !important;
}

.dark .source-panel > *,
.dark .api-key-panel > * {
    background: transparent !important;
}

.dark .field-title {
    background: #264732 !important;
    color: #d8f1dc !important;
}

.dark .source-switch label:has(input[type="radio"]:checked),
.dark .backend-switch label:has(input[type="radio"]:checked) {
    background: rgba(42, 73, 52, .90) !important;
    border-color: #76ad82 !important;
    color: #e8f6e9 !important;
}

.dark .source-switch label:not(:has(input[type="radio"]:checked)),
.dark .backend-switch label:not(:has(input[type="radio"]:checked)) {
    background: rgba(28, 42, 34, .84) !important;
    border-color: #44584a !important;
    color: #d0ddd2 !important;
}

.dark .source-switch label span,
.dark .backend-switch label span {
    color: inherit !important;
}

.dark .card-heading p,
.dark .support-note {
    color: #aebcaf !important;
}

.dark #run-btn {
    background: linear-gradient(180deg, #bb845f, #98684f) !important;
}

.dark .field-title {
    background: #264732 !important;
    color: #d8f1dc !important;
}

.dark .gradio-container [data-testid="block-label"],
.dark .gradio-container [data-testid="block-label"] *,
.dark .gradio-container .block-label,
.dark .gradio-container .block-label *,
.dark .gradio-container .label-wrap,
.dark .gradio-container .label-wrap * {
    background: #2e4536 !important;
    color: #bde2c3 !important;
    border-color: #496752 !important;
}

.dark .gradio-container [data-testid="file-upload"] *,
.dark .gradio-container .upload-container *,
.dark .gradio-container .file-preview *,
.dark .gradio-container .download *,
.dark .gradio-container .download * {
    color: #bde2c3 !important;
    border-color: #496752 !important;
}

.dark .gradio-container [data-testid="file-upload"] svg,
.dark .gradio-container .upload-container svg,
.dark .gradio-container .file-preview svg,
.dark .gradio-container .download svg {
    color: #bde2c3 !important;
    stroke: #bde2c3 !important;
}

.dark .source-switch label:has(input[type="radio"]:checked),
.dark .backend-switch label:has(input[type="radio"]:checked) {
    background: rgba(42, 73, 52, .90) !important;
    border-color: #76ad82 !important;
    color: #e8f6e9 !important;
}
"""
