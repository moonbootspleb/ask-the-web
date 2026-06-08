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

SYNTHESIS_PROMPT = """You are a research assistant writing a brief from web search snippets.

Your job is to SUMMARIZE specific facts from the snippets — not to tell the user where to look.

Rules:
1) Answer ONLY from the search results. Do not invent facts.
2) Write 3–5 bullet points. Each bullet must state a concrete fact (who, what, when) from a snippet.
3) End each bullet with an inline markdown link to the source: [title](url).
4) NEVER say "you can find news on", "visit their website", "check out", or list sites without summarizing content.
5) If snippets are thin, say what is missing. Do not output JSON or tool calls."""

STRICT_SYNTHESIS_PROMPT = SYNTHESIS_PROMPT + """

IMPORTANT: Your previous attempt only pointed at websites. Rewrite as bullet-point facts extracted from the snippets."""

_NEWS_QUERY_HINTS = (
    "latest",
    "news",
    "recent",
    "today",
    "yesterday",
    "this week",
    "breaking",
    "current",
    "update",
)

_GENERIC_ANSWER_MARKERS = (
    "can be found on",
    "can be found at",
    "official website",
    "various news sources",
    "such as bloomberg",
    "such as space.com",
    "provides updates on",
    "real-time coverage",
    "visit their",
    "check out",
    "you can find",
)

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


def _wants_news_search(query: str) -> bool:
    q = query.lower()
    return any(hint in q for hint in _NEWS_QUERY_HINTS)


def _news_topic(query: str) -> str:
    """Strip news-style question prefixes so DDGS news search gets a clean topic."""
    q = query.strip().rstrip("?")
    lowered = q.lower()
    prefixes = (
        "what is the latest news about ",
        "what are the latest news about ",
        "what's the latest news about ",
        "latest news about ",
        "recent news about ",
        "what is the latest on ",
        "what's the latest on ",
        "latest on ",
    )
    for prefix in prefixes:
        if lowered.startswith(prefix):
            return q[len(prefix) :].strip()
    return q


def _normalize_search_row(item: dict[str, Any]) -> dict[str, str]:
    return {
        "title": item.get("title") or "",
        "url": item.get("href") or item.get("link") or item.get("url") or "",
        "snippet": item.get("body") or item.get("snippet") or item.get("excerpt") or "",
    }


def _search_news(topic: str, max_results: int) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with DDGS() as ddgs:
        for item in ddgs.news(topic, max_results=max_results):
            row = _normalize_search_row(item)
            if row["url"] or row["snippet"]:
                rows.append(row)
    return rows


def _search_text(query: str, max_results: int) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with DDGS() as ddgs:
        for item in ddgs.text(query, max_results=max_results):
            row = _normalize_search_row(item)
            if row["url"] or row["snippet"]:
                rows.append(row)
    return rows


def search_web_raw(query: str, max_results: int = DEFAULT_MAX_RESULTS) -> list[dict[str, str]]:
    """Run DuckDuckGo search and return structured results."""
    if not query.strip():
        return []

    if _wants_news_search(query):
        topic = _news_topic(query)
        news_rows = _search_news(topic, max_results=max_results)
        if news_rows:
            return news_rows

    return _search_text(query, max_results=max_results)


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


def _is_generic_answer(text: str) -> bool:
    t = text.lower().strip()
    if not t:
        return True
    if _looks_like_tool_json(text):
        return True
    marker_hits = sum(1 for marker in _GENERIC_ANSWER_MARKERS if marker in t)
    has_bullets = "\n-" in t or "\n*" in t or t.startswith(("-", "*"))
    # Short answers that only point at outlets, with no bullet facts.
    if marker_hits >= 2 and not has_bullets:
        return True
    if marker_hits >= 1 and len(t) < 280 and not has_bullets:
        return True
    return False


def _fallback_summary(question: str, results: list[dict[str, str]]) -> str:
    """Deterministic summary from snippets when the LLM only lists sources."""
    lines = [f"Here is a summary of recent results for **{question.strip().rstrip('?')}**:\n"]
    for row in results[:DEFAULT_MAX_RESULTS]:
        title = row.get("title") or "Source"
        url = row.get("url") or ""
        snippet = (row.get("snippet") or "").strip()
        if not snippet:
            continue
        if not snippet.endswith("."):
            snippet += "."
        link = f"[{title}]({url})" if url else title
        lines.append(f"- {snippet} — {link}")
    if len(lines) == 1:
        return (
            f"I found sources for **{question.strip().rstrip('?')}**, "
            "but the snippets were too short to summarize. See the **Sources** tab."
        )
    return "\n".join(lines)


def _synthesize_answer(question: str, search_blob: str, llm: ChatOllama, *, strict: bool = False) -> str:
    system = STRICT_SYNTHESIS_PROMPT if strict else SYNTHESIS_PROMPT
    response = llm.invoke(
        [
            SystemMessage(content=system),
            HumanMessage(content=f"Question: {question}\n\nSearch results:\n{search_blob}"),
        ]
    )
    return _message_content(response).strip()


def _synthesis_trace_input(question: str, result_count: int) -> str:
    return (
        f"Question: {question}\n"
        f"Synthesize an answer from {result_count} search result(s) (see search_web step)."
    )


def _invoke_search_then_answer(question: str, llm: ChatOllama) -> dict[str, Any]:
    """Reliable Perplexity-style path: search first, then synthesize with the LLM."""
    query = question.strip()
    results = search_web_raw(query)
    search_blob = format_search_results(results)
    tool_steps: list[dict[str, str]] = [
        {"tool": "search_web", "input": query, "output": search_blob},
    ]
    sources = _results_to_sources(results)

    if not results:
        return {
            "answer": "I couldn't find web results for that query. Try rephrasing or check the **Sources** tab.",
            "sources": [],
            "tool_steps": tool_steps,
            "llm_available": True,
        }

    answer = _synthesize_answer(query, search_blob, llm)
    tool_steps.append(
        {
            "tool": "synthesize_answer",
            "input": _synthesis_trace_input(query, len(results)),
            "output": answer,
        }
    )

    if _is_generic_answer(answer):
        retry = _synthesize_answer(query, search_blob, llm, strict=True)
        tool_steps.append(
            {
                "tool": "synthesize_answer",
                "input": f"Strict retry — {_synthesis_trace_input(query, len(results))}",
                "output": retry or "(no response)",
            }
        )
        if retry and not _is_generic_answer(retry):
            answer = retry
        else:
            answer = _fallback_summary(query, results)
            tool_steps.append(
                {"tool": "snippet_fallback", "input": query, "output": answer},
            )

    if not answer or _looks_like_tool_json(answer):
        answer = _fallback_summary(query, results)
        if tool_steps[-1].get("tool") != "snippet_fallback":
            tool_steps.append(
                {"tool": "snippet_fallback", "input": query, "output": answer},
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
