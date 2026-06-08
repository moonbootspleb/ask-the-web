"""Gradio theme aligned with COMPANYSITE / DESIGN.md (moonboots.tech)."""

import gradio as gr

# DESIGN.md tokens
CANVAS = "#070708"
CANVAS_RAISED = "#0f1012"
ORBITAL = "#14151a"
BRAND = "#707070"
BRAND_BRIGHT = "#8a8a8a"
INK = "#f4f4f5"
BODY = "rgba(255, 255, 255, 0.55)"
MUTE = "rgba(255, 255, 255, 0.38)"
HAIRLINE = "rgba(255, 255, 255, 0.08)"
HAIRLINE_STRONG = "rgba(255, 255, 255, 0.15)"
GLOW = "rgba(112, 112, 112, 0.18)"

EMBED_PAD_X = "1rem"
EMBED_PAD_X_SM = "1.5rem"
EMBED_PAD_Y = "0.75rem"

FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@"
    "0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&family=JetBrains+Mono:wght@400;"
    "500&family=Syne:wght@600&display=swap');"
)

MOONBOOTS_CSS = f"""
{FONT_IMPORT}

:root, .gradio-container {{
    --moonboots-canvas: {CANVAS};
    --moonboots-raised: {CANVAS_RAISED};
    --moonboots-orbital: {ORBITAL};
    --moonboots-brand: {BRAND};
    --moonboots-brand-bright: {BRAND_BRIGHT};
}}

html, body {{
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
    background: {CANVAS} !important;
}}

.gradio-container {{
    background: {CANVAS} !important;
    font-family: 'DM Sans', ui-sans-serif, system-ui, sans-serif !important;
    color: {INK} !important;
    width: 100% !important;
    max-width: none !important;
    min-width: 0 !important;
    padding: {EMBED_PAD_Y} {EMBED_PAD_X} 1rem {EMBED_PAD_X} !important;
    margin: 0 auto !important;
    box-sizing: border-box !important;
}}

@media (min-width: 640px) {{
    .gradio-container {{
        padding: 1rem {EMBED_PAD_X_SM} 1.25rem {EMBED_PAD_X_SM} !important;
    }}
}}

.gradio-container .main,
.gradio-container .wrap,
.gradio-container .contain,
.gradio-container .panel,
.gradio-container .tabs,
.gradio-container .tabitem,
.gradio-container .column,
.gradio-container .row,
.gradio-container footer {{
    background: transparent !important;
    width: 100% !important;
    max-width: none !important;
    min-width: 0 !important;
    box-sizing: border-box !important;
}}

.gradio-container .main {{ padding: 0 !important; }}
.gradio-container .wrap,
.gradio-container .contain {{
    padding: 0 !important;
    gap: 0.5rem !important;
}}

.gradio-container > .main,
.gradio-container .main.fillable,
.gradio-container .fillable:not(.gradio-container) {{
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
}}

.gradio-container .tabs {{
    margin-top: 0.15rem !important;
    gap: 0.35rem !important;
}}

.gradio-container .tabitem {{
    padding-top: 0.25rem !important;
    gap: 0.5rem !important;
}}

.gradio-container .tab-nav {{
    margin-bottom: 0 !important;
    gap: 0.25rem !important;
}}

.gradio-container .tab-nav button {{
    font-family: 'JetBrains Mono', ui-monospace, monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: {MUTE} !important;
    border-color: {HAIRLINE} !important;
    background: transparent !important;
}}

.gradio-container .tab-nav button.selected {{
    color: {INK} !important;
    border-color: {BRAND} !important;
    background: {GLOW} !important;
}}

.gradio-container .block,
.gradio-container .form,
.gradio-container .panel {{
    background: {CANVAS_RAISED} !important;
    border-color: {HAIRLINE} !important;
    border-radius: 1rem !important;
}}

.gradio-container label span,
.gradio-container .block-title {{
    font-family: 'JetBrains Mono', ui-monospace, monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: {MUTE} !important;
}}

.gradio-container textarea,
.gradio-container input[type="text"] {{
    background: {ORBITAL} !important;
    border: 1px solid {HAIRLINE_STRONG} !important;
    color: {INK} !important;
    border-radius: 0.75rem !important;
    font-family: 'JetBrains Mono', ui-monospace, monospace !important;
}}

/* Chat shell overrides global ORBITAL textarea + secondary fills */
.everstorm-chat-shell textarea,
.everstorm-chat-shell input[type="text"] {{
    background: {CANVAS_RAISED} !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}}

.gradio-container button.primary {{
    background: {BRAND} !important;
    border: none !important;
    color: #fff !important;
    border-radius: 0.75rem !important;
    box-shadow: 0 0 40px {GLOW} !important;
}}

.gradio-container button.primary:hover {{
    background: {BRAND_BRIGHT} !important;
}}

.gradio-container .markdown-prose {{ color: {BODY} !important; }}
footer {{ display: none !important; }}

/* Grok-style chat: scrollable transcript + fixed composer */
.everstorm-chat-shell {{
    --input-background-fill: {CANVAS_RAISED};
    --input-border-color: transparent;
    --input-shadow: none;
    --block-background-fill: {CANVAS_RAISED};
    --background-fill-primary: {CANVAS_RAISED};
    --background-fill-secondary: {CANVAS_RAISED};
    --block-border-color: transparent;
    --block-shadow: none;
    --button-secondary-background-fill: transparent;
    --button-secondary-background-fill-hover: rgba(255, 255, 255, 0.06);
    --button-secondary-border-color: transparent;
    --button-secondary-text-color: {INK};
    --button-secondary-shadow: none;
    --border-color-primary: transparent;
    display: flex !important;
    flex-direction: column !important;
    min-height: min(68vh, 560px) !important;
    max-height: min(78vh, 720px) !important;
    margin: 0.5rem 0 1rem !important;
    background: {CANVAS_RAISED} !important;
    border: 1px solid {HAIRLINE} !important;
    border-radius: 1.25rem !important;
    overflow: hidden !important;
    padding: 0 !important;
    gap: 0 !important;
}}

.everstorm-chat-shell > .form,
.everstorm-chat-shell > .column {{
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
    gap: 0 !important;
}}

.everstorm-chat-messages {{
    flex: 1 1 auto !important;
    min-height: 0 !important;
    overflow: hidden !important;
    border: none !important;
    border-radius: 0 !important;
    background: transparent !important;
    padding: 0 !important;
}}

.everstorm-chat-messages > .form,
.everstorm-chat-messages .block,
.everstorm-chat-messages .wrap,
.everstorm-chat-messages [class*="wrapper"],
.everstorm-chat-messages [class*="chatbot"] {{
    background: {CANVAS_RAISED} !important;
    background-color: {CANVAS_RAISED} !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0.75rem 1rem 0.25rem !important;
    height: 100% !important;
}}

.everstorm-chat-messages .bubble-wrap,
.everstorm-chat-messages [class*="chatbot"] {{
    max-height: 100% !important;
    overflow-y: auto !important;
}}

.everstorm-chat-composer {{
    flex-shrink: 0 !important;
    padding: 0 1rem 0.75rem !important;
    border-top: none !important;
    background: {CANVAS_RAISED} !important;
    gap: 0.35rem !important;
}}

.everstorm-chat-composer > .form,
.everstorm-chat-composer .block {{
    background: {CANVAS_RAISED} !important;
    border: none !important;
    padding: 0 !important;
}}

/* Input row: one continuous surface with the transcript above */
.everstorm-chat-input-row {{
    align-items: flex-end !important;
    gap: 0.35rem !important;
    background: {CANVAS_RAISED} !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0.5rem 0 0 !important;
    margin: 0 !important;
}}

.everstorm-chat-input-row > .form,
.everstorm-chat-input-row .block,
.everstorm-chat-input-row .wrap,
.everstorm-chat-input-row label {{
    background: {CANVAS_RAISED} !important;
    border: none !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}}

#everstorm-chat-input textarea,
#everstorm-chat-input input {{
    background: {CANVAS_RAISED} !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    outline: none !important;
    padding: 0.55rem 0 !important;
    min-height: 2.5rem !important;
    line-height: 1.45 !important;
    color: {INK} !important;
}}

.everstorm-chat-send-btn button,
#everstorm-chat-send button {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: {INK} !important;
    font-size: 1.35rem !important;
    line-height: 1 !important;
    min-width: 2.25rem !important;
    width: 2.25rem !important;
    height: 2.25rem !important;
    padding: 0 !important;
    border-radius: 0.5rem !important;
}}

.everstorm-chat-send-btn button:hover,
#everstorm-chat-send button:hover {{
    background: rgba(255, 255, 255, 0.06) !important;
}}

.everstorm-chat-hint {{
    margin: 0 !important;
    padding: 0 0.15rem !important;
    font-size: 0.72rem !important;
    color: {MUTE} !important;
    font-family: 'JetBrains Mono', ui-monospace, monospace !important;
    letter-spacing: 0.04em !important;
}}

.everstorm-chat-toolbar {{
    align-items: center !important;
    gap: 0.5rem !important;
}}

.everstorm-chat-toolbar button {{
    font-size: 0.8rem !important;
}}

/* Ask-the-Web layout */
.ask-web-hero {{
    width: 100% !important;
}}

.gradio-container .ask-web-hero,
.gradio-container div:has(> .ask-web-hero) {{
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
}}

.ask-web-chat-shell {{
    --input-background-fill: {CANVAS_RAISED};
    --block-background-fill: {CANVAS_RAISED};
    --background-fill-primary: {CANVAS_RAISED};
    --background-fill-secondary: {CANVAS_RAISED};
    --chatbot-body-background: {CANVAS_RAISED};
    display: flex !important;
    flex-direction: column !important;
    min-height: unset !important;
    max-height: none !important;
    margin: 0.25rem 0 0.5rem !important;
    background: {CANVAS_RAISED} !important;
    border: 1px solid {HAIRLINE} !important;
    border-radius: 0.85rem !important;
    overflow: hidden !important;
    padding: 0 !important;
    gap: 0 !important;
    width: 100% !important;
}}

.ask-web-chat-shell > .form,
.ask-web-chat-shell > .column {{
    background: {CANVAS_RAISED} !important;
    border: none !important;
    padding: 0 !important;
    gap: 0 !important;
    width: 100% !important;
}}

.ask-web-chat-messages {{
    flex: 0 0 auto !important;
    min-height: unset !important;
    overflow: hidden !important;
    border: none !important;
    background: {CANVAS_RAISED} !important;
    width: 100% !important;
}}

.ask-web-chat-messages > .form,
.ask-web-chat-messages .block,
.ask-web-chat-messages .wrap,
.ask-web-chat-messages [class*="wrapper"],
.ask-web-chat-messages [class*="chatbot"],
.ask-web-chat-messages [class*="viewport"],
.ask-web-chat-messages [class*="message-row"] {{
    background: {CANVAS_RAISED} !important;
    background-color: {CANVAS_RAISED} !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0.5rem 0.85rem 0.25rem !important;
    height: auto !important;
    min-height: unset !important;
    width: 100% !important;
    max-width: 100% !important;
}}

.ask-web-chat-messages .bubble-wrap,
.ask-web-chat-messages [class*="chatbot"] {{
    max-height: min(40vh, 340px) !important;
    overflow-y: auto !important;
}}

.ask-web-chat-shell .bubble,
.ask-web-chat-shell [class*="message"] .bubble,
.ask-web-chat-shell .message {{
    padding: 0.7rem 0.95rem !important;
    margin: 0.15rem 0 !important;
    border-radius: 0.75rem !important;
    line-height: 1.5 !important;
}}

.ask-web-chat-shell .bot,
.ask-web-chat-shell .bubble.bot {{
    background: {ORBITAL} !important;
    border: 1px solid {HAIRLINE} !important;
    color: {INK} !important;
}}

.ask-web-chat-shell .user,
.ask-web-chat-shell .bubble.user {{
    background: rgba(255, 255, 255, 0.06) !important;
    border: 1px solid {HAIRLINE} !important;
    color: {INK} !important;
}}

.ask-web-chat-shell .message-buttons,
.ask-web-chat-shell [class*="icon-button"],
.ask-web-chat-shell button[aria-label*="Copy"],
.ask-web-chat-shell button[aria-label*="Share"],
.ask-web-chat-shell button[aria-label*="Delete"] {{
    display: none !important;
}}

.ask-web-chat-shell .everstorm-chat-composer {{
    border-top: 1px solid {HAIRLINE} !important;
    padding: 0.55rem 0.85rem 0.7rem !important;
    margin: 0 !important;
    background: {CANVAS_RAISED} !important;
}}

.ask-web-chat-shell #everstorm-chat-input textarea,
.ask-web-chat-shell #everstorm-chat-input input {{
    padding: 0.5rem 0.15rem !important;
}}

.ask-web-chat-shell .ask-web-toolbar {{
    align-items: center !important;
    justify-content: space-between !important;
    gap: 0.75rem !important;
    padding-top: 0.35rem !important;
    margin: 0 !important;
}}

.ask-web-chat-shell .ask-web-toolbar button {{
    width: auto !important;
    min-width: unset !important;
    max-width: max-content !important;
    flex: 0 0 auto !important;
    padding: 0.35rem 0.75rem !important;
    font-size: 0.78rem !important;
    background: transparent !important;
    border: 1px solid {HAIRLINE} !important;
    border-radius: 0.5rem !important;
    color: {MUTE} !important;
}}

.ask-web-chat-shell .ask-web-toolbar .everstorm-chat-hint {{
    flex: 1 1 auto !important;
    text-align: right !important;
    margin: 0 !important;
    padding: 0 !important;
}}

.ask-web-status {{
    margin: 0.25rem 0 0.4rem !important;
    padding: 0.5rem 0.75rem !important;
    font-size: 0.82rem !important;
    line-height: 1.45 !important;
    border-radius: 0.5rem !important;
    background: {ORBITAL} !important;
    border: 1px solid {HAIRLINE} !important;
}}

.ask-web-status p {{
    margin: 0 !important;
}}

.ask-web-sources {{
    margin-top: 0.35rem !important;
}}

.ask-web-sources .block,
.ask-web-sources .wrap,
.ask-web-sources .form {{
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}}

.ask-web-examples {{
    margin-top: 0.5rem !important;
    margin-bottom: 0 !important;
    width: 100% !important;
}}

.ask-web-examples .block,
.ask-web-examples .form,
.ask-web-examples .wrap {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}}

.ask-web-examples .gr-examples,
.ask-web-examples [class*="examples"],
.ask-web-examples table,
.ask-web-examples tbody {{
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 0.5rem !important;
    width: 100% !important;
    border: none !important;
    background: transparent !important;
}}

.ask-web-examples tr {{
    display: inline-flex !important;
    border: none !important;
    background: transparent !important;
}}

.ask-web-examples td {{
    padding: 0 !important;
    border: none !important;
    background: transparent !important;
}}

.ask-web-examples button {{
    margin: 0 !important;
    padding: 0.4rem 0.75rem !important;
    font-size: 0.78rem !important;
    line-height: 1.35 !important;
    border-radius: 999px !important;
    border: 1px solid {HAIRLINE} !important;
    background: {ORBITAL} !important;
    color: {BODY} !important;
    white-space: normal !important;
    text-align: left !important;
    max-width: 100% !important;
}}

.ask-web-examples button:hover {{
    border-color: {HAIRLINE_STRONG} !important;
    color: {INK} !important;
}}
"""

EVERSTORM_CHAT_JS = """
const EVERSTORM_CHAT_BG = '#0f1012';
const ASK_WEB_ORBITAL = '#14151a';

function everstormPaintChatSurface() {
    const shell = document.querySelector('.everstorm-chat-shell, .ask-web-chat-shell');
    if (!shell) return;
    const isAskWeb = shell.classList.contains('ask-web-chat-shell');
    const paint = (el) => {
        if (!el || el.closest('.bubble')) return;
        if (el.classList && el.classList.contains('bubble')) return;
        el.style.setProperty('background-color', EVERSTORM_CHAT_BG, 'important');
        el.style.setProperty('background', EVERSTORM_CHAT_BG, 'important');
        el.style.setProperty('border-color', 'transparent', 'important');
        el.style.setProperty('box-shadow', 'none', 'important');
    };
    shell.querySelectorAll(
        '.block, .form, .wrap, label, textarea, input, [class*="chatbot"], [class*="wrapper"]'
    ).forEach(paint);
    if (isAskWeb) {
        shell.querySelectorAll('.bubble, .bot, .user').forEach((el) => {
            const isUser = el.classList.contains('user') || el.classList.contains('user');
            el.style.setProperty('padding', '0.7rem 0.95rem', 'important');
            el.style.setProperty(
                'background-color',
                isUser ? 'rgba(255,255,255,0.06)' : ASK_WEB_ORBITAL,
                'important'
            );
        });
        shell.querySelectorAll('button').forEach((btn) => {
            const label = (btn.getAttribute('aria-label') || btn.title || '').toLowerCase();
            if (label.includes('copy') || label.includes('share') || label.includes('delete')) {
                btn.style.setProperty('display', 'none', 'important');
            }
        });
    }
    const sendBtn = document.querySelector('#everstorm-chat-send button');
    if (sendBtn) {
        sendBtn.style.setProperty('background', 'transparent', 'important');
        sendBtn.style.setProperty('color', '#f4f4f5', 'important');
    }
}

function everstormChatComposerKeydown(e) {
    const root = document.getElementById('everstorm-chat-input');
    if (!root) return;
    const field = root.querySelector('textarea');
    if (!field || e.target !== field) return;
    if (e.key !== 'Enter') return;
    if (e.shiftKey) return;
    e.preventDefault();
    if (!field.value.trim()) return;
    const send = document.querySelector('#everstorm-chat-send button');
    if (send) send.click();
}

function everstormChatComposerInit() {
    everstormPaintChatSurface();
    document.removeEventListener('keydown', everstormChatComposerKeydown, true);
    document.addEventListener('keydown', everstormChatComposerKeydown, true);
}

everstormChatComposerInit();
const everstormObserver = new MutationObserver(() => everstormChatComposerInit());
everstormObserver.observe(document.body, { childList: true, subtree: true });
"""

THEME_OVERRIDES = {
    "body_background_fill": CANVAS,
    "body_background_fill_dark": CANVAS,
    "background_fill_primary": CANVAS_RAISED,
    "background_fill_secondary": ORBITAL,
    "block_background_fill": CANVAS_RAISED,
    "block_border_color": HAIRLINE,
    "button_primary_background_fill": BRAND,
    "button_primary_background_fill_hover": BRAND_BRIGHT,
    "button_primary_text_color": "#ffffff",
    "input_background_fill": ORBITAL,
    "input_border_color": HAIRLINE_STRONG,
    "border_color_accent": BRAND,
    "color_accent": BRAND,
}


def _apply_theme_overrides(theme, overrides: dict):
    import re

    pending = dict(overrides)
    while pending:
        try:
            return theme.set(**pending)
        except TypeError as err:
            match = re.search(r"unexpected keyword argument '(\w+)'", str(err))
            if not match or match.group(1) not in pending:
                raise
            del pending[match.group(1)]
    return theme


def build_moonboots_theme():
    try:
        font = gr.themes.GoogleFont("DM Sans")
        font_mono = gr.themes.GoogleFont("JetBrains Mono")
    except Exception:
        font = ("DM Sans", "ui-sans-serif", "system-ui", "sans-serif")
        font_mono = ("JetBrains Mono", "ui-monospace", "monospace")

    theme = gr.themes.Base(
        primary_hue=gr.themes.colors.gray,
        secondary_hue=gr.themes.colors.gray,
        neutral_hue=gr.themes.colors.gray,
        font=font,
        font_mono=font_mono,
    )
    return _apply_theme_overrides(theme, THEME_OVERRIDES)


EVERSTORM_HERO_HTML = """
<div style="margin-bottom:1rem;padding-bottom:1rem;border-bottom:1px solid rgba(255,255,255,0.08);">
  <p style="margin:0 0 0.5rem;font-family:'JetBrains Mono',ui-monospace,monospace;font-size:0.75rem;
     letter-spacing:0.18em;text-transform:uppercase;color:rgba(255,255,255,0.38);">
    Everstorm Outfitters · Support
  </p>
  <h1 style="margin:0;font-family:'Syne',ui-sans-serif,system-ui,sans-serif;font-size:1.75rem;
     font-weight:600;color:#ffffff;line-height:1.15;">
    Ask about shipping, returns, sizing &amp; more
  </h1>
</div>
"""

ASK_THE_WEB_HERO_HTML = """
<div class="ask-web-hero" style="margin:0 0 0.5rem;padding:0 0 0.55rem;border-bottom:1px solid rgba(255,255,255,0.08);">
  <p style="margin:0 0 0.3rem;font-family:'JetBrains Mono',ui-monospace,monospace;font-size:0.7rem;
     letter-spacing:0.16em;text-transform:uppercase;color:rgba(255,255,255,0.38);">
    Ask the Web · Tool-calling agent
  </p>
  <h1 style="margin:0;font-family:'Syne',ui-sans-serif,system-ui,sans-serif;font-size:1.35rem;
     font-weight:600;color:#ffffff;line-height:1.25;">
    Search the web, cite your sources
  </h1>
</div>
"""
