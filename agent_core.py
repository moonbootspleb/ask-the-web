"""Ask-the-Web agent — shared search tool, LangChain agent, and trace helpers."""

from __future__ import annotations

import os
import re
from typing import Any
from urllib.parse import urlparse

from ddgs import DDGS
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
DEFAULT_MAX_RESULTS = 5

SYSTEM_PROMPT = """You are a helpful research assistant that answers questions using web search.

Rules:
1) Use the search_web tool when you need current or factual information from the internet.
2) Base your answer on search results — do not invent facts.
3) Cite sources inline using markdown links: [title](url).
4) If search results are insufficient, say what is missing.
5) Be concise and direct."""

SYNTHESIS_PROMPT = """You are a helpful research assistant. You are given DuckDuckGo search results.

Rules:
1) Answer ONLY from the search results — do not invent facts.
2) Cite sources inline using markdown links: [title](url).
3) If results are insufficient, say what is missing.
4) Be concise and direct. Do not output JSON or tool calls."""

NO_LLM_MESSAGE = (
    "LLM not configured. Set **OLLAMA_BASE_URL** (remote Ollama via Tailscale Funnel) "
    "or run `ollama serve` locally with `ollama pull llama3.2:3b`. "
    "The **Sources** tab still shows raw search results."
)

_llm: ChatOllama | None = None
_agent = None


def ollama_base_url() -> str | None:
    url = os.environ.get("OLLAMA_BASE_URL", "").strip().rstrip("/")
    return url or None


def _make_chat_ollama(base_url: str) -> ChatOllama:
    kwargs: dict[str, Any] = {
        "model": OLLAMA_MODEL,
        "temperature": 0.1,
        "base_url": base_url,
    }
    api_key = os.environ.get("OLLAMA_API_KEY", "").strip()
    if api_key:
        kwargs["client_kwargs"] = {"headers": {"Authorization": f"Bearer {api_key}"}}
    return ChatOllama(**kwargs)


def get_llm() -> ChatOllama | None:
    """Remote Ollama (OLLAMA_BASE_URL) → local Ollama for dev."""
    global _llm
    if _llm is not None:
        return _llm

    remote = ollama_base_url()
    if remote:
        try:
            _llm = _make_chat_ollama(remote)
            return _llm
        except Exception:
            _llm = None
            return None

    try:
        _llm = _make_chat_ollama("http://127.0.0.1:11434")
        return _llm
    except Exception:
        _llm = None
        return None


def llm_backend_name() -> str:
    remote = ollama_base_url()
    if remote:
        host = urlparse(remote).netloc or remote
        return f"ollama:{OLLAMA_MODEL}@{host}"
    if os.environ.get("SPACE_ID"):
        return "search-only"
    return f"ollama:{OLLAMA_MODEL}@127.0.0.1:11434"


def search_web_raw(query: str, max_results: int = DEFAULT_MAX_RESULTS) -> list[dict[str, str]]:
    """Run DuckDuckGo search and return structured results."""
    if not query.strip():
        return []
    rows: list[dict[str, str]] = []
    with DDGS() as ddgs:
        for item in ddgs.text(query, max_results=max_results):
            rows.append(
                {
                    "title": item.get("title") or "",
                    "url": item.get("href") or item.get("link") or "",
                    "snippet": item.get("body") or item.get("snippet") or "",
                }
            )
    return rows


def format_search_results(results: list[dict[str, str]]) -> str:
    if not results:
        return "No search results found."
    lines = []
    for i, row in enumerate(results, 1):
        title = row.get("title") or "Untitled"
        url = row.get("url") or ""
        snippet = row.get("snippet") or ""
        lines.append(f"{i}. {title}\n   URL: {url}\n   {snippet}")
    return "\n\n".join(lines)


@tool
def search_web(query: str) -> str:
    """Search the web for current information. Returns titles, URLs, and snippets."""
    return format_search_results(search_web_raw(query))


def create_web_agent():
    """Build LangChain create_agent graph with search_web tool."""
    llm = get_llm()
    if llm is None:
        raise RuntimeError(NO_LLM_MESSAGE)
    return create_agent(llm, tools=[search_web], system_prompt=SYSTEM_PROMPT)


def get_web_agent():
    global _agent
    if _agent is None:
        _agent = create_web_agent()
    return _agent


def _message_content(msg: Any) -> str:
    content = getattr(msg, "content", msg)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)
    return str(content)


def _extract_urls(text: str) -> list[str]:
    return re.findall(r"https?://[^\s\])>\"']+", text)


def _results_to_sources(results: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "title": row.get("title") or row.get("url") or "Source",
            "url": row.get("url") or "",
            "snippet": row.get("snippet") or "",
        }
        for row in results
        if row.get("url")
    ]


def _looks_like_tool_json(text: str) -> bool:
    t = text.strip()
    return t.startswith("{") and '"name"' in t and ("parameters" in t or "args" in t)


def _invoke_search_then_answer(question: str, llm: ChatOllama) -> dict[str, Any]:
    """Reliable Perplexity-style path: search first, then synthesize with the LLM."""
    query = question.strip()
    results = search_web_raw(query)
    search_blob = format_search_results(results)
    tool_steps = [{"tool": "search_web", "input": query, "output": search_blob}]
    sources = _results_to_sources(results)

    if not results:
        return {
            "answer": "I couldn't find web results for that query. Try rephrasing or check the **Sources** tab.",
            "sources": [],
            "tool_steps": tool_steps,
            "llm_available": True,
        }

    response = llm.invoke(
        [
            SystemMessage(content=SYNTHESIS_PROMPT),
            HumanMessage(content=f"Question: {query}\n\nSearch results:\n{search_blob}"),
        ]
    )
    answer = _message_content(response).strip()
    if not answer or _looks_like_tool_json(answer):
        answer = (
            f"I found results for **{query}**, but couldn't summarize them cleanly. "
            "See the sources below."
        )

    for url in _extract_urls(answer):
        if not any(s["url"] == url for s in sources):
            sources.append({"title": url, "url": url, "snippet": ""})

    return {
        "answer": answer,
        "sources": sources,
        "tool_steps": tool_steps,
        "llm_available": True,
    }


def _invoke_langchain_agent(question: str) -> dict[str, Any]:
    """Native tool-calling agent — used when the model returns real tool_calls."""
    agent = get_web_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": question.strip()}]})

    tool_steps: list[dict[str, str]] = []
    sources: list[dict[str, str]] = []
    answer = ""

    for msg in result.get("messages", []):
        if isinstance(msg, ToolMessage):
            tool_steps.append(
                {
                    "tool": msg.name or "tool",
                    "input": "",
                    "output": _message_content(msg),
                }
            )
            for url in _extract_urls(_message_content(msg)):
                sources.append({"title": url, "url": url, "snippet": ""})
        elif isinstance(msg, AIMessage):
            text = _message_content(msg)
            if text.strip() and not _looks_like_tool_json(text):
                answer = text
            for tc in getattr(msg, "tool_calls", None) or []:
                if isinstance(tc, dict):
                    name = tc.get("name", "tool")
                    args = tc.get("args", {})
                    query = args.get("query", str(args))
                    tool_steps.append({"tool": name, "input": str(query), "output": ""})

    if not sources and tool_steps:
        for step in tool_steps:
            if "search" in step["tool"].lower() and step["output"]:
                for line in step["output"].split("\n"):
                    if line.strip().startswith("URL:"):
                        url = line.split("URL:", 1)[1].strip()
                        sources.append({"title": url, "url": url, "snippet": ""})

    for url in _extract_urls(answer):
        if not any(s["url"] == url for s in sources):
            sources.append({"title": url, "url": url, "snippet": ""})

    return {
        "answer": answer,
        "sources": sources,
        "tool_steps": tool_steps,
        "llm_available": True,
    }


def invoke_with_trace(question: str) -> dict[str, Any]:
    """Run the web agent and return answer, sources, and tool steps."""
    if not isinstance(question, str):
        question = str(question)
    if not question.strip():
        return {"answer": "Enter a question.", "sources": [], "tool_steps": [], "llm_available": False}

    llm = get_llm()
    if llm is None:
        results = search_web_raw(question)
        return {
            "answer": NO_LLM_MESSAGE,
            "sources": _results_to_sources(results),
            "tool_steps": [{"tool": "search_web", "input": question, "output": format_search_results(results)}],
            "llm_available": False,
        }

    # Remote Ollama often emits malformed tool JSON in content instead of executing tools.
    # Search-then-synthesize is reliable for the public demo.
    return _invoke_search_then_answer(question, llm)


# --- Manual tool-calling helpers (notebook sections 1–2) ---

def get_current_weather(city: str, unit: str = "celsius") -> str:
    """Return current weather for a city. unit is celsius or fahrenheit."""
    return f"It is 23°{'C' if unit == 'celsius' else 'F'} and sunny in {city}."


def to_schema(fn) -> dict[str, Any]:
    """Build a JSON schema dict from a function's signature and docstring."""
    import inspect

    sig = inspect.signature(fn)
    params: dict[str, Any] = {"type": "object", "properties": {}, "required": []}
    for name, param in sig.parameters.items():
        ann = param.annotation
        type_name = "string"
        if ann is int:
            type_name = "integer"
        elif ann is float:
            type_name = "number"
        elif ann is bool:
            type_name = "boolean"
        params["properties"][name] = {"type": type_name, "description": f"Parameter {name}"}
        if param.default is inspect.Parameter.empty:
            params["required"].append(name)
    return {
        "name": fn.__name__,
        "description": (fn.__doc__ or "").strip(),
        "parameters": params,
    }


MANUAL_TOOL_SYSTEM = """You are a helpful assistant with access to tools.

When you need a tool, respond with exactly one line:
TOOL_CALL: {"name": "<tool_name>", "args": {<json args>}}

Available tools:
- get_current_weather(city, unit): Return current weather for a city.
"""


def parse_tool_call(text: str) -> tuple[str, dict] | None:
    match = re.search(r"TOOL_CALL:\s*(\{.*\})", text, re.DOTALL)
    if not match:
        return None
    import json

    payload = json.loads(match.group(1))
    return payload.get("name"), payload.get("args", {})


def dispatch_tool(name: str, args: dict) -> str:
    if name == "get_current_weather":
        return get_current_weather(**args)
    if name == "search_web":
        return search_web.invoke(args)
    return f"Unknown tool: {name}"
