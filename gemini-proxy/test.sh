#!/usr/bin/env bash
# 用法：./test.sh            （读取 .env 中的 API_KEY 和 PORT）
set -euo pipefail
cd "$(dirname "$0")"
set -a; [ -f .env ] && . ./.env; set +a
BASE="http://127.0.0.1:${PORT:-8000}"
AUTH="Authorization: Bearer ${API_KEY:-}"

echo "== 健康检查 =="
curl -sS "$BASE/health" -H "$AUTH"; echo

echo "== 可用模型 =="
curl -sS "$BASE/v1/models" -H "$AUTH"; echo

MODEL="${1:-gemini-3.1-pro}"
echo "== 对话测试（模型：$MODEL）=="
curl -sS "$BASE/v1/chat/completions" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d "{\"model\":\"$MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"用一句话介绍你自己，并说出你是哪个模型\"}]}"
echo
