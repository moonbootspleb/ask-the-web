#!/usr/bin/env bash
# Copy demos-3 files into a cloned HF Space repo and push.
# Prerequisite: git clone https://huggingface.co/spaces/moonbootspleb/ask-the-web

set -euo pipefail

SPACE_DIR="${1:-}"
if [[ -z "${SPACE_DIR}" || ! -d "${SPACE_DIR}/.git" ]]; then
  echo "Usage: $0 /path/to/ask-the-web-space-clone"
  echo "Clone first: git clone https://huggingface.co/spaces/moonbootspleb/ask-the-web"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC="$(cd "${SCRIPT_DIR}/.." && pwd)"

cp "${SRC}/app.py" "${SRC}/theme.py" "${SRC}/agent_core.py" "${SRC}/requirements.txt" "${SRC}/README.md" "${SPACE_DIR}/"

cd "${SPACE_DIR}"
git add app.py theme.py agent_core.py requirements.txt README.md
git status
echo ""
echo "Review changes, then: git commit -m 'Ask-the-Web: Gradio + DuckDuckGo + remote Ollama' && git push"
