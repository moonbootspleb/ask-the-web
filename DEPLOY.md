# Deploy Ask-the-Web to Hugging Face Spaces + moonboots.tech

Production demo: **Gradio on HF CPU basic** embedded on the React blog. LLM runs on your Linux box via **Tailscale Funnel** (`llama3.2:3b`).

| Piece | Where |
|-------|--------|
| Space source | [`BYTEBTYEGO/demos-3/`](.) |
| Blog embed | `COMPANYSITE` → `/blog/building-an-ask-the-web-agent` |
| Netlify env | `VITE_ASK_THE_WEB_SPACE_URL` |

---

## 1. Prepare Ollama on your Linux box

```bash
ollama serve
ollama pull llama3.2:3b
```

`llama3.2:3b` is required for **native tool calling**. Smaller models (e.g. `gemma3:1b`) work in the lab notebook with manual parsing only.

---

## 2. Expose Ollama via Tailscale Funnel

```bash
cd BYTEBTYEGO/demos-3
chmod +x scripts/setup_tailscale_funnel.sh scripts/verify_ollama_remote.sh
./scripts/setup_tailscale_funnel.sh
```

Default model in the script is `llama3.2:3b`. Copy the HTTPS Funnel URL from the output.

Verify from outside your LAN:

```bash
./scripts/verify_ollama_remote.sh https://your-host.tail12345.ts.net
```

---

## 3. Create the Hugging Face Space

1. [huggingface.co/new-space](https://huggingface.co/new-space)
2. **Space name:** `ask-the-web`
3. **SDK:** Gradio
4. **Hardware:** CPU basic (free tier)
5. **Visibility:** Public

---

## 4. Push files to the Space repo

| File / folder | Notes |
|---------------|--------|
| `app.py` | Gradio entry |
| `theme.py` | MoonBoots styling |
| `agent_core.py` | Agent + search logic |
| `requirements.txt` | Space dependencies |
| `README.md` | HF YAML frontmatter |

```bash
git clone https://huggingface.co/spaces/moonbootspleb/ask-the-web
cd ask-the-web

SRC=~/MOONBOOTS/BYTEBTYEGO/demos-3
cp "$SRC/app.py" "$SRC/theme.py" "$SRC/agent_core.py" "$SRC/requirements.txt" "$SRC/README.md" .

git add app.py theme.py agent_core.py requirements.txt README.md
git commit -m "Ask-the-Web: Gradio + DuckDuckGo + remote Ollama"
git push
```

---

## 5. Space secrets

| Secret | Example | Required |
|--------|---------|----------|
| `OLLAMA_BASE_URL` | `https://your-host.tail12345.ts.net` | Yes (for full Ask tab) |
| `OLLAMA_MODEL` | `llama3.2:3b` | No (default in code) |

Do **not** set `OLLAMA_API_KEY` unless you add bearer auth in front of Ollama.

After saving secrets, wait for **Building** → **Running**.

---

## 6. Test the Space

| Check | URL / action |
|-------|----------------|
| Space page | `https://huggingface.co/spaces/moonbootspleb/ask-the-web` |
| Embed host | `https://moonbootspleb-ask-the-web.hf.space` |
| Sources tab | Query works without LLM |
| Ask tab | Returns cited answer with `OLLAMA_BASE_URL` set |
| Steps tab | Shows `search_web` tool trace after Ask |

---

## 7. Embed on Netlify (moonboots.tech)

```bash
VITE_ASK_THE_WEB_SPACE_URL=https://huggingface.co/spaces/moonbootspleb/ask-the-web
```

Clear cache and redeploy. Open `https://moonboots.tech/blog/building-an-ask-the-web-agent`.

---

## 8. Smoke test checklist

- [ ] HF Space status **Running**
- [ ] `verify_ollama_remote.sh` passes for Funnel URL
- [ ] Ask tab: multi-step question returns answer + sources
- [ ] Sources tab: raw DDG results
- [ ] Steps tab: tool trace after Ask
- [ ] Blog embed loads via lazy iframe

---

## Operational notes

- Funnel exposes Ollama to the public internet — restrict identity in Tailscale admin if needed.
- Your Linux box and Funnel must stay up for live Ask answers.
- Expect several seconds latency (HF cloud → your home → back).
- **Sources** tab works even when Ollama is down.
