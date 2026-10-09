# 关键论断清单（待核查）
> 汇总自 5 个视角的笔记，共 36 条，都是学习报告会直接使用的核心结论、数据和引文。信源编号见 sources.md。

## A. 原理
- C1 英国 NCSC（2025-12-08）指出 SQL 注入可以用参数化查询彻底缓解，而 LLM 内部 "there is only ever 'next token'"，并判断提示词注入 "may never be totally mitigated in the way that SQL injection attacks can be"。［G2］
- C2 Zverev 等（arXiv 2403.06833）的结论是 "none of the existing models provide a dedicated mechanism to distinguish between instructions and data"；GPT-4 的分离分数约为 20.8%。［G3］
- C3 Simon Willison 于 2025-06-16 提出 "lethal trifecta"：私有数据访问、暴露于不可信内容、对外通信能力，三者同时具备时攻击者可以轻易窃取数据。［G6］
- C4 Meta 于 2025-10-31 发布 "Agents Rule of Two"：一个会话最多同时满足 [A] 处理不可信输入、[B] 访问敏感系统或私有数据、[C] 改变状态或对外通信 中的两项；并称 "Prompt injection is a fundamental, unsolved weakness in all LLMs."［G7］
- C5 Willison（2025-11-02）指出 trifecta "only covers the risk of data exfiltration"，并认为即使去掉敏感数据，"不可信输入 + 可改变状态" 仍然危险。［G8］
- C6 Google DeepMind（arXiv 2505.14534）称对抗训练 "clearly not sufficient as a defense in isolation"，且 "More capable models aren't necessarily more secure"。［G12］
- C7 Spotlighting 论文（arXiv 2403.14720）报告，在 GPT 系列模型的实验中，攻击成功率 "from greater than 50% to below 2%"。［G10］
- C8 OpenAI IH-Challenge（2026-03，arXiv 2603.10521）报告：GPT-5-Mini 的 IH 鲁棒性平均提升 +10.0%（84.1% → 94.1%），不安全行为从 6.6% 降到 0.7%。［G11］
- C9 Anthropic（2025-11-24）报告：Claude Opus 4.5 在浏览器场景、面对 100 次尝试的自适应攻击者时，攻击成功率约 1%，并写明 "No browser agent is immune to prompt injection"。［G13］
- C10 （二手）据 The Decoder 转述 Anthropic Opus 5 system card：浏览器场景下，开启两层系统防护时攻击成功率为 0%，不开启时为 3.7%。［G14］

## B. 自适应攻击与评估
- C11 "The Attacker Moves Second"（arXiv 2510.09023，2025-10）绕过了 12 种防御，大多数攻击成功率 >90%，而这些防御的原报告大多接近 0；人类红队 "succeeds in all the cases we evaluated"。作者来自 OpenAI、Anthropic、Google DeepMind 等机构。［G18］
- C12 同一论文测得：Spotlighting 和 Prompt Sandwiching 在静态攻击下最低约 1%，在自适应攻击下 >95%；MetaSecAlign 原报告 2%，复测为 96%；Protect AI、PromptGuard、Model Armor 三种检测器 >90%，PIGuard 为 71%。［G18］
- C13 Zhan 等（arXiv 2503.00061，NAACL 2025 Findings）评估了 8 种防御，全部被自适应攻击绕过，攻击成功率持续高于 50%。［G19］
- C14 NIST CAISI 的 agent hijacking 评估：重复尝试 25 次后，平均攻击成功率从 57% 升到 80%；自适应攻击可把成功率从 11% 提到 81%。［G91］
- C15 NIST CAISI（2026-03-23）的大规模红队竞赛中，所有前沿目标模型都被至少一次成功攻破。［G92］
- C16 WASP（Meta，arXiv 2504.18575）报告攻击 "partially succeed in up to 86% of the case"，但 Agent 往往无法完整达成攻击者目标，作者称之为 "security by incompetence"。［G83］
- C17 arXiv 2510.05244 用简单的 "Tool-Input Firewall + Tool-Output Sanitizer" 在四个基准上做到 "perfect security with high utility"，并指出这些基准存在 "flawed success metrics, implementation bugs, ... weak attacks"。［G85］

## C. 攻击面与野外利用
- C18 Unit 42（2026-03-03）称在野外观察到 22 种构造载荷的技巧，并称 "this is the first reported detection of a real-world example of malicious IDPI"。［G34］
- C19 Google（2026-04-23）扫描 CommonCrawl 后称，恶意类别在 2025-11 到 2026-02 间相对增长 32%，同时认为 "the observed activity suggests limited sophistication"。［G35］
- C20 Invariant Labs（2025-04-01）定义了 MCP 工具投毒，并指出恶意服务器 "can change the tool description after the client has already approved it"（rug pull）。［G25］
- C21 PoisonedRAG（USENIX Security 2025）报告，注入 5 条恶意文本即可达到 90% 的攻击成功率。［G30］
- C22 OWASP Top 10 for Agentic Applications 2026 于 2025-12 发布，把间接注入归入 ASI01 Agent Goal Hijack，并写道 "agents and the underlying model cannot reliably distinguish instructions from related content"。［G24］

## D. 真实案例
- C23 EchoLeak（CVE-2025-32711，M365 Copilot）：CVSS 9.3，零点击；通过伪装成写给人看的邮件绕过 XPIA 分类器，利用引用式 Markdown 链接和图片，借助 CSP 允许的 Teams 域名外泄数据；微软于 2025-05 在服务端修复，2025-06-11 公开。［G51］［G36］［G53］
- C24 Invariant Labs（2025-05-26）演示：通过公共仓库中的恶意 issue 劫持接入 GitHub MCP 的 Agent，把私有仓库数据写进公共 PR；并称 "this is not a flaw in the GitHub MCP server code itself"。［G26］
- C25 GitHub 于 2025-12-10 为 MCP Server 引入 Lockdown mode，只展示有 push 权限的可信协作者的内容。［G55］
- C26 CVE-2026-48529（2026-06-26）：GitHub MCP Server 的 Lockdown mode 在 HTTP 模式下存在跨用户 GraphQL 客户端混淆，1.1.2 版本修复。［G56］
- C27 Brave（2025-08-20）披露 Perplexity Comet 的注入：藏在 Reddit 评论中的指令让 Agent 读取用户邮箱和 OTP 并外传；Perplexity 的初次修复被复测发现不完整。［G33］
- C28 Miggo（2026-01-19）在 Google 部署多层防御之后，仍用日历邀请中的自然语言指令让 Gemini 通过 Calendar.create 外泄私密会议信息。［G60］
- C29 CVE-2025-53773（2025-08-12）：注入让 GitHub Copilot Agent Mode 向 .vscode/settings.json 写入 "chat.tools.autoApprove": true，从而关闭确认并执行命令；微软在 2025 年 8 月的 Patch Tuesday 修复。［G52］［G39］
- C30 General Analysis（2025-07）演示：客服工单中的注入让 Cursor 通过 Supabase MCP 以 service_role 读取 integration_tokens 表，并把结果写回工单。［G64］

## E. 防御
- C31 CaMeL（arXiv 2503.18813）在 AgentDojo 上以 "provable security" 完成 77% 的任务，无防御系统为 84%；Token 用量约为原生工具调用的 2.82 倍（输入）和 2.73 倍（输出）。［G15］
- C32 FIDES（Microsoft，arXiv 2505.23643）："With policy checks enabled, Fides stops all prompt injection attacks in AgentDojo."［G73］
- C33 AgentDojo（GPT-4o）中，Tool filter 把目标攻击成功率从 57.69% 降到 6.84%；该防御在 17% 的测试用例中失效，因为完成任务所需的工具本身就足以执行攻击。［G69］
- C34 "Can CaMeLs Talk?"（arXiv 2610.05640，2026-10）发现 "CaMeL's guarantees do not compose"，即在多 Agent 系统中 CaMeL 的保证不再成立。［G75］
- C35 Anthropic 报告：Claude Code 用户批准了 93% 的权限提示；沙箱在内部使用中把权限提示减少了 84%。［G94］［G79］
- C36 Rehberger 演示：Claude 代码解释器的默认网络白名单包含 api.anthropic.com，注入可以让模型用攻击者的 API key 把文件上传到攻击者账户。［G80］
