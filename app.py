"""Ask-the-Web — Hugging Face Space (Gradio)."""

from __future__ import annotations

import html
import sys
from pathlib import Path

import gradio as gr

_DEMO_ROOT = Path(__file__).resolve().parent
_LAB = _DEMO_ROOT.parent / "project_3"

if (_DEMO_ROOT / "agent_core.py").exists():
    sys.path.insert(0, str(_DEMO_ROOT))
elif (_LAB / "agent_core.py").exists():
    sys.path.insert(0, str(_LAB))

import agent_core  # noqa: E402
from theme import (  # noqa: E402
    ASK_THE_WEB_HERO_HTML,
    EVERSTORM_CHAT_JS,
    HAIRLINE,
    INK,
    MOONBOOTS_CSS,
    ORBITAL,
    build_moonboots_theme,
)

EXAMPLE_QUESTIONS = [
    "What is the latest news about SpaceX?",
    "What are the main features of Python 3.13?",
    "Who won the most recent Formula 1 championship?",
]

WELCOME_MESSAGE = [
    {
        "role": "assistant",
        "content": (
            "Hi — I'm an **ask-the-web** research assistant. I search DuckDuckGo, "
            "reason over results, and cite sources. Try a question below."
        ),
    }
]


def _status_banner() -> str | None:
    backend = agent_core.llm_backend_name()
    if agent_core.get_llm() is None:
        return (
            f"**Search-only mode** — LLM not reachable (`{backend}`). "
            "Set **OLLAMA_BASE_URL** in Space secrets (Tailscale Funnel + `llama3.2:3b`). "
            "The **Sources** tab still returns raw search results."
        )
    return f"**LLM:** `{backend}`"


def _format_sources_html(sources: list[dict]) -> str:
    if not sources:
        return "<p style='color:rgba(255,255,255,0.5);'>No sources yet.</p>"
    blocks = []
    for i, s in enumerate(sources, 1):
        title = html.escape(s.get("title") or "Source")
        url = html.escape(s.get("url") or "")
        snippet = html.escape(s.get("snippet") or "")
        link = f'<a href="{url}" target="_blank" rel="noopener" style="color:#8edce6;">{title}</a>'
        snippet_html = (
            f'<p style="margin:8px 0 0;color:rgba(255,255,255,0.55);font-size:0.9em;">{snippet}</p>'
            if snippet
            else ""
        )
        blocks.append(
            f'<div style="margin:8px 0;padding:12px;border:1px solid {HAIRLINE};'
            f'border-radius:0.75rem;background:{ORBITAL};">'
            f'<p style="margin:0 0 6px;color:{INK};font-family:monospace;">[{i}] {link}</p>'
            f'<p style="margin:0;color:rgba(255,255,255,0.45);font-size:0.85em;">{url}</p>'
            f"{snippet_html}</div>"
        )
    return "".join(blocks)


def _format_steps_html(steps: list[dict]) -> str:
    if not steps:
        return "<p style='color:rgba(255,255,255,0.5);'>No tool steps yet. Ask a question on the **Ask** tab.</p>"
    blocks = []
    for i, step in enumerate(steps, 1):
        tool = html.escape(step.get("tool", "tool"))
        inp = html.escape(step.get("input", ""))
        out = html.escape((step.get("output") or "")[:1200])
        input_html = (
            f'<p style="margin:8px 0 0;color:rgba(255,255,255,0.55);"><strong>Input:</strong> {inp}</p>'
            if inp
            else ""
        )
        output_html = (
            f'<pre style="margin:8px 0 0;white-space:pre-wrap;color:rgba(255,255,255,0.55);font-size:0.85em;">{out}</pre>'
            if out
            else ""
        )
        blocks.append(
            f'<details style="margin:8px 0;border:1px solid {HAIRLINE};'
            f'border-radius:0.75rem;padding:8px 12px;background:{ORBITAL};" open>'
            f'<summary style="cursor:pointer;color:{INK};font-family:monospace;">'
            f"Step {i}: {tool}</summary>{input_html}{output_html}</details>"
        )
    return "".join(blocks)


def stage_user_message(message: str, history: list[dict]) -> tuple[list[dict], dict]:
    if not message.strip():
        return history, gr.update()
    return history + [{"role": "user", "content": message.strip()}], gr.update(value="", interactive=False)


def complete_assistant_response(
    history: list[dict],
) -> tuple[list[dict], dict, str, str, dict]:
    if not history or history[-1].get("role") != "user":
        return history, {}, "", "", gr.update(interactive=True)
    question = history[-1]["content"]
    result = agent_core.invoke_with_trace(question)
    answer = result["answer"]
    if not result.get("llm_available"):
        answer = (
            f"_{agent_core.NO_LLM_MESSAGE}_\n\n**Raw search preview:**\n\n"
            f"{agent_core.format_search_results(result.get('sources', []))}"
        )
    return (
        history + [{"role": "assistant", "content": answer}],
        result,
        _format_sources_html(result.get("sources") or []),
        _format_steps_html(result.get("tool_steps") or []),
        gr.update(interactive=True),
    )


def run_sources_only(query: str) -> str:
    if not query.strip():
        return "Enter a search query."
    return _format_sources_html(agent_core.search_web_raw(query))


def clear_chat() -> tuple:
    return WELCOME_MESSAGE, {}, "", "", gr.update(interactive=True)


_moonboots_theme = build_moonboots_theme()

with gr.Blocks(title="Ask the Web", fill_width=True) as demo:
    gr.HTML(ASK_THE_WEB_HERO_HTML)
    _banner = _status_banner()
    if _banner:
        gr.Markdown(_banner)

    last_result = gr.State({})

    with gr.Tabs():
        with gr.Tab("Ask"):
            with gr.Column(elem_classes="everstorm-chat-shell"):
                chatbot = gr.Chatbot(
                    value=WELCOME_MESSAGE,
                    height=420,
                    show_label=False,
                    layout="bubble",
                    autoscroll=True,
                    elem_classes="everstorm-chat-messages",
                )
                with gr.Column(elem_classes="everstorm-chat-composer"):
                    with gr.Row(elem_classes="everstorm-chat-input-row"):
                        chat_in = gr.Textbox(
                            show_label=False,
                            lines=1,
                            max_lines=6,
                            placeholder="Ask anything that needs a web search…",
                            autofocus=True,
                            elem_id="everstorm-chat-input",
                            container=False,
                            submit_btn=False,
                            scale=20,
                        )
                        chat_btn = gr.Button(
                            "↑",
                            elem_id="everstorm-chat-send",
                            elem_classes="everstorm-chat-send-btn",
                            scale=0,
                            min_width=44,
                        )
                    with gr.Row(elem_classes="everstorm-chat-toolbar"):
                        clear_btn = gr.Button("Clear chat", scale=0)
            ask_sources = gr.HTML(label="Sources from last answer")
            gr.Examples(examples=[[q] for q in EXAMPLE_QUESTIONS], inputs=chat_in)

        with gr.Tab("Sources"):
            src_q = gr.Textbox(label="Search query", lines=2, placeholder="e.g. latest AI agent frameworks")
            src_btn = gr.Button("Search", variant="primary")
            src_out = gr.HTML()
            src_btn.click(run_sources_only, inputs=src_q, outputs=src_out)
            gr.Examples(examples=[[q] for q in EXAMPLE_QUESTIONS], inputs=src_q)

        with gr.Tab("Steps"):
            gr.Markdown("Tool-call trace from your last **Ask** question.")
            steps_out = gr.HTML()

    _submit = dict(fn=stage_user_message, inputs=[chat_in, chatbot], outputs=[chatbot, chat_in])
    _reply = dict(
        fn=complete_assistant_response,
        inputs=[chatbot],
        outputs=[chatbot, last_result, ask_sources, steps_out, chat_in],
    )
    chat_btn.click(**_submit).then(**_reply)
    chat_in.submit(**_submit).then(**_reply)
    clear_btn.click(clear_chat, outputs=[chatbot, last_result, ask_sources, steps_out, chat_in])

demo.launch(
    ssr_mode=False,
    theme=_moonboots_theme,
    css=MOONBOOTS_CSS,
    js=EVERSTORM_CHAT_JS,
)
