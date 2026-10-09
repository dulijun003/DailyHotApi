# 视角 5：参考架构与落地实践

> 检索日期：2026-10-09。等级说明：A = 标准/官方文档/官方博客；B = 一线工程博客、学术论文；C = 二手报道，只作线索。
> 标注约定：【事实】指来源原文明确写到的内容（含厂商自报数据，自报数据会注明）；【观点】指来源作者的判断或主张；【整理】指本笔记在多个来源基础上的归纳，不是任何单一来源的原话。

## 子问题 1：权威机构和主要厂商推荐的分层防御思路是什么？

### 发现

**标准/政府机构**

- 【事实】OWASP LLM01:2025 列了 7 条预防措施：约束模型行为、定义并校验输出格式、输入输出过滤、权限控制与最小权限、高风险操作需人工批准、隔离并标识外部内容、对抗测试。其中"Require human approval for high-risk actions"和"Segregate and identify external content"是两条架构层面的措施。［S1］
- 【事实】OWASP Top 10 for Agentic Applications 2026（2025 年 12 月）把间接注入归入 ASI01 Agent Goal Hijack。它的缓解清单把"所有自然语言输入视为不可信"、"工具最小权限 + 高影响/改变目标的操作需人工批准"、"运行时校验用户意图与 agent 意图"、"日志与行为基线监控"、"定期红队"放在一起。它还提出"Least-Agency"原则：不需要的自主性不要给。［S2］
- 【事实】OWASP ASI02（工具滥用）建议了几种更具体的架构控件：按工具定义最小权限配置（作用域、速率、出站白名单），执行沙箱 + 出站白名单，"Policy Enforcement Middleware（Intent Gate）"把 LLM 输出当作不可信并在执行前校验，以及 JIT/短期凭证。［S2］
- 【事实】NIST AI 100-2e2025（2025 年 3 月）列出三类缓解：训练（含层级信任训练）、检测、输入处理（过滤、spotlighting、提示模型忽略数据中的指令）。它明确说现有手段不能完全防住，所以设计时应"假设注入一定可能发生"，例如使用"不同权限的多个 LLM"，或只通过定义良好的接口接触不可信数据。［S3］
- 【事实】NIST CAISI 的 agent hijacking 评估（2025-01，2025-12 更新）有三个结论：自适应攻击可以把成功率从 11% 提到 81%；重复尝试 25 次后，平均成功率从 57% 升到 80%；应看分任务结果，不能只看总体平均。［S4］2026-03 的红队竞赛对 13 个前沿模型做了 25 万次以上攻击，每个模型都被至少一次攻破。［S5］
- 【事实】英国 NCSC（2025-12-08）认为提示词注入"may never be totally mitigated"，应把 LLM 视作"inherently confusable deputy"。它要求设计上侧重"deterministic (non-LLM) safeguards that constrain the actions of the system"，引用"when an LLM processes information from a party, the privileges it has drops to that of the party"作为降权原则，警惕黑名单式过滤，要求记录完整的输入、输出和工具调用日志。它的组织框架对齐 ETSI TS 104 223。［S6］

**模型/平台厂商**

- 【事实】Microsoft MSRC（2025-07-29）的纵深防御分三层：预防（系统提示、Spotlighting）、检测（Prompt Shields 分类器）、影响缓解（数据治理 + 细粒度权限、确定性阻断外泄通道如 markdown 图片、人工确认）。研究方向是 FIDES 信息流控制。MSRC 自己把 Spotlighting 和 Prompt Shields 称为"probabilistic"，把权限控制称为"deterministically mitigated"。［S18］
- 【事实】Google GenAI 安全团队（2025-06-13）为 Gemini 设计了五层：注入内容分类器、security thought reinforcement、Markdown 清洗与可疑 URL 屏蔽、用户确认框架、终端用户安全提示。目标是"elevating the difficulty, expense, and complexity faced by an attacker"，而不是声称能根除。［S15］
- 【事实】Anthropic（2025-11-24）对浏览器 agent 的三层做法是：RL 训练抗注入、扫描所有进入上下文的不可信内容的分类器、持续红队。它自报的攻击成功率约 1%，并明确说"No browser agent is immune to prompt injection"。［S7］Anthropic 2026-05 的文章把原则表述为"Design for containment at the environment layer first, then steer behavior at the model layer"。［S11］
- 【事实】OpenAI Agent Builder 安全指南的建议有：不把不可信输入放进 developer message；节点之间用结构化输出（enum/schema）消除自由文本通道；"always enable tool approvals"；guardrail 只算第一层；用 trace grader 和 eval 做评估。［S12］OpenAI 关于 Atlas 的官方表态（经 CISO 公开发言）是："prompt injection remains a frontier, unsolved security problem"。［S14］
- 【事实】MCP 规范在 Tools 一节要求"there SHOULD always be a human in the loop with the ability to deny tool invocations"，客户端应在调用前向用户展示工具输入，并且"MUST consider tool annotations to be untrusted unless they come from trusted servers"。［S21］MCP Security Best Practices 主要处理授权层问题（confused deputy、token passthrough 禁止、SSRF、本地 MCP 服务器需同意 + 沙箱、scope 最小化）。［S20］

**归纳出的共同结构**

- 【整理】各方的分层大体一致，可归为四层：
  - ① 模型层：训练与指令层级，属概率性防御；
  - ② 输入/输出层：分类器、spotlighting、输出清洗，属概率性防御（Markdown 图片阻断这类除外，那是确定性的）；
  - ③ 能力层：最小权限、隔离、出站控制、按数据来源降权、策略引擎，属确定性防御；
  - ④ 人与运营层：高风险确认、日志监控、红队。
- 【观点】NCSC、Anthropic、Microsoft 都认为应以第③层为主，第①②层只用来降低概率。［S6］［S11］［S18］

### 冲突与不确定

- **攻击成功率差异很大。** Anthropic 自报浏览器 agent 约 1%［S7］；Claude for Chrome 早期数据是从 23.6% 降到 11.2%［S8］；NIST 竞赛显示所有前沿模型都能被攻破［S5］；CAISI 显示多次尝试会显著抬高成功率［S4］。这些数据的测试集、攻击预算和是否自适应各不相同，不能直接比较。厂商自报的低成功率不等于"可以不做架构隔离"。
- **OpenAI 原始博文未能直接读取。** OpenAI 关于 Atlas 加固的原文（2025-12）返回 403，相关内容只能依据 CISO 发言和媒体报道（TechCrunch 等）。有一个第三方页面声称 Atlas 将于 2026-08-09 停止服务，未找到 OpenAI 官方来源核实。
- **OWASP Agentic Top 10 的取材路径。** 本笔记依据的是从 genai.owasp.org 获取的 PDF 正文（Version 2026, December 2025）。官方资源页的准确 URL 未逐一核对。

## 子问题 2：如何按"信任边界"画 Agent 数据流，找出不可信内容与敏感能力相遇的位置？

### 发现

- 【事实】AWS 安全博客（2024-11-18）给出的通用威胁建模流程是：用 Shostack 四问（What are we working on / What can go wrong / What are we going to do about it / Did we do a good enough job）组织工作；画"from request to response"的数据流图（DFD）；用 STRIDE 辅助枚举威胁。博文示例中已有"Embed an indirect prompt injection in a webpage"这类攻击步骤。［S26］（注：此来源超过 12 个月，但方法论本身不随时间变化。）
- 【事实】Simon Willison 的"lethal trifecta"（2025-06-16）指以下三项同时出现：
  - "Access to your private data"
  - "Exposure to untrusted content"
  - "The ability to externally communicate"

  三者同时存在时，"an attacker can easily trick it into accessing your private data and sending it to that attacker"。他的结论是"The only way to stay safe there is to avoid that lethal trifecta combination entirely"。［S23］
- 【事实】Meta 的"Agents Rule of Two"（2025-10-31）把检查扩展为三个属性，要求一个会话内最多满足其中两个：
  - [A] 处理不可信输入
  - [B] 访问敏感系统或私有数据
  - [C] 改变状态或对外通信

  如果三者都需要，又不能拆到上下文全新的独立会话里，就不应自主运行，至少需要人工批准等监督。Meta 也说明它不是最终保障，例如用户可能不看警告就点批准。［S22］
- 【事实】NCSC 的检查法是：LLM 处理某一方的数据时，权限降到那一方的水平。例子是处理陌生外部邮件的 LLM 不应拥有特权工具。［S6］
- 【事实】OWASP ASI01 要求"把所有自然语言输入视为不可信"，并点名需要检查的连接数据源："RAG inputs, emails, calendar invites, uploaded files, external APIs, browsing output, and peer-agent messages"。这份清单可以直接用来标注 DFD 上的不可信入口。［S2］
- 【事实】Beurer-Kellner 等（2025-06，作者来自 IBM、Invariant Labs、ETH、Google、Microsoft 等机构）给出的核心约束是："once an LLM agent has ingested untrusted input, it must be constrained so that it is impossible" 让该输入触发有副作用的动作。论文提出 6 种模式：Action-Selector、Plan-Then-Execute、LLM Map-Reduce、Dual LLM、Code-Then-Execute、Context-Minimization。［S24］CaMeL 从可信查询中显式提取控制流和数据流，并用 capability 阻止私有数据外泄。在 AgentDojo 上，它以"provable security"完成 77% 的任务，无防御系统为 84%。［S25］
- 【事实】CSA 的 MAESTRO 框架是面向 agentic AI 的 7 层威胁建模框架：基础模型、数据运营、Agent 框架、部署基础设施、评估与可观测、安全合规、Agent 生态。它建立在 STRIDE、PASTA、LINDDUN 之上。［S27］（只读到检索摘要和二手介绍，未读原文。）
- 【整理】综合 S2、S6、S22、S23、S26，可操作的画法如下：
  1. 列出所有进入上下文的数据源，按"谁能写入它"标为可信或不可信（网页、邮件、日历、他人可编辑的文档、issue/PR、依赖 README、MCP 工具返回、其他 agent 消息都算不可信）；
  2. 列出所有工具，标出读敏感数据、写状态、对外通信三种能力（对外通信包括渲染外链图片、发起 HTTP、发邮件、提交 PR、发表评论等隐式通道）；
  3. 在 DFD 上找出"不可信数据进入同一上下文窗口，而该上下文又能调用 [B] 或 [C] 能力"的位置。这些位置就是 trifecta / Rule of Two 违规点；
  4. 对每个违规点，选择拆会话（降权）、加确定性门控（策略引擎/白名单/人工确认），或者移除其中一项能力。

### 冲突与不确定

- **两个检查法的范围不同。** lethal trifecta 只关注数据外泄（三要素都是外泄条件）［S23］；Meta Rule of Two 把 [C] 扩大到"改变状态"，因此也覆盖破坏性操作［S22］。两者对"什么算安全"的界定不同：只读私有数据并对外通信的 agent，在 Rule of Two 下若不处理不可信输入就是允许的；按 trifecta 也同样允许。差异主要出现在"不可信输入 + 写操作、但没有私有数据"的场景。
- **STRIDE 应用于 LLM agent 缺少权威官方指南。** 未找到 Microsoft 或 AWS 专门针对 LLM agent 的 STRIDE 官方指南，检索到的多为第三方博客（C 级，未采用）。AWS 博文只说 STRIDE"可以辅助"。
- **"可证明安全"的适用范围。** 学术方案（CaMeL、设计模式）给出可证明保证，但以牺牲效用为代价（77% vs 84%），并且只覆盖控制流/数据流劫持，不能防"在允许的数据流内给出错误答案"这类攻击。［S24］［S25］

## 子问题 3：安全与可用性如何权衡（approval fatigue、权限过紧）？

### 发现

- 【事实】Anthropic 的遥测显示"Claude Code users approve 93% of permission prompts"，并指出这会导致"approval fatigue, where people stop paying close attention to what they're approving"。［S10］
- 【事实】Anthropic（2025-10-20）的做法是用 OS 级沙箱代替逐条审批，并称"sandboxing safely reduces permission prompts by 84%"（内部使用数据）。它强调"effective sandboxing requires both filesystem and network isolation"：没有网络隔离会外泄 SSH key，没有文件隔离可以逃出沙箱获得网络。［S9］
- 【事实】Claude Code auto mode（2026-03-25）按风险分级处理工具调用：
  - Tier 1：不改变状态的只读工具走固定白名单，直接放行；
  - Tier 2：项目目录内的写入和编辑不经分类器，直接放行；
  - 其余操作（shell、web fetch 等）交给只看用户消息和工具调用、不看工具输出的分类器；
  - 另有服务端探针扫描工具输出中的注入。

  厂商自报的完整管线数据为：误报率 0.4%，对真实越权行为的漏报率 17%，对合成外泄的漏报率 5.7%。官方明确说"It is not a drop-in replacement for careful human review on high-stakes infrastructure"。［S10］
- 【事实】Anthropic（2026-05）的结论是：在边界内"the agent runs largely without interruption"；出站白名单本身是一种能力授予，"Every function reachable through any domain on an allowlist is now an attack surface"。［S11］
- 【事实】OWASP ASI09 的建议包括：
  - "Adaptive Trust Calibration"：按上下文风险评分动态调整自主度和人工监督；
  - 给用户看平台生成的风险摘要，而不是模型生成的理由（"plain-language risk summary (not model-generated rationales)"）；
  - "Separate preview from effect"。

  ASI02 要求高影响操作在批准前展示 dry-run 或 diff。［S2］
- 【事实】OWASP 早期的 Agentic AI Threats & Mitigations 指南有一项 T10"Overwhelming Human in the Loop"，讲的是攻击者故意制造大量审批请求，压垮人工审核。［S28］（只读到二手转述，C 级线索。OWASP ASI 文档的映射表中出现了"T10 Overwhelming"字样，可佐证该条目存在。）
- 【事实】MCP Security Best Practices 列出过宽 scope 的风险，包括"Consent abandonment: users decline dialogs listing excessive scopes"。它推荐渐进式最小权限：初始只给低风险的读或发现 scope，执行特权操作时再通过 `WWW-Authenticate` 逐步提权。［S20］
- 【事实】Meta 指出 Rule of Two 的人工批准可能失效，例如"user approves a warning without reading it"。［S22］
- 【事实】Google Chrome 只在少数确定性场景下要求确认：银行或医疗网站（"deterministic check against a list of sensitive sites"）、使用密码管理器登录、购买/支付、发送消息。［S16］
- 【整理】业界常见的取舍手段：
  - ① 按操作风险分级确认：只读放行，可逆写入放行，不可逆、对外或金融操作需确认［S10］［S16］［S2］；
  - ② 用环境隔离换取少确认：沙箱加网络默认拒绝［S9］［S11］［S13］；
  - ③ 读写分离：Chrome 的 read-only 与 read-writable origin［S16］；Atlas 的 logged-out 模式［S14］；
  - ④ 按会话或数据来源降权：NCSC 降权原则、Rule of Two 拆会话［S6］［S22］；
  - ⑤ 渐进授权或 JIT 凭证［S20］［S2］；
  - ⑥ 用确定性 UI 展示 diff 或预览，而不是让模型自己解释［S2］。

### 冲突与不确定

- **"每个操作都确认"还是"减少确认"。** OpenAI Agent Builder 指南建议"always enable tool approvals so end users can review and confirm every operation, including reads and writes"［S12］；MCP 规范也说"SHOULD always be a human in the loop"［S21］。Anthropic 则以 93% 批准率和审批疲劳为由，主张用沙箱和分类器减少确认［S9］［S10］。两种立场适用的产品形态不同（低频业务流程 vs 高频编程 agent），但字面上存在冲突。
- **分类器替代人工的效果。** 有二手报道称，Anthropic 研究里分类器拦下 89% 的危险命令，而人类只有 13.6%。未在 Anthropic 原文中找到这组数字，标为未核实。官方原文只给了误报率和漏报率（见上）。
- **审批的 fail-open 风险。** Microsoft Copilot Studio 的外部实时监控在超时时会放行："If no response arrives in time, the agent assumes approval and continues"［S19］。这与"高风险操作默认拒绝"的思路相反，部署时需要注意。

## 子问题 4：浏览器 Agent、编程 Agent、企业办公 Agent 的架构配置差异

### 发现

**浏览器 Agent**

- 【事实】Google Chrome（2025-12-08）的做法：
  - 用单独的"User Alignment Critic"模型在执行前复核每个动作，它"architected to see only metadata about the proposed action"，不接触不可信网页内容；
  - "Agent Origin Sets"把站点分为 read-only 和 read-writable 两类，扩展了站点隔离；
  - 注入分类器与规划模型并行运行；
  - 对银行、医疗、密码登录、支付和发消息做确定性确认。

  官方说法是"includes both deterministic and probabilistic defenses"。［S16］
- 【事实】Anthropic Claude for Chrome 提供：站点级授权（随时授予或撤销）；发布、购买、分享个人数据前确认；默认屏蔽金融服务、成人内容、盗版等高风险类别网站。早期数据显示，攻击成功率加防护后从 23.6% 降到 11.2%。［S8］
- 【事实】OpenAI Atlas 提供 logged-out 模式（不带用户凭证），官方建议"when you don't need to take action within your accounts"；logged-in 模式只适合"well-scoped actions on very trusted sites"；敏感站点使用 Watch Mode（要求标签页处于激活状态）。［S14］Simon Willison 批评说，让用户自己选模式是"an unfair burden"，而且他实测时 Watch Mode 未被触发。［S14］

**编程 Agent**

- 【事实】OpenAI Codex 的默认设置是"no network access and write permissions limited to the active workspace"。域名规则采用 allowlist-first，`.git` 目录强制只读。文档写明："Prompt injection can cause the agent to fetch and follow untrusted instructions"，并要求"Treat web results as untrusted"。［S13］
- 【事实】Claude Code 采用 OS 级沙箱：可以自由读取，只能在工作区写入，"network is denied by default"［S11］；文件和网络双重隔离［S9］；auto mode 分级审批［S10］。Anthropic 建议在隔离环境中使用 auto mode（来自二手报道；官方原文给出的表述是"不能替代高风险基础设施上的人工审查"）。

**企业办公 Agent**

- 【事实】Google Workspace Studio（2026-08-26）有四层防护：
  1. 滥用缓解，含间接注入防护；
  2. 身份隔离：每个 flow 使用独立的 OAuth Client ID，权限是所有者权限的最小子集；
  3. 管理员控制和用户确认，用于防止数据流向域外实体；
  4. 运行时防护，含 Gemini DLP 和 Studio DLP：受保护的 Drive 文件不可被引用，满足条件时需显式确认。

  管理员可以暂停所有 flow，也可以撤销单个 flow 的 scope。［S17］
- 【事实】Microsoft Copilot Studio 默认开启 XPIA 和 UPIA 防护，并可接入外部实时监控：执行前把计划发给外部系统审批。存在超时放行的情况。［S19］MSRC 强调用细粒度权限和数据治理确定性地限制影响，对外发送邮件等操作由用户亲自完成（"the user must explicitly approve the generated text and send the email themselves"）。［S18］
- 【事实】OWASP 建议把 AI Agent 纳入内部威胁（Insider Threat）项目，并使用 JIT 临时凭证且绑定用户会话。［S2］

**差异归纳**

- 【整理】三类 agent 的主要差异：
  - **浏览器 agent**：不可信输入（任意网页）不可避免，又带着用户登录态。核心手段是站点/来源级隔离、登录态隔离（logged-out）、敏感站点确定性确认，以及隔离的审查模型。
  - **编程 agent**：可以在环境层强隔离。核心手段是文件系统 + 网络沙箱、出站白名单、按工作区限定写入，确认只用于越界操作。
  - **企业办公 agent**：私有数据访问是刚需。核心手段是身份隔离（每个 agent 一个非人身份和最小 scope）、DLP 和标签、管理员集中治理与吊销、对外发送需确认。

### 冲突与不确定

- **浏览器 agent 能否依靠用户判断。** OpenAI 依赖用户选择 logged-in 或 logged-out 模式［S14］；Google 在浏览器侧做确定性的 Origin 隔离和隔离 critic［S16］。Simon Willison 认为把安全决策交给用户不公平［S14］。
- **Origin Sets 的细节。** 报道中关于 Origin Sets 的"trusted gating function"等细节来自二手报道，原文只确认了 read-only 与 read-writable 的划分。
- **企业 agent 缺少独立评测。** 未找到可靠来源对企业办公 agent 的注入攻击成功率做独立评测。

## 子问题 5：给初级实操者的排查步骤（按顺序，附依据）

### 发现

【整理】以下顺序是本笔记基于权威资料归纳的，不是任何单一机构发布的清单。每一步都标出了依据来源。

1. **先承认残余风险，判断这个用例是否适合 LLM。** 默认注入一定会发生；如果系统无法承受残余风险，就不该用 LLM 做这件事。依据：NCSC："If the system's security cannot tolerate the remaining risk, it may not be a good use case for LLMs"［S6］；NIST："design systems with the assumption that prompt injection attacks are possible"［S3］；OWASP 的 Least-Agency 原则：不需要的自主性就不要给［S2］。
2. **盘点输入源：列出所有进入上下文的数据，标记谁能写入。** 网页、邮件、日历、共享文档、issue/PR、依赖文件、RAG 文档、MCP 工具返回、其他 agent 消息，一律视为不可信。依据：OWASP ASI01 第 1 条和第 6 条［S2］；OWASP LLM01 的"Segregate and identify external content"［S1］。
3. **盘点能力：列出每个工具的读敏感数据、写状态、对外通信能力，包括隐式外泄通道。** 隐式通道如 markdown 图片、URL 预览、web fetch、提交 PR 或评论。依据：lethal trifecta［S23］；Microsoft 与 Google 对 markdown 图片外泄的确定性阻断［S18］［S15］；NIST 提到 markdown 图片可用于外泄［S3］。
4. **做 trifecta / Rule of Two 检查：** 找出"不可信输入 + 敏感数据 + 对外通信或写状态"三者同处一个会话的位置，优先拆会话、去掉一项能力，或按数据来源降权。依据：Meta Rule of Two［S22］；Simon Willison［S23］；NCSC 降权原则［S6］；设计模式论文［S24］。
5. **收紧权限和凭证：** 每个工具配最小权限，使用 agent 专用身份，不复用人的全权 token；scope 渐进授予，凭证短期有效；MCP 服务器不得透传 token。依据：OWASP ASI02 第 1 条和第 6 条［S2］；MCP Security Best Practices 的 Scope Minimization 和 Token Passthrough 部分［S20］；Google Workspace Studio 的身份隔离［S17］。
6. **加环境隔离和出站控制：** 代码和命令在沙箱中执行，文件系统与网络都隔离，网络默认拒绝，使用白名单，并把白名单内每个域名的可用功能视为攻击面；本地 MCP 服务器也放进沙箱。依据：Anthropic 沙箱与 containment 文章［S9］［S11］；Codex 默认无网络［S13］；OWASP ASI02 第 3 条［S2］；MCP Local Server Compromise 部分［S20］。
7. **在执行前加确定性门控：** 用策略引擎或"Intent Gate"校验工具名和参数；节点之间使用结构化输出；高风险、不可逆、对外操作需人工确认，确认界面展示参数或 diff，而不是模型的解释；避免超时放行。依据：OWASP ASI02 第 2 条和第 4 条、ASI09 第 4 条和第 7 条［S2］；OpenAI 结构化输出建议［S12］；MCP 的"Show tool inputs to the user before calling the server"［S21］；Chrome 的确定性确认［S16］；Copilot Studio 超时放行的反例［S19］。
8. **再叠加概率性防护：** spotlighting 或分隔标记、注入分类器（如 Prompt Shields）、指令层级。不可信内容不能放进 system 或 developer 消息。不要依赖关键词黑名单，也不要相信声称能"stop"注入的产品。依据：MSRC［S18］；Google 五层防御［S15］；OpenAI［S12］；NCSC 对 deny-listing 的警告［S6］。
9. **确认人工审批不会造成疲劳：** 统计审批次数和批准率；如果批准率接近 100%，说明审批已形同虚设，应改用沙箱或分级审批。依据：Anthropic 的 93% 批准率与 84% 降幅［S10］［S9］；OWASP ASI09 的 Adaptive Trust Calibration［S2］；Meta 关于盲目批准的提醒［S22］。
10. **日志、监控与告警：** 记录完整的 LLM 输入输出和工具调用，建立行为基线，对目标漂移、异常工具序列、失败的工具或 API 调用告警。依据：NCSC 关于记录与监控的部分［S6］；OWASP ASI01 第 7 条［S2］；MCP 的"Log tool usage for audit purposes"［S21］。
11. **用自适应、多次尝试的红队测试验证：** 使用 AgentDojo 等框架，看分任务的成功率而不是平均值，每个攻击重复多次。依据：NIST CAISI 的四条洞见［S4］；NIST 竞赛结果［S5］；OWASP LLM01 第 7 条与 ASI01 第 8 条［S1］［S2］。

### 冲突与不确定

- **排查顺序。** 未找到权威机构发布的"按顺序排查 agent 注入风险"的标准清单。上面的顺序是归纳结果：先架构（1–7），再概率性防护（8），最后运营（9–11）。这个排序与 NCSC、Anthropic"环境层优先"的立场一致［S6］［S11］，但 OWASP LLM01 的列表顺序是把"约束模型行为"放在第一位［S1］。
- **第 8 步的位置有分歧。** OpenAI 和 Google 把模型鲁棒性（如选用更抗注入的模型）列为重要手段［S12］［S15］；NCSC 认为这类手段"unlikely to be sufficient"［S6］。

## 本视角小结（3–5 条）

1. 【整理】NCSC、NIST、OWASP 和四家主要厂商在一点上基本一致：间接注入无法靠模型或过滤根除，应假设它必然发生，靠确定性的能力约束来限制后果。分类器、spotlighting、对抗训练只用于降低概率。［S3］［S6］［S7］［S14］［S18］
2. 【整理】最实用的威胁建模工具是在数据流图上做"lethal trifecta / Agents Rule of Two"检查：找出不可信输入、敏感数据、对外通信或写状态三者同处一个会话的位置，通过拆会话、降权或删除能力来切断。［S22］［S23］［S6］
3. 【事实 + 观点】人工确认不是万能的。Anthropic 数据显示用户批准 93% 的提示，存在审批疲劳。业界的趋势是用环境隔离（文件和网络沙箱、默认无网络）换取更少的确认，只对不可逆、对外、涉及金融的操作做确定性确认。但 OpenAI 和 MCP 的文档仍要求对每个操作确认，双方存在分歧。［S9］［S10］［S12］［S21］
4. 【整理】三类 agent 的重点不同：浏览器 agent 重在来源隔离和登录态隔离，编程 agent 重在沙箱和出站白名单，企业办公 agent 重在 agent 独立身份、最小 scope 和 DLP。［S13］［S14］［S16］［S17］
5. 【事实】评估必须是自适应的，并且要多次尝试。NIST 测得重复攻击可把成功率从 57% 抬到 80%，且所有前沿模型都被攻破。单次、静态测试会低估风险。［S4］［S5］

## 信源

- [S1] LLM01:2025 Prompt Injection｜OWASP GenAI Security Project｜2025（页面未标具体日期）｜A｜https://genai.owasp.org/llmrisk/llm01-prompt-injection/
  摘录："Require human approval for high-risk actions"；"Segregate and identify external content: Separate and clearly denote untrusted content to limit its influence on user prompts."
- [S2] OWASP Top 10 for Agentic Applications 2026｜OWASP GenAI Security Project, Agentic Security Initiative｜2025-12（Version 2026）｜A｜genai.owasp.org（PDF；资源页准确路径未逐一核对）
  摘录："Treat all natural-language inputs (e.g., user-provided text, uploaded documents, retrieved content) as untrusted."；"Policy Enforcement Middleware (“Intent Gate”). Treat LLM or planner outputs as untrusted."；"provide plain-language risk summary (not model-generated rationales)"；"deploying agentic behavior where it is not needed expands the attack surface without adding value."
- [S3] NIST AI 100-2e2025 Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations｜NIST｜2025-03｜A｜https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-2e2025.pdf
  摘录："Because current mitigations do not offer full protection against all attacker techniques, application designers may design systems with the assumption that prompt injection attacks are possible if a model is exposed to untrusted input sources, such as by using multiple LLMs with different permissions"
- [S4] Technical Blog: Strengthening AI Agent Hijacking Evaluations｜NIST CAISI｜2025-01-17（2025-12-19 更新）｜A｜https://www.nist.gov/node/1872381
  摘录："Testing the success of attacks on multiple attempts may yield more realistic evaluation results."；"analyze task-specific attack performance in addition to aggregate performance"
- [S5] Insights into AI Agent Security from a Large-Scale Red-Teaming Competition｜NIST CAISI｜2026-03-23｜A｜https://www.nist.gov/blogs/caisi-research-blog/insights-ai-agent-security-large-scale-red-teaming-competition
  摘录："at least one successful attack was found against all of the target frontier models"
- [S6] Prompt injection is not SQL injection (it may be worse)｜UK NCSC（David C, Technical Director for Platforms Research）｜2025-12-08｜A｜https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection
  摘录："Design protections need to therefore focus more on deterministic (non-LLM) safeguards that constrain the actions of the system, rather than just attempting to prevent malicious content reaching the LLM."；"when an LLM processes information from a party, the privileges it has drops to that of the party"；"If the system’s security cannot tolerate the remaining risk, it may not be a good use case for LLMs."
- [S7] Mitigating the risk of prompt injections in browser use｜Anthropic｜2025-11-24｜A｜https://www.anthropic.com/research/prompt-injection-defenses
  摘录："No browser agent is immune to prompt injection."；"A 1% attack success rate—while a significant improvement—still represents meaningful risk."
- [S8] Piloting Claude for Chrome｜Anthropic｜2025-08-25（2025-11-24、2025-12-18 更新）｜A｜https://claude.com/blog/claude-for-chrome
  摘录："Claude asks users before taking high-risk actions like publishing, purchasing, or sharing personal data."；"Browser use without our safety mitigations showed a 23.6% attack success rate when deliberately targeted by malicious actors."
- [S9] Beyond permission prompts: making Claude Code more secure and autonomous｜Anthropic Engineering｜2025-10-20｜A｜https://www.anthropic.com/engineering/claude-code-sandboxing
  摘录："sandboxing safely reduces permission prompts by 84%"；"effective sandboxing requires both filesystem and network isolation"
- [S10] How we built Claude Code auto mode: a safer way to skip permissions｜Anthropic Engineering｜2026-03-25｜A｜https://www.anthropic.com/engineering/claude-code-auto-mode
  摘录："Claude Code users approve 93% of permission prompts."；"It is not a drop-in replacement for careful human review on high-stakes infrastructure."
- [S11] How we contain Claude across products｜Anthropic Engineering｜2026-05-25｜A｜https://www.anthropic.com/engineering/how-we-contain-claude
  摘录："Design for containment at the environment layer first, then steer behavior at the model layer."；"Every function reachable through any domain on an allowlist is now an attack surface."；"protection in the model layer will never be 100% effective, which is why it can't stand alone."
- [S12] Safety in building agents｜OpenAI 开发者文档｜未标日期（2026-10 访问）｜A｜https://developers.openai.com/api/docs/guides/agent-builder-safety
  摘录："injecting untrusted input directly into developer messages gives attackers the highest degree of control"；"always enable tool approvals so end users can review and confirm every operation, including reads and writes"
- [S13] Agent approvals & security（Codex 文档）｜OpenAI｜未标日期（2026-10 访问）｜A｜https://learn.chatgpt.com/docs/agent-approvals-security
  摘录："Defaults include no network access and write permissions limited to the active workspace."；"Prompt injection can cause the agent to fetch and follow untrusted instructions."
- [S14] OpenAI CISO Dane Stuckey on ChatGPT Atlas（转引 CISO 公开声明并附评论）｜Simon Willison's Weblog｜2025-10-22｜B（引述内容为 OpenAI 官方表态）｜https://simonwillison.net/2025/Oct/22/openai-ciso-on-atlas/
  摘录："prompt injection remains a frontier, unsolved security problem"；"We recommend this mode when you don't need to take action within your accounts."；（Willison 评论）"an unfair burden to place on almost any user"
  补充：OpenAI 2025-12 的 Atlas 加固博文原文访问返回 403，只见到 TechCrunch 等报道（https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/，C 级线索）。
- [S15] Mitigating prompt injection attacks with a layered defense strategy｜Google GenAI Security Team｜2025-06-13｜A｜https://blog.google/security/mitigating-prompt-injection-attacks/
  摘录："Markdown sanitization and suspicious URL redaction"；"User confirmation framework"；"meaningfully elevating the difficulty, expense, and complexity faced by an attacker"
- [S16] Architecting Security for Agentic Capabilities in Chrome｜Google Chrome Security（Nathan Parker）｜2025-12-08｜A｜https://security.googleblog.com/2025/12/architecting-security-for-agentic.html
  摘录："The User Alignment Critic runs after the planning is complete to double-check each proposed action."；"Read-writable origins are those on which the agent is allowed to actuate (e.g., click, type)."；"based on a deterministic check against a list of sensitive sites"
- [S17] Defend against agentic risks with multi-layered protections in Google Workspace Studio｜Google Workspace Blog｜2026-08-26｜A｜https://workspace.google.com/blog/identity-and-security/defend-against-agentic-risks-with-multi-layered-protections-in-google-workspace-studio
  摘录："Studio generates a dedicated OAuth Client ID that is restricted to a least privileged subset of the owner's permissions"；"any steps executed by Gemini are prohibited from referencing context in protected Drive files"
- [S18] How Microsoft defends against indirect prompt injection attacks｜Microsoft MSRC（Andrew Paverd）｜2025-07-29｜A｜https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks
  摘录："a probabilistic technique to help the LLM distinguish user-provided instructions from potentially untrusted external text"；"This can be deterministically mitigated using fine-grained permissions and access controls"；"the user must explicitly approve the generated text and send the email themselves"
- [S19] Strengthen agent security with near-real-time protection in Microsoft Copilot Studio｜Microsoft Copilot Blog｜2025-09-08｜A｜https://microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/strengthen-agent-security-with-near-real-time-protection-in-microsoft-copilot-studio
  摘录："Copilot Studio includes default protections against both XPIA and user prompt injection attacks (UPIA)."；"If no response arrives in time, the agent assumes approval and continues."
- [S20] Security Best Practices｜Model Context Protocol 规范（draft 版）｜2026-10 访问（持续更新）｜A｜https://modelcontextprotocol.io/specification/draft/basic/security_best_practices
  摘录："MCP servers **MUST NOT** accept any tokens that were not explicitly issued for the MCP server."；"Consent abandonment: users decline dialogs listing excessive scopes"；"Execute MCP server commands in a sandboxed environment with minimal default privileges"
- [S21] Tools｜Model Context Protocol 规范 2025-11-25｜2025-11-25｜A｜https://modelcontextprotocol.io/specification/2025-11-25/server/tools
  摘录："For trust & safety and security, there **SHOULD** always be a human in the loop with the ability to deny tool invocations."；"Show tool inputs to the user before calling the server, to avoid malicious or accidental data exfiltration"；"clients **MUST** consider tool annotations to be untrusted unless they come from trusted servers."
- [S22] Agents Rule of Two: A Practical Approach to AI Agent Security｜Meta AI｜2025-10-31｜A｜https://ai.meta.com/blog/practical-ai-agent-security/
  摘录："[A] An agent can process untrustworthy inputs"；"[B] An agent can have access to sensitive systems or private data"；"[C] An agent can change state or communicate externally"
- [S23] The lethal trifecta for AI agents: private data, untrusted content, and external communication｜Simon Willison｜2025-06-16｜B｜https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
  摘录："an attacker can easily trick it into accessing your private data and sending it to that attacker"；"The only way to stay safe there is to avoid that lethal trifecta combination entirely."
- [S24] Design Patterns for Securing LLM Agents against Prompt Injections｜Beurer-Kellner et al.（arXiv 2506.08837）｜2025-06（v3 2025-06-27）｜B｜https://arxiv.org/abs/2506.08837
  摘录："once an LLM agent has ingested untrusted input, it must be constrained so that it is impossible"（后半句：该输入不能触发任何有负面副作用的动作）
- [S25] Defeating Prompt Injections by Design (CaMeL)｜Debenedetti et al., Google/ETH（arXiv 2503.18813）｜2025-03（v2 2025-06）｜B｜https://arxiv.org/abs/2503.18813
  摘录："explicitly extracts the control and data flows from the (trusted) query"；"solving 77% of tasks with provable security"（无防御系统为 84%）
- [S26] Threat modeling your generative AI workload to evaluate security risk｜AWS Security Blog｜2024-11-18｜A（超过 12 个月，仅用于方法论）｜https://aws.amazon.com/blogs/security/threat-modeling-your-generative-ai-workload-to-evaluate-security-risk
  摘录："You can also use a structured framework such as STRIDE to aid you in your thinking."；"Embed an indirect prompt injection in a webpage"
- [S27] Agentic AI Threat Modeling Framework: MAESTRO｜Cloud Security Alliance（Ken Huang）｜2025｜B（只读到检索摘要，未读原文）｜https://cloudsecurityalliance.org/articles/agentic-ai-threat-modeling-framework-maestro
  摘录：未获取原文逐字摘录。检索摘要称其为 7 层框架，建立在 STRIDE、PASTA、LINDDUN 之上。
- [S28] OWASP Agentic AI – Threats and Mitigations（T10 Overwhelming Human in the Loop）｜OWASP（经 HUMAN Security 等二手介绍）｜2025-02｜C（线索）｜https://humansecurity.com/learn/blog/agentic-ai-security-owasp-threats
  摘录：未获取 OWASP 原文逐字摘录。二手描述为 agent 产生超过人能审阅数量的审批请求，且可被攻击者故意放大。
