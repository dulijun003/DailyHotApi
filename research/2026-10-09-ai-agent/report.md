# AI Agent 的间接提示词注入：攻击如何发生，架构层面哪些防御真正有效

> **学习报告**｜研究日期：2026-10-09｜读者：初级实操者（应用实践）｜风格：技术拆解
> 信源：108 条（`sources.md`），A 级为主｜核查结果：36 条关键论断，✅ 26 条、⚠️ 10 条（已全部修正）、❌ 0 条（`factcheck.md`）
> 引用格式：［G编号］对应 `sources.md`。凡标"厂商自报"的数字，都只在该厂商自己的测试条件下成立，不能横向比较。

---

## 一句话结论

间接提示词注入是"模型无法区分指令和数据"导致的**结构性问题**，在模型层无法根除。真正可靠的防御，不是更好地识别恶意文本，而是在模型之外用确定性机制保证：**即使模型被劫持，它也拿不到不该拿的数据、做不了不该做的动作、传不出去。**

## 核心结论

1. **根因在结构，不在模型不够聪明。** SQL 注入可以用参数化查询根治，LLM 却没有对应的手段：开发者指令和外部内容拼进同一个 token 序列后，模型内部 "there is only ever 'next token'"。英国 NCSC 判断，提示词注入"可能永远无法像 SQL 注入那样被彻底缓解"［G2］。OpenAI、Meta、Google、Microsoft、Anthropic 也都公开承认无法完全阻止［G5］［G7］［G12］［G13］［G17］。
2. **危害需要三个条件同时成立。** 三个条件是：不可信输入、敏感数据或能力、对外通信或改变状态的通道。Willison 把它称为 lethal trifecta［G6］，Meta 进一步规定一个会话最多同时满足其中两项，即 Agents Rule of Two［G7］。拆掉其中一项，就能在架构上切断对应的攻击链。
3. **"概率性"防御在自适应攻击面前普遍失效。** 2025-10 的 "The Attacker Moves Second" 测了 12 种防御，它们原论文报告的攻击成功率大多接近 0，在自适应攻击下大多超过 90%；人类红队对所有被测场景都攻破了［G18］。分类器、提示技巧、对抗训练只能降低常见攻击的命中率，**不能作为安全边界**。
4. **真实案例都能用三要素解释。** 公开记录中，修复后又被绕过的都是检测类措施（Comet、Gemini 日历）。架构层修复（收权限、封出口、加确认门）目前没有看到被绕过的公开记录，不过 GitHub 的 Lockdown 模式出过实现漏洞［G33］［G60］［G56］。
5. **确定性控制有效，但每一种只能切断一环。** 已知的绕过点都在各环之间的接缝处：白名单内的域名被滥用［G53］［G80］、多 Agent 组合后保证失效［G75］、伪造可信数据［G77］。
6. **人工确认是兜底，不是主防线。** Claude Code 用户批准了 93% 的权限提示［G94］，确认框本身也可能被注入伪造［G81］。业界的方向是用沙箱减少确认次数（Anthropic 内部数据：减少 84%）［G79］，只对少数高风险操作保留确认。
7. **评估方法是最大的不确定性。** 只看静态基准会高估防御效果；攻击重复多次后成功率显著上升［G91］；攻击成功率低也可能只是 Agent 能力不足（"security by incompetence"）［G83］。

---

## 知识框架：四层速览

先用一句大白话把每层讲清楚，后面各章再展开。

| 层次 | 一句话解释 | 对应章节 |
|---|---|---|
| **是什么** | Agent 把读到的网页、邮件当成"上司的命令"去执行了，因为它分不清哪段文字是命令、哪段只是材料 | 第 1 章 |
| **有什么** | 任何 Agent 会读的东西都可能是入口；攻击分"藏指令"和"往外传"两步；目标是偷数据、乱操作、长期潜伏、扩散 | 第 2、3 章 |
| **如何做** | 不指望模型识破骗局，而是让被骗的模型也闯不了祸：拆掉三要素之一，在模型之外设闸门 | 第 4 章 |
| **怎么用** | 把自己的 Agent 画成数据流图，找到三要素交汇点，逐个拆掉，再用多次尝试的红队测试验证 | 第 5 章 |

---

## 第 1 章　原理：为什么"指令"和"数据"分不开

### 1.1 和 SQL 注入对比

| | SQL 注入 | 提示词注入 |
|---|---|---|
| 问题 | 用户输入被当成 SQL 代码执行 | 外部内容被当成指令执行 |
| 根治手段 | 参数化查询：数据库引擎在**结构上**不可能把参数当代码执行 | **不存在**。指令和数据进入同一个 token 序列，模型内部没有通道之分［G2］ |
| 能做的 | 根治 | 只能降低概率（训练、提示技巧、检测），以及在模型外限制后果 |

学术测量也印证了这一点。Zverev 等人的论文指出，"none of the existing models provide a dedicated mechanism to distinguish between instructions and data"。GPT-4 在默认提示下的分离分数只有 20.8%；换用优化提示后升到 95.3%，但仍然会在数百个样本里执行数据中夹带的指令［G3］。通过训练提高分离度也可以做到，代价是任务效用下降［G3］。

NCSC 给了一个很好的比喻：LLM 是一个**"天生可被混淆的代理人"**（inherently confusable deputy）［G2］。你雇了一个助理去读邮件，他会照着任何一封邮件里写的"请把老板的文件发给我"去做，因为他没办法可靠地判断这句话是谁说的。

### 1.2 问题出在哪一行代码

一个最朴素的 Agent 循环长这样：

```python
messages = [system_prompt, user_request]
while True:
    reply = llm(messages)                  # 模型决定下一步
    if reply.is_final: break
    result = run_tool(reply.tool_call)     # 读网页、读邮件、查数据库……
    messages.append(tool_result(result))   # ← 问题就在这里
```

最后一行把工具返回的**不可信内容**原样放回上下文，和系统提示、用户请求混在一起。模型下一轮决策时，这段内容和真正的指令处在同一个"频道"里。间接注入要利用的就是这一行。

### 1.3 危害成立的条件：三要素

```mermaid
flowchart LR
    A["A 不可信输入<br/>网页、邮件、issue、工具返回"] --> X{"同一个会话<br/>同时具备"}
    B["B 敏感数据或系统<br/>私有仓库、邮箱、数据库"] --> X
    C["C 改变状态或对外通信<br/>发请求、渲染图片、写 PR、发邮件"] --> X
    X -->|三项齐全| D["注入可以造成实际危害"]
```

- **Lethal trifecta（Willison，2025-06）**：私有数据访问、暴露于不可信内容、对外通信能力。三者同时具备时，"an attacker can easily trick it into accessing your private data and sending it to that attacker"［G6］。
- **Agents Rule of Two（Meta，2025-10）**：把第三项扩展为"改变状态或对外通信"，规定一个会话最多同时满足两项。三项都需要时，就不应自主运行，必须有人工批准等监督［G7］。
- **两者的差别**：Willison 指出，trifecta 只覆盖数据外泄。即使没有敏感数据，"不可信输入 + 能改变状态"仍然危险，比如删文件、误发消息［G8］。所以"去掉任意一项即安全"只对窃取数据这类危害成立。

### 1.4 模型层能做到什么程度

下表都是在各自测试条件下的**厂商或作者自报**数字：

| 手段 | 报告的效果 | 条件与局限 |
|---|---|---|
| Spotlighting（定界、数据标记、编码） | 攻击成功率从 >50% 降到 <2%［G10］ | GPT 系列，非 Agent 任务，静态攻击 |
| 指令层级训练（IH-Challenge） | GPT-5-Mini 的 IH 鲁棒性平均 +10.0%（84.1% → 94.1%），不安全行为从 6.6% 降到 0.7%［G11］ | 作者承认"robust IH behavior is difficult to train"，模型可能学会过度拒绝 |
| Gemini 对抗训练 | 邮件场景中，Beam Search 攻击从 74.8% 降到 4.2%；但日历场景的 TAP 攻击仍有 94.6%［G12］ | 作者原话："clearly not sufficient as a defense in isolation" |
| Claude 浏览器扩展（Opus 4.5 + 新防护） | 内部 Best-of-N 自适应攻击（每环境 100 次）下约 1%［G13］ | 包含分类器和产品层防护；"No browser agent is immune" |
| Claude Opus 5 / 5.5（System Card） | 无系统防护时，Opus 5 为 3.64%，Opus 5.5 为 0.09%；开启 auto mode（注入探针 + 危险操作分类器）时两者均为 0%［G107］［G108］ | 厂商自报，110–129 个场景；0% 是"模型 + 系统防护"的组合结果 |

**为什么降不到零？** 有三个原因：

- 训练只是改变概率分布，没有建立结构性的边界［G2］；
- 攻击空间无法穷举，所以"it is not possible to claim that the model is truly robust"［G12］；
- 能力更强、更听指令的模型，有时反而更容易被攻击（"More capable models aren't necessarily more secure"）［G12］。

### 1.5 自适应攻击：静态数字为什么不可信

"The Attacker Moves Second"（作者来自 OpenAI、Anthropic、Google DeepMind、ETH 等机构，USENIX Security 2026）用梯度、强化学习、随机搜索和人类红队攻击了 12 种防御［G18］：

- Spotlighting 和 Prompt Sandwiching：静态攻击下最低约 1%，自适应攻击下 **>95%**
- MetaSecAlign：原论文报告 2%，复测 **96%**
- Protect AI、PromptGuard、Model Armor 三种检测器：**>90%**；PIGuard：71%
- 人类红队（500 多人参与）：所有被测场景都攻破

另一篇 NAACL 2025 的论文测试了 8 种防御，全部被自适应攻击绕过，攻击成功率持续超过 50%［G19］。

检测器失效的原因很直接：很多成功的触发文本**本身看起来并不恶意**，脱离上下文时根本无法判定为危险［G18］。EchoLeak 正是利用了这一点（见第 3 章）。

> **本章要点**：防御设计的出发点应该是"假设注入一定会成功"，然后问：成功之后，它能造成什么后果？

---

## 第 2 章　攻击面：入口、手法与目标

### 2.1 入口：Agent 读的一切都是入口

| 入口 | 有出处的实例 |
|---|---|
| 网页、搜索结果 | 藏在 Reddit 评论里的指令劫持了 Comet［G33］；Unit 42 报告了首个旨在绕过 AI 广告审核的恶意 IDPI 野外案例［G34］ |
| 邮件 | EchoLeak：一封邮件实现零点击外泄［G51］ |
| 日历邀请 | 一个日历邀请即可劫持 Gemini，进而控制智能家居［G59］ |
| 文档（含隐藏文字） | 恶意 Google Doc 让 ChatGPT 外泄数据（OWASP ASI01 场景）［G24］ |
| 代码仓库、issue、PR | 恶意 issue 劫持 GitHub MCP［G26］；PR 描述里的隐藏注释（CamoLeak）［G40］ |
| 业务表单、工单字段 | Salesforce Web-to-Lead 表单（ForcedLeak）［G41］；Supabase 客服工单［G64］ |
| MCP 工具描述 | 工具投毒：描述里藏着用户看不到、模型看得到的指令［G25］ |
| RAG 知识库 | PoisonedRAG：在含数百万文本的知识库中，针对每个目标问题注入 5 条恶意文本，攻击成功率可达 90%［G30］ |
| 长期记忆 | 通过注入写入跨会话持久化的"间谍指令"［G37］ |
| 其他 Agent 的输出 | 低权限 Agent 被注入后，调用高权限的同队 Agent（ServiceNow 二阶注入）［G43］ |
| 图片 | 图片缩放后才显现的文字（Trail of Bits）［G44］；截图中几乎不可见的文字［G45］ |

OWASP Agentic Top 10（2025-12）对此的解释是："agents and the underlying model cannot reliably distinguish instructions from related content"［G24］。**靠逐个封堵入口来防御是行不通的。**

### 2.2 手法：先"藏"，再"传"

```mermaid
flowchart LR
    subgraph 藏["第一步：藏起来（人看不到，模型读得到）"]
        H1["CSS 隐藏 / 零字号"]
        H2["HTML 注释"]
        H3["Unicode tag 字符 / 零宽字符"]
        H4["图片缩放 / 近乎透明的文字"]
    end
    subgraph 传["第二步：传出去（借合法功能外泄）"]
        E1["Markdown 图片自动加载"]
        E2["白名单域名上的代理或跳转"]
        E3["写操作：PR、工单、日历事件"]
        E4["Agent 自己的网络请求"]
    end
    藏 --> M["模型被劫持"] --> 传
```

- **藏**：Unit 42 在野外观察到 22 种构造载荷的技巧，包括 `font-size: 0`、`display: none` 等［G34］；Unicode tag 字符（U+E0000–U+E007F）在界面上不显示，模型却能读到［G28］。
- **传**：Markdown 图片在渲染时会自动请求 URL，数据就藏在 URL 参数里［G5］。所以 GitHub 干脆完全禁用了 Copilot Chat 的图片渲染［G40］。
- **持久化和供应链**：MCP 工具定义可以在用户批准之后再被篡改（rug pull）［G25］；被写进记忆的指令能跨会话生效［G37］。

### 2.3 攻击目标

| 目标 | 例子 | 框架中的对应项 |
|---|---|---|
| 数据外泄 | EchoLeak、GitHub MCP | OWASP LLM01 / ASI01；ATLAS AML.T0086 |
| 越权执行动作 | Copilot 改配置后执行命令 | LLM01 "unauthorized access to functions"；ASI02 |
| 篡改输出 | 误导性摘要 | LLM01 "Content manipulation" |
| 持久化 | 记忆投毒、工具投毒 | ASI06；ATLAS Persistence 战术 |
| 扩散传播 | AI 蠕虫 Morris II | ASI07/08；ATLAS AML.T0061 |

同一种攻击在不同框架里的归类并不一致。例如工具投毒，在 OWASP 里分属 ASI02 或 ASI04，在 ATLAS 里归入 Persistence［G24］［G23］。学的时候理解攻击机制即可，不必纠结归类。

### 2.4 不同类型 Agent 的主要暴露面

| Agent 类型 | 主要入口 | 典型危险组合 |
|---|---|---|
| 浏览器 / 电脑操作 Agent | 任意网页、评论区、截图、广告 | 不可信网页 + 用户在所有站点的登录态 + 能发帖、能填表（Comet 案例） |
| 编程 Agent | 代码文件、依赖的 README、issue/PR、规则文件、MCP 工具、图片 | 不可信仓库内容 + 本机文件和密钥 + 终端和网络（Copilot、Gemini CLI 经 Zapier MCP 外泄［G44］） |
| 办公助手（邮件、日历、文档） | 外部来信、日历邀请、共享文档、记忆 | 攻击者可以**主动投递**，用户无需任何操作（零点击，EchoLeak） |
| 客服 / 企业流程 Agent | 外部用户可写的表单、工单、记录字段；同队的其他 Agent | 外部文本以**内部员工的权限**被处理（ForcedLeak［G41］、ServiceNow 二阶注入［G43］） |

ServiceNow 的案例尤其值得注意：攻击发生时，平台的提示词注入防护功能处于开启状态（"all while the ServiceNow prompt injection protection feature was enabled"）［G43］。

Willison 的观点是，判断风险的关键不在 Agent 属于哪种类型，而在于它**是否同时具备三要素**［G6］。上表可以帮你快速定位每类 Agent 的三要素分别落在哪里。

### 2.5 野外现状

野外攻击已经出现，但目前还不复杂：

- Google 扫描 CommonCrawl 后发现，恶意类注入在 2025-11 到 2026-02 间相对增长了 32%，同时评价为"limited sophistication"［G35］；
- Unit 42 在 2026-03 报告了针对 AI 广告审核系统的真实攻击［G34］。

---

## 第 3 章　真实案例拆解

以下 6 个案例都有一手资料（研究者原文、厂商公告或 CVE）。

### 案例 A：EchoLeak（CVE-2025-32711，M365 Copilot，CVSS 9.3）

```mermaid
sequenceDiagram
    participant 攻击者
    participant 邮箱
    participant Copilot
    participant 浏览器
    攻击者->>邮箱: 发一封"写给人看"的邮件（躲过 XPIA 分类器）
    Note over Copilot: 受害者问了个无关的问题
    Copilot->>邮箱: 检索把这封邮件拉进上下文（零点击）
    Copilot->>浏览器: 输出引用式 Markdown 图片，URL 参数里带着内部数据
    浏览器->>攻击者: 自动加载图片，经 CSP 白名单中的 Teams 域名转发
```

- **根因**：外部邮件和内部机密进入同一个上下文；检测只靠一个分类器；图片会自动渲染；CSP 白名单过宽［G36］［G53］。
- **修复**：微软于 2025-05 在服务端修复，去除外部内容里的引用式链接和图片，2025-06-11 公开［G51］［G36］。
- **修复后的绕过**：未找到公开记录。

### 案例 B：GitHub MCP 恶意 issue（Invariant Labs，2025-05）

- **链条**：攻击者在公共仓库提交恶意 issue → 用户让 Agent "看看 open issues" → Agent 用同一个 token 读取私有仓库 → 把数据写进公共 PR［G26］。
- **根因**：一个 token 同时能访问公共和私有仓库，三要素集中在同一个 MCP 里。研究者的原话是："this is not a flaw in the GitHub MCP server code itself"［G26］。
- **修复**：2025-12 推出 Lockdown mode，只展示有 push 权限的协作者写的内容［G55］，属于架构层修复。但这个模式本身出过实现漏洞 CVE-2026-48529（跨用户客户端混淆），在 1.1.2 版本修复［G56］。**隔离机制也需要正确实现。**

### 案例 C：Perplexity Comet（Brave，2025-08）

- **链条**：Reddit 评论的剧透标签里藏着指令 → 用户点"总结此页" → Agent 读取账户邮箱，再打开 Gmail 读取 OTP → 回帖外传，攻击者据此接管账户［G33］。
- **根因**：Agent 带着用户在所有站点的登录态；只读的"总结"意图被升级成了跨站的多步操作。
- **修复与绕过**：初次修复第二天就被复测绕过；10 月又出现截图注入这一新载体［G33］［G45］。

### 案例 D：Gemini 日历邀请（SafeBreach 2025-08；Miggo 2026-01）

- **D1**：日历标题里的指令让 Gemini 删除事件、外传邮件，还通过 Google Home 开窗、开锅炉［G59］。Google 随后部署了分类器、Markdown 清洗、用户确认等多层防御［G61］。
- **D2**：Google 已部署独立的恶意提示检测模型的情况下，Miggo 仍用自然语言指令，让 Gemini 把私密会议的摘要写进一个新建事件。在很多企业的日历配置下，这个事件对攻击者可见。Google 已确认并修复［G60］。
- **启示**："新建日历事件"这样的普通写操作，本身就可以成为外传通道。

### 案例 E：Copilot 改写自身配置（CVE-2025-53773）

- **链条**：代码文件里的注入 → Agent 向 `.vscode/settings.json` 写入 `"chat.tools.autoApprove": true` → 之后所有工具调用不再需要确认 → 执行终端命令［G39］［G52］。
- **根因**：Agent 不经审批就能写入控制自身权限的配置文件，**确认机制被 Agent 自己关掉了**。
- **修复**：2025 年 8 月的 Patch Tuesday［G39］。

### 案例 F：Supabase MCP（General Analysis，2025-07）

- **链条**：客服工单中的指令 → 开发者在 Cursor 里让 Agent 查看工单 → Agent 以 `service_role` 身份（绕过行级安全）读取 `integration_tokens` 表 → 把结果写回工单［G64］。
- **修复**：默认只读，并限定单个项目范围。研究者的评价是："A prompt injection filter can flag suspicious content, but it cannot grant or restrict database permissions."［G64］

### 其他值得知道的案例（一句话版）

- **CamoLeak（Legit Security，2025-10）**：指令藏在 PR 描述的隐藏注释里。攻击者预先生成一组 GitHub Camo 代理图片 URL，靠图片的请求顺序逐字符外泄私有代码，绕过了 CSP。GitHub 的修复是**完全禁用 Copilot Chat 的图片渲染**［G40］，是"封出口"的典型做法。
- **ForcedLeak（Noma，2025-09）**：指令写进 Salesforce 的线索表单。外泄用的域名本来在白名单里，但它**已经过期**，可以被任何人买下来［G41］。白名单必须持续维护。
- **Claude Pirate（Rehberger，2025）**：默认网络白名单中包含 `api.anthropic.com`，注入让模型用攻击者的 API key 把文件上传到攻击者账户，单次最多 30MB［G80］。合法的 API 域名也可以成为外泄通道。
- **图片缩放注入（Trail of Bits，2025-08）**：图片在原始分辨率下看不出异常，被系统缩放后才显现出指令；在 Gemini CLI 上外泄了日历数据，利用了 Zapier MCP 默认自动批准工具调用的设置［G44］。

### 跨案例规律

| 修复类型 | 案例 | 修复后是否有公开绕过 |
|---|---|---|
| 检测或清洗（概率性） | C Comet、D Gemini（分类器） | **有** |
| 收权限、封出口、加确认门（确定性） | A 去除图片、B Lockdown、F 只读 | 未见（B 出过实现漏洞） |

> **本章要点**：六个案例没有一个的根因是"模型不够聪明"，都是三要素同时存在。把确认门放在 Agent 可写的位置等于没有确认门（案例 E）；普通的写操作也可以是外传通道（案例 B、D、F）。

---

## 第 4 章　防御手段逐个评估

### 4.1 总表

| 防御 | 切断哪一环 | 能防 | 防不住 | 代价 | 证据强度 |
|---|---|---|---|---|---|
| 分类器、护栏模型 | 入口检测 | 模板化、低成本攻击；静态 AgentDojo 上让攻击成功率下降 57%［G66］ | 自适应攻击 >90%［G18］；"写给人看"的文本［G36］ | 误报，损失效用 | 强（结论一致：只能降概率） |
| 提示技巧（定界符、spotlighting、sandwich） | 模型解读 | 随手写的攻击：AgentDojo 中从 57.7% 降到 27.8%–41.7%［G69］ | 自适应攻击 >95%［G18］ | 几乎为零 | 强（便宜、有用、靠不住） |
| 模型训练（IH、对抗训练） | 模型内在 | 提高攻击门槛［G11］［G12］ | 自适应攻击 96%（Meta-SecAlign）［G18］ | 训练成本，可能过度拒绝 | 中 |
| Dual LLM | 不可信数据不进特权模型 | 不可信内容直接劫持工具调用 | 篡改数据值（例如把收件人换掉）［G15］ | 实现复杂（作者自评"pretty bad"） | 中 |
| CaMeL | 控制流和不可信数据分离，并在工具调用处执行策略 | AgentDojo 上以可证明安全完成 77% 的任务（无防御为 84%）［G15］ | 侧信道、多 Agent 组合［G75］、伪造数据［G77］ | Token 约 2.8 倍，需要编写和维护策略 | 中（缺少独立的自适应评测） |
| 信息流控制（FIDES 等） | 数据流出处按标签检查 | 开启策略检查后挡住 AgentDojo 全部攻击［G73］ | 不开策略时与普通规划器一样脆弱；策略写错 | 需要改造规划器 | 中 |
| 最小权限、工具过滤 | 缩小可调用的工具 | AgentDojo 中从 57.69% 降到 6.84%［G69］ | 完成任务所需的工具本身就能执行攻击（17% 的用例） | 低 | 中-强 |
| 出口白名单、禁止自动渲染 | 切断外泄 | 零点击图片外泄［G61］［G5］ | 白名单内的域名被滥用［G53］［G80］；破坏型操作 | 低到中 | 强 |
| 人工确认 | 高风险动作前设闸 | 低频、高价值的操作 | 审批疲劳［G94］；确认框被伪造［G81］ | 打断流程 | 中 |
| 沙箱（文件 + 网络） | 限制爆炸半径 | 本地破坏、密钥外泄［G79］ | 沙箱内允许的通道仍可外泄［G80］ | 环境配置 | 中-强 |

### 4.2 概率性防御：便宜、有用、靠不住

分类器、提示技巧和训练值得做，因为它们能挡住大量随手写的攻击，成本也低。例如 LLMail-Inject 竞赛中，叠加全部防御后，第二阶段没有出现成功的攻击［G70］。但它们**不能作为安全边界**，原因有两个：

1. 自适应攻击者可以针对防御本身做优化［G18］；
2. 成功的注入文本往往看起来完全无害，检测器要识别它们，就必须付出大量误报［G18］。

Willison 的说法是："in web application security 95% is very much a failing grade"［G6］。

几组具体数据，可以帮你建立对检测类防御的直觉：

- **静态评测**：Meta 的 LlamaFirewall 在 AgentDojo 上，把无防御时 17.6% 的攻击成功率，用 PromptGuard 2 降到 7.5%，再加上审查推理链的 AlignmentCheck 降到 1.75%；任务效用从 47.7% 降到 42.7%［G66］。论文自己也承认，这个评测集只覆盖"a narrow class of attacks"。
- **误报代价**：AgentDojo 原论文测试的一个 BERT 类检测器，把攻击成功率从 57.69% 降到 7.95%，但良性任务的完成率从 69.0% 降到 41.49%，作者评价它"has too many false positives"［G69］。
- **字符级绕过**：2024 年有人发现，只要在字符之间加空格、去掉标点，就能让 Prompt-Guard-86M 的识别准确率从 100% 降到 0.2%（后已修复）［G68］。

结论：检测器能拦下大量低成本攻击，但要用误报和效用来换；而且它的判断标准一旦被攻击者摸清，就能被针对性绕过。

### 4.3 架构类防御：把"可信控制流"和"不可信数据"分开

学术界的共识原则是："once an LLM agent has ingested untrusted input, it must be constrained so that it is impossible for that input to trigger any consequential actions"［G9］。

**Plan-then-Execute（先定计划，再执行）**：

```python
# 1. 只根据可信的用户请求制定计划，此时还没读任何外部内容
plan = planner_llm(user_request)          # 例如 [read_email(id=3), summarize, reply_to(user)]
# 2. 执行时，工具输出只能填进变量，不能改变"调用哪些工具"
for step in plan:
    result = run_tool(step)
    step.next_input = result              # 外部内容只是数据
```

它的局限是：注入改不了"调用哪个工具"，但仍然可能篡改工具的**参数**［G9］。

**CaMeL 的思路**更进一步：让模型把用户请求写成受限的程序，每个数据都带上"来源和可去向"的能力标签，由解释器（不是模型）在每次工具调用前检查策略［G15］：

```python
email   = get_email(id=3)               # 标签：来源=外部邮件（不可信）
summary = quarantined_llm(email)         # 隔离模型处理，标签随数据传递
send(to=user.address, body=summary)      # 策略检查：收件人来自可信的用户请求 → 放行
send(to=extract(email), body=secrets)    # 策略检查：收件人来自不可信数据 → 拒绝
```

代价与边界：

- 效用从 84% 降到 77%，Token 约 2.8 倍，还需要编写和维护策略［G15］；
- 它防的是"不可信数据改变控制流或数据流向"，**防不住**在允许的数据流内给出误导性回答，也防不住社会工程［G15］；
- 在分层多 Agent 系统中，单个 Agent 的保证不能直接组合。作者为此提出了 multi-CaMeL 协议，把攻击成功率降到 0.0%（预印本）［G75］；
- 还出现了一类新攻击"Agent Data Injection"：不注入指令，而是伪造资源标识符、数据来源等"可信数据"。据作者报告，它能绕过现有防御（预印本）［G77］。

**六种设计模式**［G9］，按对通用性的牺牲从大到小排列：

1. **Action-Selector**：只从预定义的动作里选，对注入免疫；
2. **Plan-then-Execute**：先定计划，见上；
3. **LLM Map-Reduce**：每份不可信文档由隔离的子 Agent 单独处理，一份恶意文档影响不到其他文档；
4. **Dual LLM**：特权模型从不直接接触不可信内容；
5. **Code-then-Execute**：即 CaMeL 的路线；
6. **Context-Minimization**：从上下文里删掉不需要的内容。

作者的判断是，基于当前的模型，"it is unlikely that general-purpose agents can provide meaningful and reliable safety guarantees"［G9］。**要换安全，就得有意限制通用性。**

### 4.4 权限与执行层：最实用的一层

- **最小权限、工具过滤**：在读取任何不可信数据之前，先选定本任务需要的工具。这个最简单的做法就把攻击成功率从 57.69% 降到了 6.84%［G69］。
- **出口控制**：禁止自动渲染外部图片，对外链做脱敏［G61］［G5］。要特别注意，**白名单本身就是一种能力授予**："Every function reachable through any domain on an allowlist is now an attack surface"［G95］。例如 Claude 代码解释器的默认白名单里有 `api.anthropic.com`，注入可以让模型用**攻击者的** API key 把文件传到攻击者账户［G80］。
- **沙箱**：必须同时隔离文件系统和网络。只隔离网络，Agent 可以逃出沙箱；只隔离文件，SSH key 可以被外传［G79］。
- **人工确认**：确认界面应展示确定性生成的参数或 diff，不能展示模型自己写的解释［G24］。不能有"超时即放行"这种设计，Copilot Studio 的外部监控就是这样一个反例［G101］。

### 4.5 怎么看防御论文和产品宣传里的数字

| 基准 / 数据集 | 测什么 | 已知局限 |
|---|---|---|
| AgentDojo（ETH） | 97 个任务、629 个安全用例，可扩展环境［G69］ | 默认攻击是静态的；已被指出容易饱和，指标和实现也有缺陷［G85］ |
| InjecAgent（UIUC） | 1,054 个用例；ReAct 提示的 GPT-4 有 24% 被攻击成功［G82］ | 偏单步，侧重测量 Agent 是否被诱导去执行攻击动作 |
| WASP（Meta） | 端到端 Web Agent；攻击部分成功的比例最高 86%［G83］ | 完整达成攻击目标的比例低得多，很可能是"security by incompetence" |
| ART（Gray Swan 等） | 22 个 Agent、44 个场景、180 万次注入；几乎所有 Agent 在 10–100 次查询内就出现违规［G84］ | 竞赛形式，场景固定 |
| LLMail-Inject（微软等） | 20.8 万条自适应攻击，只有 0.8% 端到端成功［G70］ | 攻击目标被限定为触发一次特定的发邮件调用 |

看到任何"攻击成功率 X%"时，先问三个问题：

1. **攻击是静态的还是自适应的？** 同一个防御，两种攻击下的数字可能是 1% 和 95% 的差别［G18］。
2. **每个攻击试了几次？** NIST 的测试中，重复 25 次就让成功率从 57% 升到 80%［G91］。
3. **Agent 本身能不能完成任务？** 攻击成功率低，可能只是 Agent 太弱，连攻击者想让它做的事都做不成［G83］。

---

## 第 5 章　参考架构与排查方法

### 5.1 各方口径

NCSC、NIST、OWASP 和四家主要厂商的立场基本一致［G2］［G90］［G24］［G5］［G61］［G95］：

- **假设注入一定会发生**；
- 主防线是**确定性的能力约束**；
- 概率性手段只用来降低发生的概率。

NCSC 给出的降权原则很好记："when an LLM processes information from a party, the privileges it has drops to that of the party"［G2］。也就是说，模型读了谁写的内容，它的权限就降到和谁一样。

### 5.2 分层参考架构

```mermaid
flowchart TB
    U["用户请求（可信）"] --> P["规划层<br/>只看可信输入，产出计划或程序"]
    subgraph 不可信区["不可信区（权限 = 内容作者的权限）"]
        W["网页、邮件、文档、issue、工具返回"] --> Q["隔离处理<br/>隔离模型 / 子 Agent，没有工具权限"]
    end
    P --> G{"策略闸门（不由 LLM 判断）<br/>工具白名单、参数校验、<br/>数据来源标签、速率限制"}
    Q -->|只作为数据传递| G
    G -->|低风险：只读、可逆| T["工具执行"]
    G -->|高风险：不可逆、对外、涉及金钱| H["人工确认<br/>展示确定性的 diff"]
    H --> T
    T --> S["沙箱<br/>文件隔离 + 网络默认拒绝 + 出口白名单"]
    S --> O["输出层<br/>不自动渲染外部图片或链接"]
    L["日志、监控、红队"] -.-> G
    L -.-> T
```

策略闸门的核心逻辑可以这样写：

```python
def gate(call, ctx):
    if call.tool not in ctx.allowed_tools:              # 本任务没选这个工具
        return DENY
    if ctx.touched_untrusted and call.tool.is_external:  # 三要素会话：读过不可信内容后对外发送
        return REQUIRE_HUMAN
    if any(arg.source == "untrusted" for arg in call.sensitive_args):  # 例如收件人、URL
        return DENY
    if call.tool.irreversible:
        return REQUIRE_HUMAN                             # 确认框展示确定性 diff，超时即拒绝
    return ALLOW
```

### 5.3 三类 Agent 的配置重点

| Agent 类型 | 难点 | 配置重点 | 实例 |
|---|---|---|---|
| 浏览器 Agent | 不可信输入无法避免，而且带着登录态 | 站点分为只读和可写两类；不带登录态的模式；敏感站点做确定性确认；用隔离的审查模型复核动作 | Chrome 的 User Alignment Critic 和 Origin Sets［G99］；Atlas 的 logged-out 模式 |
| 编程 Agent | 能执行命令、能写文件 | 文件 + 网络沙箱；默认无网络；写入限定在工作区；安全配置不可被 Agent 改写 | Codex 默认无网络［G97］；Claude Code 沙箱［G79］ |
| 企业办公 Agent | 访问私有数据是刚需 | 每个 Agent 一个独立身份，最小 scope；DLP；对外发送需确认；管理员可以一键撤销 | Google Workspace Studio 四层防护［G100］ |

### 5.4 实例：按风险分级确认

"每一步都确认"会让人疲劳，"全都不确认"又太危险。下面两个厂商实例展示了中间路线该怎么走：

**Claude Code auto mode（厂商自报）**［G94］：

| 级别 | 操作 | 处理方式 |
|---|---|---|
| 第 1 级 | 不改变状态的只读工具 | 固定白名单，直接放行 |
| 第 2 级 | 项目目录内的写入和编辑 | 直接放行（可以用版本控制回滚） |
| 其余 | shell 命令、网页抓取等 | 交给分类器判断；这个分类器**只看用户消息和工具调用，不看工具输出**，所以注入内容影响不到它 |
| 另外 | 工具输出 | 服务端探针扫描其中的注入 |

厂商公布的完整管线数据是：误报率 0.4%，对真实越权行为的漏报率 17%，对合成外泄的漏报率 5.7%。官方明确写道："It is not a drop-in replacement for careful human review on high-stakes infrastructure"［G94］。这里值得学的设计点是：**审查者看不到不可信内容**，自然也就不会被它注入。Chrome 的 User Alignment Critic 采用了同样的思路，它"architected to see only metadata about the proposed action"［G99］。

**Chrome 的确定性确认清单**［G99］：只在以下情况要求用户确认：访问银行或医疗网站（对照一份固定名单检查）、用密码管理器登录、购买或支付、发送消息。触发条件是确定性的，不让模型判断"这一步危险不危险"。

### 5.5 排查自己 Agent 的步骤（AI 建议，依据权威资料归纳）

1. **先判断值不值得用 Agent。** 如果系统承受不了注入成功的残余风险，就不该交给 LLM［G2］。不需要的自主性不要给（OWASP Least-Agency）［G24］。
2. **列出所有输入源，标注谁能写入。** 外人能写入的，一律标为不可信。
3. **列出所有工具的三种能力**：读敏感数据、写状态、对外通信。别漏掉隐式通道，比如图片渲染、链接预览、发评论。
4. **画数据流图，找三要素交汇点。** 对每个交汇点，选择拆会话、去掉一项能力，或者按数据来源降权［G7］［G6］。
5. **收紧凭证。** Agent 使用专用身份，不复用人的全权 token；凭证短期有效，权限逐步授予。
6. **加沙箱和出口控制。** 网络默认拒绝；白名单里每个域名能做的事都要逐一审视。
7. **在执行前加确定性闸门。** 校验工具和参数；高风险操作需确认；确认框展示 diff；超时即拒绝。
8. **再叠加概率性防护**：spotlighting、分类器。不可信内容不能放进 system 或 developer 消息［G96］。
9. **检查确认是否已经形同虚设。** 统计批准率，如果接近 100%，就改用沙箱或分级确认［G94］。
10. **用多次尝试的自适应红队测试验证。** 看每个任务的成功率，不要只看平均值［G91］。

---

## 第 6 章　争议与不确定

- **厂商数字和学术数字差距很大。** 厂商报告约 1% 甚至 0%［G13］［G108］，学术自适应攻击则在 90% 以上［G18］。两者的威胁模型不同：前者是固定基准或内部攻击者，后者针对具体防御、计算预算很大。目前**没有找到**针对最新"模型 + 系统防护"组合的独立自适应评测。
- **确认多一点还是少一点。** OpenAI 的 Agent Builder 指南建议"always enable tool approvals"［G96］，MCP 规范也写着"SHOULD always be a human in the loop"［G103］；Anthropic 则以 93% 的批准率为依据，主张用沙箱减少确认［G94］。合理的理解是：低频的业务流程可以多确认，高频的编程 Agent 应该少确认、强隔离。
- **架构类防御缺少同等强度的对抗评测。** CaMeL、FIDES 等目前只在静态基准上验证过；独立复现只有一个小规模的数据点（Progent，结果对防御有利）［G74］。
- **基准本身有问题。** 一个简单的输入防火墙加输出清洗器组合，就能在四个基准上做到满分，说明这些基准的攻击太弱，指标和实现也有缺陷［G85］。另外，攻击成功率低也可能只是"security by incompetence"［G83］。
- **NIST 的数据很能说明评估设定的重要性。** 2025-01，美国 AISI（现在的 CAISI）用 Claude 3.5 Sonnet 在 AgentDojo 上测试：同一攻击重复 25 次后，平均成功率从 57% 升到 80%；新开发的攻击把 Workspace 环境中的成功率从最强基线的 11% 提到 81%［G91］。2026-03，CAISI 分析了 Gray Swan 主办的公开竞赛数据（13 个前沿模型、400 多名参与者、25 万次以上攻击），所有模型都被至少攻破一次［G92］。
- **未核实的线索**：GitLost（GitHub Agentic Workflows 泄露私有仓库，2026-07）只找到媒体报道（C 级）；Copilot 修复"只防写入、不防加载"的说法来自第三方，未经独立验证。

---

## 第 7 章　对照选题地图

| 地图题号 | 覆盖情况 |
|---|---|
| **33**（提示词注入如何发生、怎么防） | ✅ 本报告完整回答 |
| 34（执行环境隔离） | 🟡 部分覆盖：沙箱、出口控制、密钥（第 4.4、5.3 节） |
| 29（人工确认的位置） | 🟡 部分覆盖：分级确认、审批疲劳（第 4.4、6 章） |
| 35（基准与真实表现的差距） | 🟡 部分覆盖：只涉及安全类基准（第 6 章） |
| 22（工具设计）、24（评估集）、28（读 trace） | ⬜ 没有覆盖 |

**建议下一步研究第 24 题（如何建立评估集）。** 本报告反复出现的结论是"评估方法决定你能不能相信防御"，第 24 题正好补上这块，而且和你的"应用实践"目的最贴近。

---

## 第 8 章　给你的行动建议（初级实操者 × 应用实践）

**本周可以做的三件事：**

1. **给你正在用的一个 Agent 画数据流图。** 可以是 Claude Code、带 MCP 的 Cursor，或者你自己写的 Agent。按第 5.5 节的步骤 2–4，标出所有三要素交汇点。只要画出来，通常就能发现一两个"同一个会话里既读外部内容、又能对外发送"的地方。
2. **审查 MCP 配置。** 每个 MCP 服务器的 token 权限是否最小？有没有开"始终允许"？有没有一个 MCP 同时具备三要素（参考案例 B、F）？
3. **亲手复现一次攻击。** 在本地搭一个最小 Agent（第 1.2 节那个循环），让它读一个你自己写的、含隐藏指令的网页，观察它是否照做；然后依次加上工具过滤、出口限制、确认门，看看哪一步切断了攻击链。

**一个练习项目（2–4 周）：**

用 AgentDojo 跑一遍基线，实现第 5.2 节的策略闸门，对比加闸门前后的攻击成功率和任务完成率。重点体会"安全换效用"的代价。如果条件允许，按 NIST 的建议，每个攻击重复多次。

**必读的 5 份一手资料：**

1. NCSC《Prompt injection is not SQL injection》［G2］：理解根因
2. Willison《The lethal trifecta》［G6］和 Meta《Agents Rule of Two》［G7］：排查工具
3. 《Design Patterns for Securing LLM Agents》［G9］：架构选型
4. 《The Attacker Moves Second》［G18］：理解为什么检测靠不住
5. Anthropic《How we contain Claude across products》［G95］：一家厂商的完整落地思路

---

## 信源

报告中引用的全部信源都在 `sources.md`（共 108 条，含核查阶段新增的 G107、G108），核查记录在 `factcheck.md`，各视角的原始笔记在 `notes/`。

关键信源：

- ［G2］NCSC, Prompt injection is not SQL injection, 2025-12-08
- ［G3］Zverev et al., Can LLMs Separate Instructions From Data?, ICLR 2025
- ［G6］Willison, The lethal trifecta, 2025-06-16
- ［G7］Meta, Agents Rule of Two, 2025-10-31
- ［G9］Beurer-Kellner et al., Design Patterns for Securing LLM Agents, 2025-06
- ［G15］Debenedetti et al., CaMeL, 2025-03/06
- ［G18］Nasr et al., The Attacker Moves Second, 2025-10
- ［G24］OWASP Top 10 for Agentic Applications 2026, 2025-12
- ［G26］Invariant Labs, GitHub MCP Exploited, 2025-05-26
- ［G36］EchoLeak 案例研究, arXiv 2509.10540
- ［G69］AgentDojo, NeurIPS 2024
- ［G73］Microsoft, FIDES, 2025
- ［G79］Anthropic, Claude Code sandboxing, 2025-10-20
- ［G91］NIST（美国 AISI / CAISI）, Strengthening AI Agent Hijacking Evaluations, 2025-01（2025-12 更新）
- ［G95］Anthropic, How we contain Claude across products, 2026-05-25
- ［G107］［G108］Claude Opus 5 / 5.5 System Card, 2026-07 / 2026-09
