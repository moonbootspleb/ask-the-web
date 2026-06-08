---
title: Ask the Web
emoji: 🌐
colorFrom: gray
colorTo: blue
sdk: gradio
sdk_version: "6.0.0"
python_version: "3.11"
app_file: app.py
pinned: false
short_description: Perplexity-style web search agent with tool calling and citations.
---

# Ask the Web — Hugging Face Space

Gradio demo for **Project 3**: tool-calling agent that searches DuckDuckGo and cites sources.

| | |
|---|---|
| **Space (HF)** | `moonbootspleb/ask-the-web` |
| **Source (monorepo)** | `BYTEBTYEGO/demos-3/` |
| **Deploy guide** | [DEPLOY.md](DEPLOY.md) |
| **Embedded on** | [moonboots.tech](https://moonboots.tech/blog/building-an-ask-the-web-agent) |

## Tabs

1. **Ask** — chat with web-search agent + sources from last answer
2. **Sources** — raw DuckDuckGo results for any query
3. **Steps** — tool-call trace from the last Ask question

## Space secrets

| Secret | Purpose |
|--------|---------|
| `OLLAMA_BASE_URL` | Remote Ollama via Tailscale Funnel (see [DEPLOY.md](DEPLOY.md)) |
| `OLLAMA_MODEL` | Model override (default `llama3.2:3b`) |

Without `OLLAMA_BASE_URL`, **Sources** still works; **Ask** runs in search-only mode.
