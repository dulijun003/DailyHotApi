# 视角 2：攻击面与手法全景

> 检索日期：2026-10-09。来源等级：A＝官方文档/论文/官方博客/一手数据；B＝一线工程博客/权威媒体原创报道；C＝自媒体/转载（只作线索）。
> 说明：部分页面无法直接抓取（OpenAI 官方博客、Aim Security 原文、NVD 返回 403 或空页），这些地方已改用可访问的论文或媒体报道，并在正文注明。

## 子问题 1：不可信内容进入 Agent 的入口有哪些

### 发现
- 【事实】最早系统梳理"间接注入入口"的是 Greshake 等人（2023），把投递方式分为四类："Passive methods (by retrieval)"（检索，如网页、社交媒体、代码仓库）、"Active methods (e.g., emails)"（主动投递）、"User-driven injections"（诱导用户粘贴）、"Hidden injections"（多阶段、图片、编码）。论文原文写道："any prompts/instructions written on a page (while being invisible to the user) can be effectively injected and affect the model"。［S1］
- 【事实】OWASP LLM01:2025 的定义是："Indirect prompt injections occur when an LLM accepts input from external sources, such as websites or files."，示例场景覆盖网页隐藏指令、RAG 文档、简历和图片。［S2］
- 【事实】MITRE ATLAS 把间接注入（AML.T0051.001）定义为经由"separate data channel ingested by the LLM such as include text or multimedia pulled from databases or websites"注入，并另设多项入口专属技术：RAG Poisoning（AML.T0070）、AI Agent Tool Data Poisoning（AML.T0099，2025-11-25 新增）、AI Agent Clickbait（AML.T0100，针对浏览器/计算机操作 Agent）。［S3］
- 【事实】OWASP Agentic Top 10（2025-12）在 ASI01 中列出的入口包括"prompt-based manipulation, deceptive tool outputs, malicious artefacts, forged agent-to-agent messages, or poisoned external data"，并点名"email, calendar, teams"等外部通信渠道。［S4］
- 按入口分类的示例（每条一句话加出处；详细复盘由其他视角负责）：
  - **网页/搜索结果**：【事实】Brave 演示，藏在 Reddit 评论 spoiler 标签里的指令让 Perplexity Comet 读取用户邮箱和 OTP 并外传。［S13］【事实】Unit 42 于 2026-03 报告了野外网页 IDPI，称其为"the first reported detection of a real-world example of malicious IDPI"（广告审核 Agent 被绕过）。［S14］【事实】Google 扫描 CommonCrawl 后称："We saw a relative increase of 32% in the malicious category between November 2025 and February 2026."［S15］
  - **邮件**：【事实】EchoLeak（CVE-2025-32711）是"a zero-click prompt injection vulnerability in Microsoft 365 Copilot"，一封精心构造的邮件即可触发外泄。［S16］
  - **日历邀请**：【事实】SafeBreach 演示攻击者"simply by sending them a Google calendar invite"即可劫持 Gemini，后续动作包括控制智能家居、外泄邮件。［S12］
  - **文档（含隐藏文字）**：【事实】OWASP ASI01 场景 4："A malicious Google Doc injects instructions for ChatGPT to exfiltrate user data"。［S4］【事实】Rehberger 演示，文档内嵌指令让 Gemini 把攻击者选定的信息写进长期记忆。［S18］
  - **代码仓库与 issue/PR**：【事实】Invariant Labs 演示通过"a malicious GitHub Issue"劫持接入 GitHub MCP 的 Agent，并"coerce it into leaking data from private repositories"。［S6］【事实】Legit Security 的 CamoLeak 把指令写成"a hidden comment inside the PR description"。［S20］【事实】Copilot CVE-2025-53773 的注入源可以是"a prompt injection planted in a source code file, web page, GitHub issue"。［S19］
  - **工具返回值/业务数据字段**：【事实】Noma 的 ForcedLeak 中，攻击者把指令写进 Salesforce Web-to-Lead 表单："The attacker places malicious content in a web form, which gets stored in the system's database."［S21］【事实】Cato 演示，"A threat actor (acting as an external user) submits a malicious support ticket"，工单内容经 Atlassian MCP 进入内部 AI 动作。［S22］
  - **MCP 工具描述**：【事实】Invariant Labs 把工具投毒定义为"malicious instructions are embedded within MCP tool descriptions that are invisible to users but visible to AI models"。［S5］
  - **RAG 知识库**：【事实】PoisonedRAG 报告："PoisonedRAG could achieve a 90% attack success rate when injecting five malicious texts"（USENIX Security 2025）。［S10］
  - **长期记忆**：【事实】Rehberger："Through prompt injection from untrusted data, attackers could insert long-term persistent spyware into ChatGPT's memory."［S17］【事实】MINJA 论文："The attacker injects malicious records into the memory bank by only interacting with the agent via queries"。［S11］
  - **其他 Agent 的输出**：【事实】AppOmni（2025-11）演示 ServiceNow Now Assist 的"second-order prompt injection"：数据字段中的指令借助 agent discovery 让无害 Agent 调用更高权限的同队 Agent。［S23］【事实】Prompt Infection 论文："malicious prompts self-replicate across interconnected agents"。［S9］
  - **图片/多模态**：【事实】Trail of Bits："when scaled, these images can reveal prompt injections that are not visible at full resolution"，在 Gemini CLI 上外泄了日历数据。［S24］【事实】Brave（2025-10）："Malicious instructions embedded as nearly-invisible text within the image"（截图注入）。［S25］【事实】OWASP LLM01 场景 7 与 ATLAS AML.T0068 都写到指令可藏在图片像素或 EXIF/ID3 等元数据里。［S2］［S3］
- 【观点】Anthropic（2025-11）认为浏览器 Agent 的入口无处不在："every webpage an agent visits is a potential vector for attack"。［S26］

### 冲突与不确定
- **GitHub MCP 案例的入口归类不一致**：Invariant 原文说入口是"malicious GitHub Issue"（数据/工具返回值）［S6］；OWASP ASI04 引用它时写的是"a malicious public tool hides commands in its metadata"（工具元数据）［S4］。两种说法都列在这里，以一手来源 Invariant 为准更稳妥。
- **"野外首例"的说法与规模**：Unit 42 称其为首个真实恶意 IDPI 检测［S14］；Google 认为"the observed activity suggests limited sophistication"，但恶意类别相对增长 32%［S15］。两者扫描的数据集和方法不同（Unit 42 用遥测数据，Google 用 CommonCrawl，且后者不覆盖主流社交媒体），数字不能直接比较。
- MITRE ATLAS 的数据来自 GitHub 上已标注"deprecated"的 `dist/ATLAS.yaml`（v5.6.0），官网技术页抓取返回 404，最新条目可能已有调整。

## 子问题 2：典型手法

### 发现
- **隐藏文本（白字、零字号、CSS 隐藏、HTML 注释）**
  - 【事实】ATLAS AML.T0068 LLM Prompt Obfuscation 列出"small text, text colored the same as the background, or hidden HTML elements"，以及 base64/rot13 编码。［S3］
  - 【事实】Unit 42 在野外看到"22 distinct techniques"，包括"Setting font-size: 0px and line-height: 0"、"display: none"、"opacity: 0"、极端负坐标等；投递方式中，可见明文占 37.8%，HTML 属性隐藏占 19.8%，CSS 渲染隐藏占 16.9%。［S14］
  - 【事实】HTML/Markdown 注释：CamoLeak 把指令写在 PR 描述的隐藏注释里，网页界面不显示，但 Copilot 会读到。［S20］Unit 42 原文没有把 HTML 注释列为隐藏手法（抓取摘要的结论）。［S14］
- **零宽字符与 Unicode tag 字符（ASCII smuggling）**
  - 【事实】Rehberger（2024-01）："The Tags Unicode Block mirrors ASCII"，"because it is often not rendered in the UI, the special text remains unnoticable to users"，并称这种方法"allows smuggling of data in plain sight!"［S7］（注：该原页面本身也藏有 tag 字符注入，抓取时已忽略。）
  - 【事实】AWS（2025-09-30）指出 tag 字符范围是"U+E0000 to U+E007F"，LLM"can read, interpret, and act on these hidden characters placed with Unicode tags"。［S8］
  - 【事实】Pillar Security（2025-03）的 Rules File Backdoor 用"invisible Unicode characters such as zero-width joiners and bidirectional text markers"，把指令藏在 Cursor/Copilot 的规则文件里。［S27］
- **通过 Markdown 图片或链接外泄数据**
  - 【事实】Microsoft MSRC（2025-07-29）：注入可以"cause the LLM output an HTML image tag or equivalent in markdown where the source URL is the attacker's server"，也可以输出"a clickable link to the attacker's server"。［S28］
  - 【事实】CamoLeak 预先生成一组 GitHub Camo 代理图片 URL，靠请求顺序逐字符外泄，绕过了 CSP。GitHub 的修复方式是"disabling image rendering in Copilot Chat completely"。［S20］
  - 【事实】ForcedLeak 利用 CSP 白名单里一个已过期、可被买下的域名作为外泄通道："The domain my-salesforce-cms.com was whitelisted but had expired"。［S21］
  - 【观点】Simon Willison 认为，只要工具能"make an HTTP request—to an API, or to load an image, or even providing a link for a user to click"，就构成外泄通道（"lethal trifecta"的第三要素）。［S29］
- **MCP 工具描述投毒（tool poisoning）与影子化（shadowing）**
  - 【事实】Invariant Labs（2025-04-01）的定义见上文；shadowing 是指"A malicious server injects a tool description that modifies the agent's behavior with respect to a trusted service or tool"。［S5］
  - 【事实】ATLAS AML.T0110 AI Agent Tool Poisoning 归在 Persistence 战术下："By altering tool behavior such as modifying parameters or descriptions, injecting hidden logic, or redirecting outputs, attackers can maintain long-term influence"。［S3］
  - 【事实】OWASP ASI04 列有"Tool-descriptor injection"，并举出在 npm 上冒充 postmark-mcp、"secretly BCC'd emails to the attacker"的恶意 MCP 服务器。［S4］
- **工具定义上线后被篡改（rug pull）**
  - 【事实】Invariant："a malicious server can change the tool description after the client has already approved it"。［S5］
  - 【事实】Simon Willison（2025-04-09）的文章写道："MCP tools can mutate their own definitions after installation."，"You approve a safe-looking tool on Day 1, and by Day 7 it's quietly rerouted your API keys to an attacker."［S30］
  - 【事实】协议层面，MCP 规范允许服务器在工具列表变化时发出 `notifications/tools/list_changed`，并要求"clients MUST consider tool annotations to be untrusted unless they come from trusted servers"。也就是说，协议本身支持工具定义动态变化。［S31］
- **记忆持久化投毒**
  - 【事实】ATLAS AML.T0080.000 Memory（2025-09-30 新增）："an adversary can inject memories via Direct or Indirect Prompt Injection"；AML.T0080.001 Thread 指出，在共享线程（如 Slack 频道）中，"a single malicious message from one user can influence the agent's behavior in future interactions with others"。［S3］
  - 【事实】Rehberger 的 Gemini "Delayed Tool Invocation"：攻击者先"pollutes the chat context with instructions and a trigger action"，等用户说出触发词，Gemini 才写入记忆。［S18］
  - 【事实】ChatGPT spAIware 实现了"continuous data exfiltration of any information the user typed"，而且跨会话持续。［S17］
- **多 Agent 之间传播（AI 蠕虫）**
  - 【事实】Morris II（Cohen、Bitton、Nassi）："an attacker can initiate a computer worm-like chain reaction that we call Morris-II"，借助自复制提示在 RAG 邮件助手之间传播。［S32］
  - 【事实】ATLAS AML.T0061 LLM Prompt Self-Replication："cause the LLM to replicate the prompt as part of its output. This allows the prompt to propagate to other LLMs and persist on the system."［S3］
  - 【事实】Greshake 等人在 2023 年已提出"Prompts as worms"。［S1］Prompt Infection 论文研究的是多 Agent 系统内部的自复制。［S9］
- **其他手法（补充）**：多阶段载荷（先注入小段，再拉取大段）、编码/多语言载荷［S1］［S3］；拆分载荷（OWASP LLM01 场景 6 "split malicious prompts"）［S2］；图片缩放隐写［S24］；"Clickbait"诱导计算机操作 Agent 复制并执行代码（AML.T0100）［S3］；修改 Agent 配置以开启自动批准（Copilot 的 `"chat.tools.autoApprove": true`，即"YOLO mode"）［S19］。

### 冲突与不确定
- **工具投毒在框架里的归属不统一**：OWASP 把运行时篡改合法工具接口归入 ASI02（Tool Misuse），把源头即恶意的工具归入 ASI04（Supply Chain）［S4］；ATLAS 把 AML.T0110 放在 Persistence 战术下［S3］；Invariant 把它看作间接注入的一种形式［S5］。
- **Rug pull 引文出处**：S30 中那两句话很可能是 Willison 引用的他人文章（Elena Cross "The S in MCP stands for security"），我未回到原文核实，引用时应写成"Willison 文中引述"。
- **Unicode tag 是否一定能被模型读取**：Rehberger 用的是推测语气（"suggesting tokenizers can handle these characters"）［S7］；AWS 指出模型和运行时"can interpret the same character sequence in dramatically different ways"［S8］。实际效果取决于具体模型和分词器，未找到跨模型的系统性测量。
- CamoLeak 的 CVE 编号（CVE-2025-59145）只见于二手报道，Legit 原文摘要中没有核实到。

## 子问题 3：攻击目标分类与权威框架

### 发现
- 【事实】Greshake 等人（2023）按威胁分为 Information Gathering、Fraud、Intrusion、Malware、Manipulated Content、Availability，并在摘要中概括为"data theft, worming, information ecosystem contamination"。［S1］
- 【事实】OWASP LLM01:2025 列出的后果有："Disclosure of sensitive information"、"Revealing sensitive information about AI system infrastructure or system prompts"、"Content manipulation leading to incorrect or biased outputs"、"Providing unauthorized access to functions available to the LLM"、"Executing arbitrary commands in connected systems"、"Manipulating critical decision-making processes"。［S2］
- 【事实】OWASP Top 10 for Agentic Applications 2026（发布于 2025-12-09）有 ASI01 到 ASI10 共十项。与本视角直接相关的有：ASI01 Agent Goal Hijack（对应间接注入）、ASI02 Tool Misuse and Exploitation、ASI04 Agentic Supply Chain Vulnerabilities（工具描述符注入、恶意 MCP）、ASI06 Memory & Context Poisoning（持久化）、ASI07 Insecure Inter-Agent Communication、ASI08 Cascading Failures（扩散）。其中 ASI01 与 LLM01 的区别写作："Unlike LLM01:2025, which focuses on altering a single model response, ASI01 captures the broader agentic impact where manipulated inputs redirect goals, panning (when used) and multi-step behavior."；ASI06"focuses on persistent corruption of agent memory and retrievable context that propagates across sessions"。［S4］
- 【事实】MITRE ATLAS 按战术组织：AML.T0051 LLM Prompt Injection 在数据中归入 Execution（AML.TA0005），描述里同时说它"can be an initial access vector"；AML.T0070 RAG Poisoning、AML.T0080 Context Poisoning、AML.T0061 Self-Replication、AML.T0110 Tool Poisoning 归入 Persistence（AML.TA0006）；外泄类有 AML.T0086 Exfiltration via AI Agent Tool Invocation（"Sensitive information can be encoded into the tool's input parameters"）；破坏类有 AML.T0101 Data Destruction via AI Agent Tool Invocation。［S3］
- 【事实】Microsoft MSRC 把影响归为两类："Data exfiltration"和"Unintended actions"。［S28］
- 【事实】野外数据给出的意图分布：Google 分为"Harmless pranks""Helpful guidance""Search engine optimization (SEO)""Deterring AI agents""Malicious"（下分 Data exfiltration、Destruction）［S15］；Unit 42 按意图分 low/medium/high/critical 四级，占比较高的是 Irrelevant output 28.6%、Data destruction 14.2%、AI content moderation bypass 9.5%［S14］。
- 综合来看，题目给出的五类目标在框架中的对应位置：
  - 数据外泄：LLM01 / ASI01，ATLAS T0086
  - 越权执行动作：LLM01 "unauthorized access to functions"，ASI02/ASI03
  - 篡改输出：LLM01 "Content manipulation"，Greshake "Manipulated Content"
  - 持久化：ASI06，ATLAS Persistence 战术（T0070/T0080/T0110）
  - 扩散传播：ASI07/ASI08，ATLAS T0061，Greshake "worming"
  
  这五类都能在上述框架中找到对应项（对应关系是本文整理，框架原文没有这样排列）。另外，Greshake 有 Availability、Unit 42 和 Google 有"Deterring AI agents / Irrelevant output / SEO"这类偏低危目标，五分类没有覆盖。
- 【观点】SafeBreach 用 TARA 按四类损害评分："privacy, financial, safety, and operational"。［S12］

### 冲突与不确定
- **ATLAS 中提示注入的战术归属**：官方数据把 AML.T0051 放在 Execution［S3］，有二手来源把它放在 Initial Access（C 级，仅作线索）。ATLAS 描述里两种说法都出现了。
- **OWASP 内部边界有重叠**：ASI01 与 ASI06 的区分依据是"是否持久"，但原文也承认"memory poisoning frequently leads to goal hijacking (ASI01)"［S4］。实际报告同一事件时可能归入不同类别。
- 未找到 NIST 对 IPI 的分类原文（只在二手来源中看到"greatest security flaw"一说），所以未纳入。

## 子问题 4：不同类型 Agent 的主要攻击面

### 发现
- **浏览器 / 计算机操作 Agent**：主要入口是任意网页、用户生成内容（评论、论坛）、截图和图片、导航本身。
  - 【事实】Brave 的 Comet 案例中，注入藏在 Reddit 评论里［S13］；Fellou 浏览器"simply asking the browser to go to a website causes the browser to send the website's content to their LLM"［S25］。
  - 【事实】ATLAS AML.T0100 Clickbait 专门针对"Computer-Using AI agents or AI web browsers"［S3］。OWASP ASI01 场景 2 描述了 Operator 通过网页内容"accesses authenticated internal pages"［S4］。
  - 【观点】OpenAI（据 Fortune 2025-12-23 报道转引）认为 Atlas 的 agent mode"expands the security threat surface"，并称提示注入"is unlikely to ever be fully 'solved.'"［S33］Anthropic 称其浏览器扩展的攻击成功率降到了 1%，并认为这仍是"meaningful risk"（原文摘要）。［S26］
- **编程 Agent**：主要入口是代码文件、依赖、issue/PR（含隐藏注释）、规则/配置文件、MCP 工具、图片。
  - 【事实】GitHub MCP 的恶意 issue 案例［S6］、CamoLeak［S20］、Rules File Backdoor［S27］、Copilot 通过改写 settings.json 开启自动批准［S19］、Gemini CLI 读入缩放图片后经 Zapier MCP 外泄［S24］。
  - 【事实】Trail of Bits 指出，该利用依赖"Zapier MCP server's default setting that auto-approves tool calls"（摘要转述）。［S24］
- **办公助手（邮件、日历、文档）**：主要入口是外部来信、日历邀请、共享文档、记忆。这类入口的特点是攻击者可以主动投递，部分场景用户无需任何操作（零点击）。
  - 【事实】EchoLeak［S16］、SafeBreach 的 Gemini 日历攻击［S12］、Gemini 记忆投毒［S18］、OWASP ASI01 场景 3（恶意日历邀请注入每天重复的"quiet mode"指令）［S4］。
- **客服 / 企业流程 Agent（CRM、ITSM、工单、内容审核）**：主要入口是外部用户可写的表单、工单、记录字段，以及多 Agent 协作。
  - 【事实】ForcedLeak 经 Web-to-Lead 表单注入［S21］；Cato 的工单在内部用户权限下执行，"executed with internal privileges"［S22］；AppOmni 指出 Agent 以发起交互用户的权限运行，并且"all while the ServiceNow prompt injection protection feature was enabled"攻击依然成功［S23］；Unit 42 的野外案例针对 AI 广告审核 Agent［S14］。
- 【观点】Simon Willison 认为，判断风险的关键不在 Agent 类型，而在于是否同时具备"lethal trifecta"：私有数据访问、"Exposure to untrusted content"和外部通信能力。［S29］

### 冲突与不确定
- 公开的按 Agent 类型统计的攻击面数据很少。上面的归类来自案例归纳，未找到权威的定量对比来源。
- 各厂商公布的成功率（如 Anthropic 的 1%）基于各自的内部测试集，不同厂商之间不能直接比较。

## 本视角小结（3–5 条）
1. 不可信内容的入口几乎覆盖 Agent 读取的一切：网页、邮件/日历、文档、issue/PR、工具返回值、业务表单字段、MCP 工具描述、RAG、记忆、其他 Agent 的输出、图片。OWASP ASI01 与 ATLAS 都把原因归结为模型"cannot reliably distinguish instructions from related content"［S4］，因此入口无法靠逐一封堵来消除。
2. 手法分两层：一是隐藏，即让人看不到而模型读得到（CSS 隐藏、注释、Unicode tag/零宽字符、图片缩放）；二是出口，即借合法渲染或合法工具外传数据（Markdown 图片/链接、白名单域名、代理、写操作工具）。2025–2026 年的案例多数是在出口这一层被修复的，例如 GitHub 禁用图片渲染。
3. 供应链式入口（MCP 工具描述投毒、rug pull、恶意 MCP 包）和持久化（记忆/RAG/线程投毒）让一次注入能跨会话、跨用户生效。ATLAS 在 2025 年新增了 Context Poisoning（T0080）、Tool Poisoning（T0110）等 Persistence 技术。
4. 权威分类框架已经基本成型：OWASP LLM01:2025（单次响应）、OWASP Agentic Top 10 2026（ASI01/02/04/06/07/08 覆盖劫持、工具、供应链、记忆、Agent 间通信、级联）、MITRE ATLAS（按战术）。但同一攻击（如工具投毒）在不同框架里归属不同。
5. 野外利用已从概念验证走向实际出现，但目前整体还不复杂：Unit 42 报告了首个真实恶意 IDPI，Google 测得恶意类别相对增长 32%，同时评价为"limited sophistication"。

## 信源
- [S1] Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection｜Greshake, Abdelnabi, Mishra, Endres, Holz, Fritz（arXiv 2302.12173 / AISec'23）｜2023-02-23（v2 2023-05-05）｜A｜https://arxiv.org/abs/2302.12173
  摘录："Passive methods (by retrieval)" / "Active methods (e.g., emails)" / "User-driven injections" / "Hidden injections"；"any prompts/instructions written on a page (while being invisible to the user) can be effectively injected and affect the model"；"data theft, worming, information ecosystem contamination"
- [S2] LLM01:2025 Prompt Injection｜OWASP GenAI Security Project｜2024-11（2025 版）｜A｜https://genai.owasp.org/llmrisk/llm01-prompt-injection/
  摘录："Indirect prompt injections occur when an LLM accepts input from external sources, such as websites or files."；"These inputs can affect the model even if they are imperceptible to humans"；"Providing unauthorized access to functions available to the LLM"
- [S3] MITRE ATLAS 数据（ATLAS.yaml v5.6.0，GitHub mitre-atlas/atlas-data，文件头标注已 deprecated）｜MITRE｜各技术条目修改日期 2023-10 至 2025-11｜A｜https://github.com/mitre-atlas/atlas-data （raw: https://raw.githubusercontent.com/mitre-atlas/atlas-data/main/dist/ATLAS.yaml）
  摘录：AML.T0051.001 "An adversary may inject prompts indirectly via separate data channel ingested by the LLM such as include text or multimedia pulled from databases or websites."；AML.T0068 "small text, text colored the same as the background, or hidden HTML elements"；AML.T0080.000 "an adversary can inject memories via Direct or Indirect Prompt Injection"；AML.T0061 "This allows the prompt to propagate to other LLMs and persist on the system."
- [S4] OWASP Top 10 for Agentic Applications for 2026（PDF）｜OWASP GenAI Security Project – Agentic Security Initiative｜2025-12-09｜A｜https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
  摘录："agents and the underlying model cannot reliably distinguish instructions from related content."；"Unlike LLM01:2025, which focuses on altering a single model response, ASI01 captures the broader agentic impact"；"Tool-descriptor injection: An attacker embeds hidden instructions or malicious payloads into a tool's metadata or MCP/agent-card"
- [S5] MCP Security Notification: Tool Poisoning Attacks｜Invariant Labs｜2025-04-01｜B（一手研究博客）｜https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks
  摘录："malicious instructions are embedded within MCP tool descriptions that are invisible to users but visible to AI models"；"a malicious server can change the tool description after the client has already approved it"
- [S6] GitHub MCP Exploited: Accessing private repositories via MCP｜Invariant Labs｜2025-05-26｜B｜https://invariantlabs.ai/blog/mcp-github-vulnerability
  摘录："The vulnerability allows an attacker to hijack a user's agent via a malicious GitHub Issue"；"coerce it into leaking data from private repositories"
- [S7] Hiding and Finding Text with Unicode Tags｜Johann Rehberger (Embrace The Red)｜2024-01-14｜B｜https://embracethered.com/blog/posts/2024/hiding-and-finding-text-with-unicode-tags/
  摘录："The Tags Unicode Block mirrors ASCII"；"because it is often not rendered in the UI, the special text remains unnoticable to users"；"allows smuggling of data in plain sight!"
- [S8] Defending LLM applications against Unicode character smuggling｜AWS Security Blog｜2025-09-30｜A｜https://aws.amazon.com/blogs/security/defending-llm-applications-against-unicode-character-smuggling/
  摘录："a specific range of characters spanning from U+E0000 to U+E007F"；"can read, interpret, and act on these hidden characters placed with Unicode tags"
- [S9] Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems｜Lee & Tiwari（arXiv 2410.07283）｜2024-10-09｜A｜https://arxiv.org/abs/2410.07283
  摘录："a novel attack where malicious prompts self-replicate across interconnected agents"
- [S10] PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of LLMs｜Zou et al.（USENIX Security 2025）｜2024-02-12（v3 2024-08-13）｜A｜https://arxiv.org/abs/2402.07867
  摘录："PoisonedRAG could achieve a 90% attack success rate when injecting five malicious texts"
- [S11] Memory Injection Attacks on LLM Agents via Query-Only Interaction（MINJA）｜arXiv 2503.03704｜2025-03-05（v5 2026-02-12）｜A｜https://arxiv.org/abs/2503.03704
  摘录："The attacker injects malicious records into the memory bank by only interacting with the agent via queries"
- [S12] Invitation Is All You Need: Hacking Gemini｜SafeBreach Labs（Nassi, Cohen, Yair）｜2025-08-06｜B｜https://www.safebreach.com/blog/invitation-is-all-you-need-hacking-gemini/
  摘录："simply by sending them a Google calendar invite"；"Remotely control a victim's home appliances (e.g., connected windows, boiler, lights)"；"Exfiltrate a victim's emails"
- [S13] Agentic Browser Security: Indirect Prompt Injection in Perplexity Comet｜Brave｜2025-08-20｜B｜https://brave.com/blog/comet-prompt-injection/
  摘录："the prompt injection instructions hidden behind the spoiler tag"；"Exfiltrate both the email address and the OTP by replying to the original Reddit comment."
- [S14] Fooling AI Agents: Web-Based Indirect Prompt Injection Observed in the Wild｜Palo Alto Networks Unit 42｜2026-03-03｜A（一手遥测数据）｜https://unit42.paloaltonetworks.com/ai-agent-prompt-injection/
  摘录："Our research identified 22 distinct techniques attackers used in the wild to put together payloads"；"Setting font-size: 0px and line-height: 0 to shrink text until it physically disappears"；"To our knowledge, this is the first reported detection of a real-world example of malicious IDPI"
- [S15] AI threats in the wild: The current state of prompt injections on the web｜Google（Brunner, Liu, Pande）｜2026-04-23｜A｜https://blog.google/security/prompt-injections-web/
  摘录："We saw a relative increase of 32% in the malicious category between November 2025 and February 2026."；"While the observed activity suggests limited sophistication, this might be only part of the bigger picture."
- [S16] EchoLeak: The First Real-World Zero-Click Prompt Injection Exploit in a Production LLM System｜arXiv 2509.10540（AAAI Fall Symposium 2025）｜2025-09-06｜A｜https://arxiv.org/abs/2509.10540
  摘录："a zero-click prompt injection vulnerability in Microsoft 365 Copilot"（Aim Security 原博客返回 403，未能抓取）
- [S17] Spyware Injection Into Your ChatGPT's Long-Term Memory (SpAIware)｜Johann Rehberger｜2024-09-20｜B｜https://embracethered.com/blog/posts/2024/chatgpt-macos-app-persistent-data-exfiltration/
  摘录："Through prompt injection from untrusted data, attackers could insert long-term persistent spyware into ChatGPT's memory."；"continuous data exfiltration of any information the user typed"
- [S18] Hacking Gemini's Memory with Prompt Injection and Delayed Tool Invocation｜Johann Rehberger｜2025-02-10｜B｜https://embracethered.com/blog/posts/2025/gemini-memory-persistence-prompt-injection/
  摘录："Delayed Tool Invocation just means that the attacker "pollutes" the chat context with instructions and a trigger action"；"Gemini is tricked, and it saves the attacker's chosen information to long-term memory"
- [S19] GitHub Copilot: Remote Code Execution via Prompt Injection (CVE-2025-53773)｜Johann Rehberger｜2025-08-12｜B｜https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/
  摘录："a prompt injection planted in a source code file, web page, GitHub issue"；"\"chat.tools.autoApprove\": true"
- [S20] CamoLeak: Critical GitHub Copilot Vulnerability Leaks Private Source Code｜Legit Security（Omer Mayraz）｜2025-10-08（更新 2026-02-12）｜B｜https://www.legitsecurity.com/blog/camoleak-critical-github-copilot-vulnerability-leaks-private-source-code
  摘录："I tried the same prompt but this time as a hidden comment inside the PR description."；"GitHub fixed it by disabling image rendering in Copilot Chat completely."
- [S21] ForcedLeak: AI Agent Risks Exposed in Salesforce Agentforce｜Noma Security｜2025-09-25｜B｜https://noma.security/blog/forcedleak-agent-risks-exposed-in-salesforce-agentforce/
  摘录："The attacker places malicious content in a web form, which gets stored in the system's database."；"The domain my-salesforce-cms.com was whitelisted but had expired and become available for purchase"
- [S22] Cato CTRL PoC attack targeting Atlassian's MCP（经 Simon Willison 转引四步链路；Cato 原文抓取为空）｜Cato Networks / simonwillison.net｜2025-06-19｜B｜https://simonwillison.net/2025/Jun/19/atlassian-prompt-injection-mcp/ （原文 https://www.catonetworks.com/blog/cato-ctrl-poc-attack-targeting-atlassians-mcp/）
  摘录："A threat actor (acting as an external user) submits a malicious support ticket."；"A prompt injection payload in the malicious support ticket is executed with internal privileges."
- [S23] AI Agent-to-Agent Discovery Prompt Injection (ServiceNow Now Assist)｜AppOmni AO Labs（Aaron Costello）｜2025-11-19｜B｜https://appomni.com/ao-labs/ai-agent-to-agent-discovery-prompt-injection/
  摘录："Through second-order prompt injection, an attacker can redirect a benign task assigned to an innocuous agent"；"all while the ServiceNow prompt injection protection feature was enabled"
- [S24] Weaponizing image scaling against production AI systems｜Trail of Bits｜2025-08-21｜B｜https://blog.trailofbits.com/2025/08/21/weaponizing-image-scaling-against-production-ai-systems/
  摘录："when scaled, these images can reveal prompt injections that are not visible at full resolution"；"exfiltrates user data stored in Google Calendar"
- [S25] Unseeable prompt injections in screenshots: more vulnerabilities in Comet and other AI browsers｜Brave｜2025-10-21（更新 2025-10-31）｜B｜https://brave.com/blog/unseeable-prompt-injections/
  摘录："Malicious instructions embedded as nearly-invisible text within the image"；"simply asking the browser to go to a website causes the browser to send the website's content to their LLM"
- [S26] Mitigating the risk of prompt injections in browser use｜Anthropic｜2025-11-24｜A｜https://www.anthropic.com/research/prompt-injection-defenses
  摘录："every webpage an agent visits is a potential vector for attack"；"every webpage, embedded document, advertisement, and dynamically loaded script"
- [S27] New Vulnerability in GitHub Copilot and Cursor: How Hackers Can Weaponize Code Agents (Rules File Backdoor)｜Pillar Security｜2025-03-18｜B｜https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents
  摘录："invisible Unicode characters such as zero-width joiners and bidirectional text markers"
- [S28] How Microsoft defends against indirect prompt injection attacks｜Microsoft MSRC｜2025-07-29｜A｜https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks
  摘录："cause the LLM output an HTML image tag or equivalent in markdown where the source URL is the attacker's server."；"the prompt injection could cause the LLM to output a clickable link to the attacker's server"
- [S29] The lethal trifecta for AI agents: private data, untrusted content, and external communication｜Simon Willison｜2025-06-16｜B｜https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
  摘录："Exposure to untrusted content"；"If a tool can make an HTTP request—to an API, or to load an image, or even providing a link for a user to click"
- [S30] Model Context Protocol has prompt injection security problems｜Simon Willison｜2025-04-09｜B｜https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/
  摘录："MCP tools can mutate their own definitions after installation."；"With multiple servers connected to the same agent, a malicious one can override or intercept calls made to a trusted one."
- [S31] MCP Specification 2025-06-18 – Server/Tools｜Model Context Protocol｜2025-06-18｜A｜https://modelcontextprotocol.io/specification/2025-06-18/server/tools
  摘录："clients MUST consider tool annotations to be untrusted unless they come from trusted servers."；"When the list of available tools changes, servers that declared the listChanged capability SHOULD send a notification"
- [S32] Here Comes The AI Worm: Unleashing Zero-click Worms that Target GenAI-Powered Applications（Morris II）｜Cohen, Bitton, Nassi（arXiv 2403.02817）｜2024-03-05（v2 2025-01-30）｜A｜https://arxiv.org/abs/2403.02817
  摘录："an attacker can initiate a computer worm-like chain reaction that we call Morris-II"
- [S33] OpenAI says prompt injections may never be fully solved（报道转引 OpenAI 官方博客 "Continuously hardening ChatGPT Atlas against prompt injection"，原文抓取 403）｜Fortune（Beatrice Nolan）｜2025-12-23｜B｜https://fortune.com/2025/12/23/openai-ai-browser-prompt-injections-cybersecurity-hackers/
  摘录：OpenAI 称提示注入"much like scams and social engineering on the web, is unlikely to ever be fully 'solved.'"；"agent mode" in ChatGPT Atlas "expands the security threat surface."
