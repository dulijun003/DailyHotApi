# Gemini 网页版 → OpenAI 兼容 API（本地 Docker）

基于 [Nativu5/Gemini-FastAPI](https://github.com/Nativu5/Gemini-FastAPI)，用 Gemini Pro 订阅账号的网页 Cookie 提供 OpenAI 格式接口。当前配置为**单账号、仅本机访问**。

> ⚠️ 这是对 Gemini 网页版的逆向调用，不是官方 API，违反 Google 服务条款，存在封号风险。建议用不重要的账号，请求频率保持在正常人工使用水平。

## 1. 准备

- 安装 [Docker Desktop](https://www.docker.com/products/docker-desktop/)（Windows / macOS）或 Docker Engine（Linux）
- 本机能访问 `gemini.google.com`（需要代理的话见第 3 步的 `ACCOUNT1_PROXY`）

## 2. 获取 Cookie

1. 打开浏览器**无痕窗口**，登录你的 Pro 账号，进入 <https://gemini.google.com> 并随便发一句话
2. 按 `F12` → **Application**（应用）→ 左侧 **Cookies** → `https://gemini.google.com`
3. 复制这两项的 Value：
   - `__Secure-1PSID`
   - `__Secure-1PSIDTS`
4. **直接关闭无痕窗口，不要点退出登录**（退出会让 Cookie 立刻失效）

## 3. 配置

```bash
cd gemini-proxy
cp .env.example .env
```

编辑 `.env`：

| 变量 | 说明 |
|---|---|
| `API_KEY` | 调用本服务的密钥，自己设定（`openssl rand -hex 24` 生成） |
| `ACCOUNT1_SECURE_1PSID` / `ACCOUNT1_SECURE_1PSIDTS` | 第 2 步复制的 Cookie |
| `ACCOUNT1_PROXY` | 本机需要代理才能访问 Google 时填写，例如 `http://host.docker.internal:7890`（容器里不能写 `127.0.0.1`） |
| `CHAT_MODE` | 默认 `temporary`，不会写进网页版聊天记录 |

## 4. 启动

```bash
docker compose up -d
docker compose logs -f     # 看到客户端初始化成功即可，Ctrl+C 退出日志
./test.sh                  # 健康检查 + 模型列表 + 一次对话
```

Windows 没有 bash 时，可以直接在浏览器打开 <http://127.0.0.1:8000/health> 检查。

## 5. 在客户端中使用

在 Cherry Studio、LobeChat、ChatBox、Open WebUI 等工具里添加一个 **OpenAI 兼容**的服务商：

- API 地址：`http://127.0.0.1:8000/v1`
- API Key：`.env` 里的 `API_KEY`
- 模型：从 `/v1/models` 返回的列表里选，例如 `gemini-3.1-pro`

Python 示例：

```python
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="你的API_KEY")
resp = client.chat.completions.create(
    model="gemini-3.1-pro",
    messages=[{"role": "user", "content": "你好"}],
)
print(resp.choices[0].message.content)
```

## 常用操作

```bash
docker compose pull && docker compose up -d   # 更新到最新版本（网页改版失效时先试这个）
docker compose restart                        # 重启
docker compose down                           # 停止
```

## 常见问题

- **401 / UNAUTHENTICATED / 初始化失败**：Cookie 失效，重新按第 2 步获取并替换 `.env`，然后删除 `cache/` 目录再 `docker compose up -d`
- **回答像 Flash 而不是 Pro**：Cookie 不是 Pro 账号的，或已失效被降级
- **连接超时**：本机访问不了 Google，填写 `ACCOUNT1_PROXY`

## 以后加账号

在 `docker-compose.yml` 的 `environment` 里按序号追加，并在 `.env` 加对应变量：

```yaml
      CONFIG_GEMINI__CLIENTS__1__ID: account-2
      CONFIG_GEMINI__CLIENTS__1__SECURE_1PSID: ${ACCOUNT2_SECURE_1PSID}
      CONFIG_GEMINI__CLIENTS__1__SECURE_1PSIDTS: ${ACCOUNT2_SECURE_1PSIDTS}
      CONFIG_GEMINI__CLIENTS__1__PROXY: ${ACCOUNT2_PROXY:-}
```

多账号时建议每个账号配一个不同的出口代理，避免被关联。

## 安全提醒

- `.env` 里的 Cookie 等同于你的 Google 账号登录凭证，**不要提交到 Git、不要发给任何人**（本目录 `.gitignore` 已忽略 `.env`、`data/`、`cache/`）
- 端口默认只绑定 `127.0.0.1`。如要开放给局域网，把 `docker-compose.yml` 里的端口改成 `"8000:8000"`，并确保 `API_KEY` 足够复杂
