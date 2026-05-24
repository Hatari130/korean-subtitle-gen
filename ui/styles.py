CSS = r"""
:root {
    --paper: #f8faf6;
    --panel: rgba(255, 255, 255, 0.90);
    --ink: #172321;
    --muted: #6c7470;
    --line: #dde5dd;
    --green: #3e7a58;
    --green-dark: #2b5c40;
    --green-soft: #e9f3ec;
    --green-mid: #76ad82;
    --sage: #76937d;

    /* Unified radius scale */
    --r-sm: 10px;
    --r-md: 14px;
    --r-lg: 18px;
    --r-xl: 22px;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: var(--paper);
}

.gradio-container {
    max-width: 100% !important;
    background:
        radial-gradient(circle at 55% 8%, rgba(116, 147, 124, 0.16), transparent 24%),
        linear-gradient(180deg, #fafcf8 0%, #f5f8f3 100%) !important;
    color: var(--ink);
}

/* ── Hero ── */
.app-hero {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    min-height: 112px;
    padding: 24px 42px;
    border: 1px solid rgba(88, 125, 96, 0.18);
    border-radius: 0 0 var(--r-xl) var(--r-xl);
    background:
        linear-gradient(115deg, rgba(255,255,255,.90), rgba(245,250,243,.76)),
        radial-gradient(circle at 52% 40%, rgba(91,137,103,.18), transparent 26%);
    box-shadow: 0 16px 48px rgba(44, 64, 53, 0.08);
    overflow: hidden;
    max-width: 1840px;
    margin: 0 auto;
}

.app-hero::after {
    content: "";
    position: absolute;
    inset: -30% -10% auto 34%;
    height: 180px;
    border: 1px solid rgba(126, 154, 132, .20);
    border-radius: 50%;
    transform: rotate(-8deg);
}

.brand-lockup {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    gap: 20px;
}

.brand-mark {
    display: grid;
    place-items: center;
    width: 56px;
    height: 56px;
    border-radius: var(--r-md);
    background: linear-gradient(145deg, #2f6f4d, #78a982);
    color: #fff;
    font-size: 26px;
    box-shadow: 0 12px 24px rgba(47, 111, 77, .20);
}

.brand-lockup h1 {
    margin: 0 0 6px;
    color: #182421;
    font-size: 30px;
    line-height: 1.1;
}

.brand-lockup h1 span { color: var(--green); }

.brand-lockup p {
    margin: 0;
    color: #5d6762;
    font-size: 14px;
}

.hero-actions {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    gap: 12px;
}

.model-pill,
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    min-height: 46px;
    padding: 0 16px;
    border: 1px solid rgba(50, 70, 60, .10);
    border-radius: var(--r-md);
    background: rgba(255, 255, 255, .86);
    color: #23312d;
    font-size: 14px;
    box-shadow: 0 8px 20px rgba(36, 52, 44, .06);
}

.model-pill span { color: #68746e; }

.status-pill i {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #4f9567;
}

/* ── Tabs ── */
div[role="tablist"], .tab-nav {
    display: flex !important;
    gap: 8px !important;
    max-width: 1840px;
    margin: 0 auto !important;
    padding: 0 38px !important;
    border-bottom: 1px solid var(--line) !important;
}

button[role="tab"], .tab-nav button {
    min-width: 170px !important;
    min-height: 52px !important;
    margin: 0 !important;
    padding: 0 28px !important;
    border: 1px solid transparent !important;
    border-radius: var(--r-md) var(--r-md) 0 0 !important;
    background: transparent !important;
    color: #4e5753 !important;
    font-size: 15px !important;
    font-weight: 700 !important;
}

button[role="tab"][aria-selected="true"] {
    background: rgba(255,255,255,.94) !important;
    color: var(--green) !important;
    border-color: var(--line) !important;
    border-bottom-color: rgba(255,255,255,.94) !important;
    box-shadow: 0 -4px 16px rgba(34, 62, 46, .05) !important;
}

button[role="tab"]:hover {
    color: var(--green) !important;
    background: rgba(255,255,255,.55) !important;
}

/* ── Layout grids ── */
.studio-grid,
.result-grid {
    gap: 24px !important;
    align-items: stretch !important;
    max-width: 1840px;
    margin: 0 auto !important;
    padding: 24px 38px 0;
}

.result-grid {
    padding-top: 16px;
}

.studio-card {
    align-self: stretch !important;
    height: auto !important;
    display: flex !important;
    flex-direction: column !important;
    padding: 24px !important;
    border: 1px solid var(--line) !important;
    border-radius: var(--r-lg) !important;
    background: var(--panel) !important;
    box-shadow: 0 16px 48px rgba(30, 45, 38, .07) !important;
}

.input-card { min-height: 380px; }
.action-card { min-height: 380px; }
.result-grid .studio-card { min-height: 300px; }

/* ── Card headings (unified across all tabs) ── */
.card-heading {
    display: flex;
    align-items: center;
    gap: 16px;
    min-height: 60px;
    margin-bottom: 20px;
}

.card-heading.compact { min-height: 60px; margin-bottom: 20px; }

.step-icon {
    flex-shrink: 0;
    display: grid;
    place-items: center;
    width: 40px;
    height: 40px;
    border-radius: var(--r-sm);
    background: var(--green-soft);
    color: var(--green);
    font-weight: 850;
}

.step-icon.bars {
    background: rgba(118, 147, 125, .12);
    color: var(--sage);
}

.card-heading h2,
.page-title h2,
.section-title {
    margin: 0;
    color: var(--ink);
    font-size: 20px;
    line-height: 1.2;
}

.card-heading p,
.page-title p {
    margin: 6px 0 0;
    color: var(--muted);
    font-size: 13px;
}

/* ── Source / backend radio ── */
.source-switch .wrap,
.backend-switch .wrap {
    display: grid !important;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 8px;
    padding: 0 !important;
    background: transparent !important;
    border: 0 !important;
}

.backend-switch .wrap { grid-template-columns: 1fr; }

.source-switch label,
.backend-switch label {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px;
    min-height: 62px;
    border: 1px solid var(--line) !important;
    border-radius: var(--r-md) !important;
    background: rgba(255,255,255,.82) !important;
    color: #35413d !important;
    box-shadow: 0 6px 16px rgba(20, 35, 28, .04) !important;
    transition: border-color .15s, background .15s;
}

.backend-switch label {
    justify-content: flex-start !important;
    min-height: 62px;
    padding: 0 18px !important;
}

.source-switch label:has(input[type="radio"]:checked),
.backend-switch label:has(input[type="radio"]:checked) {
    background: linear-gradient(180deg, #f4fbf5, #e8f4ea) !important;
    border-color: var(--green-mid) !important;
    color: var(--green-dark) !important;
}

.gradio-container input[type="radio"] {
    appearance: none !important;
    width: 20px !important;
    height: 20px !important;
    min-width: 20px !important;
    border: 2px solid #bfc8c0 !important;
    border-radius: 50% !important;
    background: #fff !important;
}

.gradio-container input[type="radio"]:checked {
    border: 6px solid var(--green) !important;
}

/* ── Field label chip ── */
.field-title {
    display: inline-flex;
    align-items: center;
    width: fit-content;
    padding: 8px 12px;
    margin: 6px 0 10px;
    border-radius: var(--r-sm);
    background: var(--green-soft);
    color: var(--green-dark);
    font-size: 13px;
    font-weight: 700;
}

/* ── Inputs ── */
textarea,
input[type="text"],
input[type="password"] {
    border-radius: var(--r-sm) !important;
    border-color: #d0d9d0 !important;
    background: #fff !important;
    color: var(--ink) !important;
    font-size: 15px !important;
}

textarea::placeholder,
input::placeholder { color: #8a948e !important; }

.api-key-panel { margin-bottom: 16px !important; }

/* ── Run button (unified green) ── */
#run-btn {
    min-height: 64px !important;
    border: 0 !important;
    border-radius: var(--r-md) !important;
    background: linear-gradient(180deg, #4e9268, #326b4c) !important;
    color: #fff !important;
    font-size: 17px !important;
    font-weight: 800 !important;
    box-shadow: 0 12px 28px rgba(50, 107, 76, .30) !important;
    transition: opacity .15s !important;
}

#run-btn:hover { opacity: .92 !important; }

/* ── Action bar ── */
.action-bar-row {
    max-width: 1840px;
    margin: 20px auto 0 !important;
    padding: 0 38px;
}

.action-bar {
    width: 100%;
    padding: 16px 24px !important;
    border: 1px solid var(--line);
    border-radius: var(--r-lg);
    background: var(--panel);
    box-shadow: 0 16px 48px rgba(30, 45, 38, .07);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    flex-wrap: wrap;
}

.action-bar #run-btn {
    flex: 1 1 auto;
    min-width: 220px;
    max-width: 460px !important;
}

.action-bar .legal-note {
    margin: 0;
    color: var(--muted);
    font-size: 12px;
    white-space: nowrap;
}

/* ── Error banner ── */
.error-banner {
    margin: 12px 0 0;
    padding: 12px 16px;
    border-radius: var(--r-sm);
    background: #fdf2f2;
    border: 1px solid #f0c4c4;
    color: #8b2c2c;
    font-size: 14px;
    display: none;
}

.error-banner.visible { display: block; }

/* ── Section divider ── */
.section-divider {
    max-width: 1840px;
    margin: 28px auto 0;
    padding: 0 38px;
}

.section-divider span {
    display: block;
    padding-top: 16px;
    border-top: 1px solid var(--line);
    color: var(--muted);
    font-size: 13px;
    font-weight: 700;
    letter-spacing: .04em;
    text-transform: uppercase;
}

.legal-note {
    text-align: center;
    color: var(--muted);
    font-size: 12px;
}

/* ── Page title (other tabs) ── */
.page-title {
    display: flex;
    align-items: center;
    gap: 16px;
    min-height: 60px;
    max-width: 1840px;
    margin: 0 auto;
    padding: 24px 38px 0;
}

.page-title .step-icon { flex-shrink: 0; }

.page-title-text span {
    display: block;
    color: var(--muted);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .10em;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.page-title h2 { margin-top: 0; }

/* ── Subtitle textarea mono ── */
#subtitle-text textarea {
    font-family: "SF Mono", "Consolas", monospace !important;
    font-size: 13px !important;
    line-height: 1.7 !important;
    background: #fafcfb !important;
}

/* ── Downloads row ── */
.downloads-row { gap: 12px !important; }

/* ── File upload ── */
.upload-container,
.file-preview,
[data-testid="file-upload"] {
    border-color: var(--line) !important;
    background: rgba(255,255,255,.78) !important;
    border-radius: var(--r-sm) !important;
}

.gradio-container [data-testid="block-label"],
.gradio-container [data-testid="block-label"] *,
.gradio-container .block-label,
.gradio-container .block-label *,
.gradio-container .label-wrap,
.gradio-container .label-wrap * {
    background: var(--green-soft) !important;
    color: var(--green-dark) !important;
    border-color: #c8dfcc !important;
    border-radius: var(--r-sm) !important;
}

.gradio-container [data-testid="file-upload"] *,
.gradio-container .upload-container *,
.gradio-container .file-preview *,
.gradio-container .download * {
    color: var(--green-dark) !important;
    border-color: #c8dfcc !important;
}

.gradio-container [data-testid="file-upload"] svg,
.gradio-container .upload-container svg,
.gradio-container .file-preview svg,
.gradio-container .download svg,
.gradio-container video + button svg {
    color: var(--green) !important;
    stroke: var(--green) !important;
}

a { color: var(--green) !important; }

footer { display: none !important; }

/* ── Responsive ── */
@media (max-width: 1023px) {
    .app-hero {
        flex-direction: column;
        align-items: flex-start;
        gap: 16px;
        min-height: unset;
    }
    div[role="tablist"], .tab-nav {
        padding: 0 16px !important;
        overflow-x: auto;
        gap: 4px !important;
    }
    button[role="tab"] { min-width: 130px !important; padding: 0 16px !important; }
    .studio-grid,
    .result-grid,
    .action-bar-row,
    .section-divider,
    .page-title {
        padding-left: 16px !important;
        padding-right: 16px !important;
    }
    .source-switch .wrap { grid-template-columns: 1fr; }
}

/* ══════════════════════════════════════
   DARK MODE
══════════════════════════════════════ */
.dark,
.dark .gradio-container {
    background: #0c1210 !important;
    color: #e5e8e5 !important;
}

.dark .app-hero {
    background: linear-gradient(115deg, rgba(26,36,30,.97), rgba(18,26,21,.94)) !important;
    border-color: #263028 !important;
    box-shadow: 0 16px 48px rgba(0,0,0,.40) !important;
}

.dark .studio-card {
    background: #111916 !important;
    border: 1px solid #263028 !important;
    box-shadow: 0 16px 48px rgba(0,0,0,.32) !important;
}

.dark .brand-lockup h1 { color: #f0f4f0 !important; }
.dark .brand-lockup h1 span { color: #9fd0a8 !important; }
.dark .brand-lockup p,
.dark .card-heading p,
.dark .page-title p { color: #c0cdc1 !important; }

.dark .card-heading h2,
.dark .page-title h2,
.dark .section-title { color: #eef2ee !important; }

.dark button[role="tab"] { color: #d5ddd5 !important; }
.dark button[role="tab"][aria-selected="true"] {
    background: #111916 !important;
    color: #9fd0a8 !important;
    border-color: #263028 !important;
    border-bottom-color: #111916 !important;
}

.dark div[role="tablist"], .dark .tab-nav {
    border-bottom-color: #263028 !important;
}

/* Inputs */
.dark textarea,
.dark input[type="text"],
.dark input[type="password"],
.dark input[type="number"],
.dark #subtitle-text textarea {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid rgba(255,255,255,.09) !important;
    border-radius: var(--r-sm) !important;
    color: #e5e8e5 !important;
}

.dark textarea::placeholder,
.dark input::placeholder { color: #7a897c !important; }

.dark textarea:focus,
.dark input[type="text"]:focus,
.dark input[type="password"]:focus {
    border-color: #76ad82 !important;
    background: rgba(255,255,255,.06) !important;
    outline: none !important;
}

/* Radio */
.dark .source-switch label,
.dark .backend-switch label {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid rgba(255,255,255,.09) !important;
    border-radius: var(--r-md) !important;
    color: #d5ddd5 !important;
    box-shadow: none !important;
}

.dark .source-switch label:has(input[type="radio"]:checked),
.dark .backend-switch label:has(input[type="radio"]:checked) {
    background: rgba(118,173,130,.14) !important;
    border-color: #76ad82 !important;
    color: #e8f6e9 !important;
}

.dark .source-switch label span,
.dark .backend-switch label span { color: inherit !important; }

.dark .gradio-container input[type="radio"] {
    background: #1a221d !important;
    border-color: #445c4a !important;
}
.dark .gradio-container input[type="radio"]:checked {
    border-color: #76ad82 !important;
    background: #76ad82 !important;
}

/* Strip injected wrappers */
.dark .gradio-container .block,
.dark .gradio-container .block.padded,
.dark .gradio-container .input-container,
.dark .gradio-container .container,
.dark .gradio-container .form,
.dark .gradio-container .wrap,
.dark .api-key-panel,
.dark .api-key-panel > * {
    background: transparent !important;
    border-color: transparent !important;
}

/* Re-apply for actual inputs inside cards */
.dark .studio-card textarea,
.dark .studio-card input[type="text"],
.dark .studio-card input[type="password"],
.dark .studio-card [data-testid="file-upload"],
.dark .studio-card .upload-container,
.dark .studio-card .file-preview {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid rgba(255,255,255,.09) !important;
}

/* Run button dark */
.dark #run-btn {
    background: linear-gradient(180deg, #4d8e66, #2e6044) !important;
    box-shadow: 0 12px 28px rgba(0,0,0,.40) !important;
}

/* Action bar dark */
.dark .action-bar {
    background: #111916 !important;
    border-color: #263028 !important;
    box-shadow: 0 16px 48px rgba(0,0,0,.32) !important;
}

.dark .action-bar .legal-note { color: #8a9a8c !important; }

/* Field title dark */
.dark .field-title {
    background: rgba(118,173,130,.16) !important;
    color: #c4e8cb !important;
}

/* Step icon dark */
.dark .step-icon {
    background: rgba(118,173,130,.14) !important;
    color: #9fd0a8 !important;
}
.dark .step-icon.bars {
    background: rgba(255,255,255,.05) !important;
    color: #c0cdc1 !important;
}

/* Hero pills dark */
.dark .model-pill,
.dark .status-pill {
    background: rgba(255,255,255,.04) !important;
    border-color: rgba(255,255,255,.09) !important;
    color: #e5e8e5 !important;
}
.dark .model-pill span { color: #9aa49b !important; }

/* Section divider dark */
.dark .section-divider span {
    border-top-color: #263028 !important;
    color: #8a9a8c !important;
}

/* Subtitle textarea dark */
.dark #subtitle-text textarea {
    background: rgba(255,255,255,.04) !important;
}

/* File upload dark */
.dark .gradio-container [data-testid="file-upload"],
.dark .gradio-container .upload-container,
.dark .gradio-container .file-preview {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid rgba(255,255,255,.09) !important;
}

.dark .gradio-container [data-testid="block-label"],
.dark .gradio-container [data-testid="block-label"] *,
.dark .gradio-container .block-label,
.dark .gradio-container .block-label *,
.dark .gradio-container .label-wrap,
.dark .gradio-container .label-wrap * {
    background: rgba(118,173,130,.12) !important;
    color: #c4e8cb !important;
    border-color: rgba(255,255,255,.09) !important;
}

.dark .gradio-container [data-testid="file-upload"] *,
.dark .gradio-container .upload-container *,
.dark .gradio-container .file-preview *,
.dark .gradio-container .download * {
    color: #c8d8ca !important;
    border-color: transparent !important;
}

.dark .gradio-container [data-testid="file-upload"] svg,
.dark .gradio-container .upload-container svg,
.dark .gradio-container .file-preview svg,
.dark .gradio-container .download svg {
    color: #9fd0a8 !important;
    stroke: #9fd0a8 !important;
}

.dark a { color: #9fd0a8 !important; }

/* Error banner dark */
.dark .error-banner {
    background: rgba(180,60,60,.14) !important;
    border-color: rgba(180,60,60,.30) !important;
    color: #f0a8a8 !important;
}
"""
