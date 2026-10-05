#!/usr/bin/env bash
# 一键配置并启动 Gemini-FastAPI（macOS / Linux）
# 用法：bash setup.sh
set -euo pipefail
cd "$(dirname "$0")"

green() { printf '\033[32m%s\033[0m\n' "$*"; }
red() { printf '\033[31m%s\033[0m\n' "$*"; }
step() { printf '\n\033[1m== %s ==\033[0m\n' "$*"; }

step "1/5 检查 Docker"
if ! command -v docker >/dev/null 2>&1; then
  red "没找到 docker 命令：请先安装并打开 Docker Desktop（或 OrbStack），再重新运行本脚本。"
  exit 1
fi
if ! docker info >/dev/null 2>&1; then
  red "Docker 没有在运行：请打开 Docker Desktop，等菜单栏小鲸鱼不再转圈后重新运行。"
  exit 1
fi
green "Docker 正常"

step "2/5 填写 Cookie"
if [ -f .env ]; then
  read -r -p "已存在 .env，是否覆盖重新填写？[y/N] " ans
  if [[ ! "$ans" =~ ^[Yy]$ ]]; then
    green "保留现有 .env"
    SKIP_ENV=1
  fi
fi

if [ -z "${SKIP_ENV:-}" ]; then
  echo "粘贴时屏幕上不会显示内容，粘贴后直接回车即可。"
  read -r -s -p "请粘贴 __Secure-1PSID 的值：" PSID; echo
  read -r -s -p "请粘贴 __Secure-1PSIDTS 的值：" PSIDTS; echo
  PSID="$(printf '%s' "$PSID" | tr -d '[:space:]\"')"
  PSIDTS="$(printf '%s' "$PSIDTS" | tr -d '[:space:]\"')"
  if [ ${#PSID} -lt 20 ] || [ ${#PSIDTS} -lt 20 ]; then
    red "Cookie 太短，可能没复制完整，请重新运行脚本。"
    exit 1
  fi
  if [[ "$PSIDTS" != sidts-* ]]; then
    red "提示：__Secure-1PSIDTS 一般以 sidts- 开头，请确认没有复制成别的 Cookie（继续执行）。"
  fi

  step "3/5 检测网络 / 代理"
  PROXY=""
  if curl -s -m 8 -o /dev/null https://gemini.google.com; then
    green "可以直连 Google，不使用代理"
  else
    echo "无法直连 Google，正在检测本机代理端口…"
    for port in 7890 7897 6152 1087 1082 10809 8889 20171; do
      if curl -s -m 8 -o /dev/null -x "http://127.0.0.1:$port" https://gemini.google.com; then
        PROXY="http://host.docker.internal:$port"
        green "检测到可用代理：127.0.0.1:$port"
        break
      fi
    done
    if [ -z "$PROXY" ]; then
      read -r -p "没自动找到代理，请输入代理软件的 HTTP 端口（如 7890）：" port
      PROXY="http://host.docker.internal:$port"
    fi
  fi

  API_KEY="sk-$(openssl rand -hex 20)"
  cat > .env <<ENV
API_KEY=$API_KEY
PORT=8000
ACCOUNT1_SECURE_1PSID=$PSID
ACCOUNT1_SECURE_1PSIDTS=$PSIDTS
ACCOUNT1_PROXY=$PROXY
CHAT_MODE=temporary
LOG_LEVEL=INFO
ENV
  chmod 600 .env
  rm -rf cache
  green "已写入 .env"
fi

set -a; . ./.env; set +a
BASE="http://127.0.0.1:${PORT:-8000}"

step "4/5 启动服务（首次需要下载镜像，约 1-3 分钟）"
docker compose pull
docker compose up -d --force-recreate

printf "等待服务就绪"
for _ in $(seq 1 60); do
  if curl -s -m 3 -o /dev/null -w '%{http_code}' "$BASE/health" -H "Authorization: Bearer $API_KEY" | grep -q '^2'; then
    echo; green "服务已启动"
    READY=1; break
  fi
  printf "."; sleep 3
done
if [ -z "${READY:-}" ]; then
  echo; red "服务 3 分钟内没有就绪，最近日志如下（发给别人前请删掉其中的 Cookie）："
  docker compose logs --tail 40
  exit 1
fi

step "5/5 测试"
MODELS="$(curl -s "$BASE/v1/models" -H "Authorization: Bearer $API_KEY")"
echo "可用模型："
printf '%s' "$MODELS" | grep -o '"id": *"[^"]*"' | sed 's/.*"\([^"]*\)"$/\1/' | sed 's/^/  - /'
MODEL="$(printf '%s' "$MODELS" | grep -o '"id": *"[^"]*pro[^"]*"' | head -1 | sed 's/.*"\([^"]*\)"$/\1/')"
MODEL="${MODEL:-gemini-3.1-pro}"
echo "用 $MODEL 发一条测试消息…"
curl -s "$BASE/v1/chat/completions" \
  -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" \
  -d "{\"model\":\"$MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"用一句话介绍你自己\"}]}" \
  | grep -o '"content": *"[^"]*"' | head -1 | sed 's/^"content": *"//; s/"$//'

cat <<DONE

$(green "全部完成！在聊天软件里添加 OpenAI 兼容服务商：")
  API 地址：$BASE/v1
  API Key ：$API_KEY
  模型    ：$MODEL

以后停止：cd "$(pwd)" && docker compose down
以后启动：cd "$(pwd)" && docker compose up -d
DONE
