#!/usr/bin/env bash
# Smoke-test a remote Ollama endpoint (Tailscale Funnel URL) from any machine.

set -euo pipefail

BASE="${1:-}"
if [[ -z "${BASE}" ]]; then
  echo "Usage: $0 https://your-host.tail12345.ts.net"
  exit 1
fi

BASE="${BASE%/}"
API_KEY="${OLLAMA_API_KEY:-}"
MODEL="${OLLAMA_MODEL:-llama3.2:3b}"

CURL_ARGS=(-sf)
if [[ -n "${API_KEY}" ]]; then
  CURL_ARGS+=(-H "Authorization: Bearer ${API_KEY}")
fi

echo "==> GET ${BASE}/api/tags"
curl "${CURL_ARGS[@]}" "${BASE}/api/tags" | head -c 400
echo ""

echo "==> Checking model ${MODEL} is listed"
if ! curl "${CURL_ARGS[@]}" "${BASE}/api/tags" | grep -q "${MODEL}"; then
  echo "WARN: ${MODEL} not found in tags — run: ollama pull ${MODEL}"
fi

echo "OK — Ollama reachable at ${BASE}"
