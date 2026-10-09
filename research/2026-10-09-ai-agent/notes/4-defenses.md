# 视角 4：防御手段逐个评估

> 研究日期：2026-10-09。本笔记涉及的数字都标了出处和测试条件。不同论文的基准、模型、攻击强度不同，**数字不能横向直接比较**。
> 标注说明：【事实】指来源中可核对的测量结果或客观陈述；【观点】指作者或机构的判断与主张；【推断】是本研究员根据多个来源做的归纳，不是任何来源的原话。

---

## 子问题 1：检测与过滤类（输入分类器、护栏模型、厂商内置分类器）

### 发现

**静态评测下的表现（防御方自报）**
- 【事实】Meta 在 LlamaFirewall 论文中报告：在 AgentDojo 上（阈值调到效用下降 3% 以内），无防御基线 ASR 为 17.6%、效用 47.7%；只加 PromptGuard 2 86M 时 ASR 降到 7.5%（降幅 57%），效用 47.0%；只加 AlignmentCheck（用 Llama 4 Maverick 审查推理链）时 ASR 降到 2.89%，但效用降到 43.1%，时延明显增加；两者组合时 ASR 为 1.75%，效用 42.7%。［S2］
- 【事实】同一篇论文自己说明，AgentDojo 评测集"focuses primarily on a narrow class of attacks"。［S2］
- 【事实】AgentDojo 原论文（GPT-4o）测过一个 BERT 类 PI 检测器：目标 ASR 从 57.69% 降到 7.95%，但良性效用从 69.0% 降到 41.49%。作者的结论是"The prompt injection detector has too many false positives, however, and significantly degrades utility."［S9］
- 【事实】InjecGuard 论文发现，现有 prompt guard 模型存在 over-defense，也就是因为 trigger word 偏差而误报良性输入。在 NotInject 数据集上，这类模型的准确率接近"random guessing levels (60%)"。［S3］

**自适应攻击下的表现**
- 【事实】"The Attacker Moves Second"（Google DeepMind、OpenAI、ETH 等 14 位作者，2025-10）在 AgentDojo 上测了 Protect AI、PromptGuard、PIGuard、Model Armor 四种检测器。攻击者能拿到检测器的置信度和判定结果作为反馈时，搜索式自适应攻击对 Protect AI、PromptGuard、Model Armor 的 ASR 都 >90%（Model Armor 配 Gemini-2.5 Pro）。PIGuard 相对更难，但 ASR 仍达 71%。人类红队在最严格设置下也收集到 123 个成功注入。［S1］
- 【事实】该论文还指出，很多成功的触发文本"are not obviously harmful or show clear intention to overwrite the user instruction"，检测器要识别它们，就会显著抬高良性数据上的误报率。［S1］
- 【事实】基于"秘密知识/金丝雀"的检测同样失效。DataSentinel 被 RL 攻击绕过，恶意任务的准确率 >80%（与无防御模型相当），"In every case, the defense was bypassed"。MELON 也在该论文的评测范围内。［S1］
- 【事实】2024 年 7 月，Robust Intelligence 发现 Prompt-Guard-86M 只要在字符间加空格、去掉标点就能绕过：450 条有害注入的识别准确率从 100% 降到 0.2%，"(Success Rate of 99.8%)"。Cisco 的报道称 Meta 已修复。这条来源已超过 12 个月，只用来说明机制。［S4］
- 【事实】2025-11 的一项研究测了 10 个公开护栏模型（Meta、Google、IBM、NVIDIA 等），用 1,445 条提示。结果是所有模型在未见过的新攻击上都明显退化，例如 Qwen3Guard 从 91.0% 跌到 33.8%。作者认为"benchmark performance may be misleading due to training data contamination"。注意：这项研究主要针对有害内容护栏，不专门针对 IPI。［S32］
- 【事实】真实事故：EchoLeak（CVE-2025-32711，M365 Copilot）通过把指令写成"像是写给人看的"普通邮件文本，绕过了微软的 XPIA 分类器。［S22］

**厂商的做法：把分类器作为分层防御的一层**
- 【事实】Anthropic（2025-11-24）表示会对进入上下文的所有不可信内容做分类器扫描。同时公布：在内部自适应 Best-of-N 攻击者（每个环境 100 次尝试）下，Claude Opus 4.5 加上浏览器扩展防护后 ASR 约 1%，并写明"A 1% attack success rate—while a significant improvement—still represents meaningful risk."这个数字是模型训练、分类器和产品层干预的综合结果，没有单独给出分类器的贡献。［S5］
- 【事实】Google（2025-06-13）在 Gemini 中部署了 prompt injection content classifiers，作为五层防御之一。［S7］
- 【事实】Microsoft（2025-07-29）把 Prompt Shields 归为检测层，并说明此类概率性防御"may not prevent or detect every instance of the attack"。［S6］
- 【事实】LLMail-Inject（微软/ETH 等，SaTML 2025 竞赛，839 人，208,095 条攻击）中，各检测类防御被攻破的难度依次为：LLM Judge 最难，TaskTracker 次之，Prompt Shield 的团队成功率最高。叠加全部防御后效果显著提升，第二阶段用 GPT-4o 叠加全部防御时没有出现成功攻击。注意：攻击目标被限定为触发一次特定的 send_email 调用，攻击者看不到模型原始输出。［S10］

- 【观点】Simon Willison 认为，护栏产品宣称的"95% of attacks"在应用安全里是"very much a failing grade"［S13］；"99% is a failing grade"［S12］。
- 【观点】Nasr、Carlini 等人认为，只在静态攻击集上评估的防御"should not be regarded as robust"。［S1］

### 冲突与不确定
- **静态评测数字和自适应评测数字差距很大。**LlamaFirewall 报告 PromptGuard 2 在 AgentDojo 静态集上让 ASR 下降 57%［S2］；"Attacker Moves Second"在同一基准上用自适应攻击打到 >90%［S1］。两者不矛盾，测的是不同威胁模型：前者是固定攻击，后者是能拿到检测器反馈的自适应攻击者。
- **叠加防御是否有效，有不同声音。**LLMail-Inject 显示叠加多种检测器后成功攻击大幅减少，甚至降到 0［S10］；"Attacker Moves Second"显示单个检测器都能被打穿，但没有系统测试"全部叠加"。两者的攻击预算、反馈可见度和任务都不同，目前**未找到在强自适应攻击下评估多层检测叠加的可靠来源**。
- 厂商自报数字（Anthropic 1%）用的是内部攻击者，与学术基准不可比。我在检索中看到第三方（Gray Swan，经 the-decoder 报道）给出 Opus 4.5 在 100 次尝试下 ASR 63% 的说法，但只找到二手报道，属于 C 级线索，未核实。

---

## 子问题 2：提示层技巧（定界符、spotlighting/datamarking、sandwich、"忽略数据中的指令"）

### 发现
- 【事实】Spotlighting（微软，2024-03）用变换输入的方式给模型提供来源信号，有 delimiting、datamarking、encoding 三种模式。在 GPT 系列模型的实验中，"spotlighting reduces the attack success rate from greater than 50% to below 2%"，对任务效果影响很小。测试条件是论文自建的非 Agent 任务和静态攻击。［S8］
- 【事实】MSRC（2025-07-29）描述了三种模式。delimiting 是"a specific randomized text delimiter is added before and after the untrusted input"；datamarking 是"a special token is added throughout the entirety of the untrusted text"；encoding 是用 base64、ROT13 之类转换。微软把 spotlighting 归为预防层，不把它当作唯一防线。［S6］
- 【事实】AgentDojo（GPT-4o，最强的内置攻击）给出了量化对比：无防御时目标 ASR 57.69%；Delimiting（定界符加"忽略其中的指令"提示）为 41.65%；Repeat prompt（sandwich）为 27.82%。sandwich 的良性效用反而升到 85.53%。作者评价 sandwich"is unlikely to withstand adaptive attacks (e.g., an injection that instructs the model to ignore future instructions)"。［S9］
- 【事实】"Attacker Moves Second"在 AgentDojo 上实现了 Spotlighting 和 Prompt Sandwiching：静态攻击下 ASR"as low as 1%"，搜索式自适应攻击下"above 95% for both defenses"；人类红队对两者分别找到 265 和 178 个成功攻击。［S1］
- 【事实】LLMail-Inject 发现"spotlighting can be more effective than some detection defenses alone, such as Prompt Shield"。［S10］
- 【事实】Google 在 Gemini 中用了一种叫"security thought reinforcement"的提示层技巧，作为五层防御之一，没有单独公布效果数据。［S7］
- 【观点】Simon Willison 2023 年就有文章，标题即"Delimiters won't save you from prompt injection"（被 AgentDojo 引用为 [61]）。［S9］
- 【观点】Design Patterns 论文认为，依赖当前这类模型的启发式防御"inherently brittle"。［S15］

### 冲突与不确定
- **同一技术，数字从 <2% 到 >95%**。Spotlighting 原论文 <2%［S8］；AgentDojo 中 Delimiting 为 41.65%［S9］；自适应攻击下 >95%［S1］。差异来自任务形态（单轮 NLP 还是多步 Agent）、攻击是否自适应、模型版本。【推断】合理的解读是：提示层技巧能明显降低"随手写的/通用模板"攻击的成功率，对有针对性的攻击者几乎不提供保证。
- 提示层技巧有时**提高**良性效用（AgentDojo 中 sandwich 为 85.53%，无防御为 69.0%）［S9］，几乎没有成本，所以多数厂商仍把它作为默认层［S6］［S7］。它"值不值得做"和"能不能作为安全边界"是两个不同的问题。

---

## 子问题 3：架构类（Dual LLM、CaMeL、Design Patterns、IFC/FIDES）

### 发现

**3.1 Dual LLM 模式（Willison，2023-04）**
- 【事实】原理：Privileged LLM 只接受可信输入并可以调用工具；Quarantined LLM 处理不可信内容但没有工具权限；由一个 Controller 用变量名（如 $VAR1）传递结果。原文写道"The Privileged LLM only ever sees those variable names"。［S11］
- 【观点】作者本人的评价是"This solution is pretty bad"：实现复杂、体验降级；"The social engineering aspects also mean that this isn't a 100% reliable solution"；链式调用中 Q-LLM 的输出仍可能携带注入。［S11］
- 【事实】CaMeL 论文指出 Dual LLM 存在一个缺陷：P-LLM 把"从会议纪要中提取 Bob 的邮箱"之类的工作委托给 Q-LLM，而 Q-LLM 仍暴露在恶意指令下，攻击者可以篡改**数据值**（例如收件人）。Willison 在 2025-04 的博文中复述并认可了这一点。［S12］［S14］

**3.2 CaMeL（Google/Google DeepMind/ETH，2025-03，v2 2025-06）**
- 【事实】原理：P-LLM 根据可信的用户查询生成受限 Python 代码，由此显式抽取控制流和数据流，"the untrusted data retrieved by the LLM can never impact the program flow"；再给数据打 capability 标签，在工具调用时执行安全策略，防止私有数据经未授权数据流外泄。［S14］
- 【事实】效果：在 AgentDojo 上"solving 77% of tasks with provable security (compared to 84% with an undefended system)"。即使不安装任何安全策略，单靠隔离也能把 Gemini 2.5 Pro 的成功攻击数从 300 降到 0（总共 949 次攻击）。剩余的非零 ASR 来自两个注入任务（banking、travel），作者认为它们"not due to a prompt injection"。［S14］
- 【事实】代价有四项。(1) Token：输入约 2.82 倍、输出约 2.73 倍（Claude 3.5 Sonnet，受攻击条件下的中位任务）。(2) 效用：Travel 套件下降明显，例如 Gemini 2.5 Pro 整体从 73.2% 降到 41.2%。但新模型的影响小得多，例如 o3 High 从 84.5% 降到 77.3%；Claude Sonnet 系列在 Travel 上的效用从 25%（3.5）升到 55%（3.7）再到 75%（4），CaMeL 本身没有改动。(3) 策略编写和维护："CaMeL suffers from users needing to codify and specify security policies and maintain them"。(4) 用户疲劳：在解密级（de-classification）环节需要用户介入。［S14］
- 【事实】已知局限：作者自己承认存在侧信道（经间接依赖泄露、异常触发泄露 1 bit、时序侧信道），以及类似 ROP 的风险（用策略允许的小块控制流拼出恶意流程）。原文："No, prompt injection attacks are not fully solved."作者还给出一个"data flow becomes control flow"的案例：用户自己要求"执行邮件里的动作"时，隔离无效。［S14］
- 【事实】组合性问题（2026-10）："Can CaMeLs Talk?"发现"CaMeL's guarantees do not compose"：在分层多 Agent 系统中，下游 Agent 会把上游的不可信数据当作可信输入。在 MultiAgentDojo 上，无 CaMeL 的 ASR 为 12.9%，单 Agent CaMeL 为 0.2%，作者提出的 multi-CaMeL 为 0.0%，并带来一定效用代价。［S18］
- 【事实】向 Computer Use 扩展（2026-01）：在 OSWorld 上采用"单次规划 + 分支计划"，保留了前沿模型最高 57% 的性能。但存在"Branch Steering"攻击：欺骗感知模型，让执行走上攻击者偏好的预置分支（如跳转到恶意网站）。［S19］

**3.3 Design Patterns 论文（Invariant Labs、IBM、EPFL、ETH、Google、Microsoft 等，2025-06）**
- 【事实】核心原则原文："once an LLM agent has ingested untrusted input, it must be constrained so that it is impossible for that input to trigger any consequential actions"。［S15］
- 【事实】六种模式及其边界（据原文整理）：
  - **Action-Selector**：不把工具输出反馈给 Agent，等于"LLM-modulated switch"。对注入免疫，但只能做预定义的动作。
  - **Plan-then-Execute**：先定计划，工具输出不能改变要调用哪些工具；但"a prompt injection can still manipulate the inputs to these tool calls"。
  - **LLM Map-Reduce**：每份不可信文档由隔离的子 Agent 单独处理，一份恶意文档影响不到其他文档。
  - **Dual LLM**：见 3.1。
  - **Code-Then-Execute**：即 CaMeL 的路线，用程序代替计划。
  - **Context-Minimization**：从上下文中删去不必要的内容（主要针对用户提示中的注入）。［S15］
- 【观点】作者认为，基于当前这类语言模型，"it is unlikely that general-purpose agents can provide meaningful and reliable safety guarantees"，因此主张通过**有意限制 Agent 的通用性**来换取安全。［S15］

**3.4 信息流控制 / 污点追踪（FIDES 等）**
- 【事实】FIDES（Microsoft Research，2025-05，v2 2025-09）给数据打上机密性和完整性标签，并沿计划传播，在工具调用处按策略检查；还提供选择性引入变量和"受约束检查"（query_llm 返回受限类型）两种原语。结果："With policy checks enabled, Fides stops all prompt injection attacks in AgentDojo. Without policy checks, all planners, including Fides, succumb to practical PIAs."在 OpenAI 推理模型（o1、o3、o4-mini）上，比基础规划器平均多完成约 16% 的任务，经过提示调优后为 24%。［S16］
- 【事实】MSRC 在官方博客中把 FIDES 描述为"an approach for deterministically preventing indirect prompt injection in agentic systems"。［S6］
- 【事实】FLOWSEAL（2026-09）面向隐私泄露，在 LLM 上下文之外的工具层用 IFC 格和受控解密做拦截，把"Collaborative Workspace Lure"攻击的泄露率从 52.2% 降到 0.5%。论文的论点是：如果执行判断由 LLM 在攻击者可控的上下文中做出，"the enforcement mechanism and the attack surface coincide"。［S21］
- 【事实】独立复现（2026-06）：作者指出 CaMeL、FIDES、Progent、RTBAS、FORGE 等"out-of-band defenses""validated only on static benchmarks"。他们对 Progent 做了小规模自适应复现（Qwen2.5-7B，AgentDojo，3 次运行平均）：ASR 从 25.8% 降到 4.2%，手工自适应攻击下为 2.6%，防御守住了。作者明确说这只是"one small-scale data point"，更强的白盒 GCG 攻击还没有测。［S17］
- 【事实】新的攻击类别（2026-07）："Agent Data Injection"不注入指令，而是伪造可信数据，例如资源标识符、数据来源元数据、工具调用格式。作者称它"easily bypasses existing IPI defenses"，并在 Claude in Chrome、Claude Code、Codex、Gemini CLI 等真实产品中找到漏洞。［S20］

### 冲突与不确定
- **"可证明安全"的范围**：CaMeL 和 FIDES 的保证针对"不可信数据改变控制流"和"违反策略的数据流"。它们不覆盖：不改变数据流的文本操纵（如误导性摘要）、钓鱼式社会工程、侧信道、策略本身写错、跨 Agent 组合［S14］［S18］。【推断】所谓"provable"，是相对于策略和威胁模型而言的，不是绝对安全。
- **效用代价在变小，但证据有限**：CaMeL 和 FIDES 都观察到更强的模型让效用损失变小［S14］［S16］［S18］，但只在 AgentDojo（以及少量扩展基准）上验证过。真实复杂工作流（任务依赖运行时数据才能决定下一步）的效用损失**未找到可靠的量化来源**。
- **自适应评测的空白**：架构类防御还缺少与"Attacker Moves Second"同等强度的独立对抗评估。目前只有一个小规模复现，而且结果对防御有利［S17］。

---

## 子问题 4：权限与执行层（最小权限、出口白名单、禁止自动渲染、人工确认、沙箱）

### 发现

**最小权限 / 工具过滤**
- 【事实】AgentDojo 中最简单的"Tool filter"（在看到不可信数据之前，先选出本任务需要的工具）把 GPT-4o 的目标 ASR 从 57.69% 降到 6.84%，良性效用 73.13%。失效条件是：工具列表无法预先规划；完成任务所需的工具本身就足以执行攻击，这在测试用例中占 17%；多任务长会话中注入可以"等待"合适的工具出现。［S9］
- 【事实】EchoLeak 案例论文把最小权限列为通用经验之一（"emphasizing the principle of least privilege, defense-in-depth architectures"）。［S22］
- 【事实】OpenAI 对 Atlas 用户的建议包括：限制登录态访问，给出具体指令而不是"take whatever action is needed"，并写道"Wide latitude makes it easier for hidden or malicious content to influence the agent, even when safeguards are in place"。这是 TechCrunch 转引 OpenAI 博客，原文 403 无法直接获取。［S26］

**网络出口白名单 / 禁止自动渲染外链和图片**
- 【事实】作用环节：切断攻击链最后的**外泄**一环。Willison 的"致命三要素"（私有数据 + 不可信内容 + 对外通信）中，"If a tool can make an HTTP request—to an API, or to load an image, or even providing a link for a user to click—that tool can be used to pass stolen information back to an attacker"。［S13］
- 【事实】Google 的做法："Our markdown sanitizer identifies external image URLs and will not render them"，同时把可疑 URL 替换为"suspicious link removed"。［S7］
- 【事实】微软在收到 markdown 图片注入报告后选择"deterministically block the security impact (i.e., the data exfiltration technique)"，并对"certain untrusted links"做了类似处理。［S6］
- 【事实】**局限一：白名单内的域可被滥用。**EchoLeak 同时绕过 XPIA 分类器和链接脱敏（用 reference-style Markdown），再借助 CSP 允许的 Teams 域代理请求，实现零点击外泄。［S22］Johann Rehberger 演示了 Claude 代码解释器默认的"Package managers only"白名单中包含 api.anthropic.com：注入让模型用**攻击者的** API key 把文件上传到攻击者账号，单次最多 30MB。［S24］
- 【事实】Anthropic 的 Claude Code 沙箱文章指出："effective sandboxing requires both filesystem and network isolation. Without network isolation, a compromised agent could exfiltrate sensitive files like SSH keys; without filesystem isolation, a compromised agent could easily escape the sandbox and gain network access."［S23］

**人工确认（HITL）**
- 【事实】作用环节：在**高风险动作执行前**设闸。Google 有"User confirmation framework"（例如删除日历事件前要求确认）［S7］；微软"rely on the explicit consent of the user to perform a specific action"［S6］；OpenAI 称 Atlas 被训练为在发送消息或付款前请求确认［S26］。
- 【事实】**局限一：疲劳。**CaMeL 作者写道："This can lead to user fatigue, where users become desensitized to security prompts and may inadvertently approve malicious actions"［S14］。Anthropic 承认频繁确认"can lead to 'approval fatigue', where users might not pay close attention to what they're approving"，并用沙箱在内部使用中把权限弹窗减少了 84%［S23］。Design Patterns 论文在 OS 助手案例中评价逐条确认：Utility 上"cumbersome"，Security 上"It would probably be easy for an attack to obfuscate using innocuous looking commands"［S15］。
- 【事实】**局限二：确认框本身可被伪造。**Checkmarx 提出的"Lies-in-the-Loop / HITL Dialog Forging"（已收录于 OWASP 社区页）利用的是这一点："HITL dialogs, which are usually the only feedback users see, are generated based on context that an attacker can control through indirect prompt injection"，在 Claude Code 上做了 PoC。［S25］

**沙箱**
- 【事实】作用环节：限制**爆炸半径**，即注入成功后能碰到哪些文件和网络。Design Patterns 论文把 action sandboxing 列为每个 Agent 都应采用的最佳实践，同时指出它"does not prevent information leakage from the database, for example through the data analysis and output of visualizations"。［S15］
- 【事实】Anthropic 的报告是沙箱同时提升了安全性和自主性（弹窗 -84%）。［S23］

- 【观点】Willison 认为，对于自由组合工具的终端用户，"The only way to stay safe there is to avoid that lethal trifecta combination entirely"。［S13］
- 【观点】Wiz 的 Rami McCarthy（TechCrunch 采访）："A useful way to reason about risk in AI systems is autonomy multiplied by access"。［S26］

### 冲突与不确定
- 关于人工确认的**定量**证据：除了 Anthropic 的"弹窗减少 84%"这一内部数字［S23］，**未找到可靠来源**量化 Agent 场景下用户误批准恶意操作的比例。CaMeL 引用的疲劳证据（Felt et al. 2012 等）来自移动权限领域，不是 Agent 场景。
- 厂商对 HITL 的定位有分歧：Anthropic 被报道认为 LITL 不构成安全漏洞，因为已有用户确认，责任在用户（Dark Reading 和 Security Boulevard 转述，C 级线索）；Checkmarx 和 OWASP 认为确认框可被注入操纵［S25］。

---

## 子问题 5：公开基准（AgentDojo、InjecAgent、WASP 等）及其局限

### 发现
- 【事实】**AgentDojo**（ETH，NeurIPS 2024 D&B）：97 个任务、629 个安全测试用例；是可扩展环境，不是静态套件；在 GPT-4o 上跑完整安全套件约 35 美元。［S9］它已成为 CaMeL、FIDES、MELON、LlamaFirewall、Meta-SecAlign 等工作的事实标准［S14］［S16］［S33］［S2］［S31］。
- 【事实】**InjecAgent**（UIUC，2024-03）：1,054 个用例、17 个用户工具、62 个攻击者工具；ReAct 提示的 GPT-4 被攻击成功 24%，加入 hacking prompt 后约翻倍。［S27］
- 【事实】**WASP**（Meta，2025-04）：端到端 Web Agent 基准。"while attacks partially succeed in up to 86% of the case, even state-of-the-art agents often struggle to fully complete the attacker goals"，作者把这种现象称为"security by incompetence"。［S28］
- 【事实】**Agent Security Bench（ASB）**：10 个场景、400 多个工具、27 种攻防方法；最高平均 ASR 84.30%。［S34］
- 【事实】**ART（Gray Swan 等，2025-07）**：最大规模的公开红队竞赛，覆盖 22 个前沿 Agent、44 个场景，共 180 万次注入，其中超过 6 万次成功。"Nearly all agents exhibit policy violations for most behaviors within 10-100 queries"；鲁棒性与模型规模、能力、推理算力的相关性有限。［S29］
- 【事实】**LLMail-Inject**（SaTML 2025）：公开了 208,095 条自适应攻击；主阶段 370,724 次提交中只有 0.8% 端到端成功。［S10］
- 【事实】**基准本身的局限**：
  - (1) 静态攻击。"Attacker Moves Second"显示，在 AgentDojo 静态攻击下 ASR 约 1% 的防御，在自适应攻击下 >90%。［S1］
  - (2) 易饱和且有缺陷。2510.05244 用一个简单的"Tool-Input Firewall + Tool-Output Sanitizer"在 AgentDojo、ASB、InjecAgent、τ-Bench 四个基准上都做到"perfect security with high utility"，并指出这些基准存在"flawed success metrics, implementation bugs, and most importantly, weak attacks"，于是提出 AgentDojo-Revised。［S30］
  - (3) 能力混淆。WASP 的"security by incompetence"说明，低 ASR 可能只是 Agent 能力不足，并不代表安全。［S28］
  - (4) 威胁模型过窄。架构类防御"validated only on static benchmarks"［S17］；Agent Data Injection 这类"伪造可信数据"的攻击不在现有基准的覆盖范围内［S20］；多 Agent 组合场景需要新建 MultiAgentDojo［S18］。
  - (5) 不可比。"Attacker Moves Second"明确说明，不同防御用不同基准，"the robustness numbers are not necessarily comparable across defenses"。［S1］

### 冲突与不确定
- 关于 AgentDojo 是否还有区分度：2510.05244 认为它"easily saturated by a simple approach"［S30］；CaMeL、FIDES 仍用它展示安全性与效用之间的差异［S14］［S16］。【推断】它适合衡量"效用代价"和"抵御已知攻击"，不适合单独作为鲁棒性证明。
- InjecAgent 与 WASP 的结论之间可能存在落差：InjecAgent 测的是 Agent 是否"被诱导去执行"攻击动作［S27］，WASP 发现部分成功率与完整达成攻击目标之间差距很大［S28］。InjecAgent 的设置细节（单步还是多步、工具输出是否为模拟）本笔记未逐项核实。两类基准之间的差距，**未找到系统量化的来源**。

---

## 防御总表

| 防御类别 | 切断攻击链哪一环 | 能防 | 防不住 | 代价 | 证据强度 |
|---|---|---|---|---|---|
| 输入/输出分类器、护栏模型（PromptGuard、Prompt Shields、Model Armor 等） | 注入**进入**上下文时（入口检测），或在输出侧拦截 | 已知模式、模板化、低成本攻击；静态 AgentDojo 上 ASR 降 57%［S2］；在多层叠加中贡献明显［S10］ | 自适应攻击（>90%，PIGuard 71%）［S1］；字符级扰动［S4］；"看起来像写给人看的"文本［S22］；新分布攻击［S32］ | 误报，部分检测器效用从 69% 降到 41%［S9］，over-defense 接近随机［S3］；时延；需要持续更新 | **强**（多方独立证据一致表明：可降低基线，但不能作为边界） |
| 提示层技巧（定界符、spotlighting、sandwich、"忽略数据中的指令"） | 模型**解读**阶段，降低把数据当指令的概率 | 通用/随手攻击：<2%［S8］；AgentDojo 中 ASR 57.7% 降到 27.8%~41.7%［S9］ | 自适应攻击 >95%［S1］；人类红队有数百个成功案例［S1］ | 几乎为零，有时还提升效用［S9］；不提供任何保证 | **强**（结论一致：便宜、有用、不可依赖） |
| Dual LLM | 不可信数据**不进入**特权 LLM 上下文 | 不可信内容直接劫持工具调用［S11］ | 数据值篡改（收件人等）［S14］；社会工程/诱导用户复制粘贴［S11］；链式泄漏 | 实现复杂、体验降级（作者自评"pretty bad"）［S11］ | **中**（原理清楚，缺少独立量化评测） |
| CaMeL（Code-then-Execute + capability） | 控制流与不可信数据**分离**，并在**工具调用处**执行策略 | AgentDojo 内置注入几乎全部挡住（Gemini 2.5 Pro 从 300 次降到 0 次）［S14］ | 侧信道、类 ROP 组合、"数据即控制流"的任务、纯文本误导、钓鱼［S14］；多 Agent 组合［S18］；Branch Steering［S19］；伪造可信数据类攻击［S20］ | Token 约 2.8 倍；效用 84% 降到 77%（部分模型与套件降得更多）［S14］；需要编写和维护策略；解密环节有用户疲劳 | **中**（论文证据强，但独立自适应评测缺失［S17］） |
| Design Patterns（Action-Selector / Plan-then-Execute / Map-Reduce / Context-Min.） | 限制不可信输入**能触发的后果**［S15］ | Action-Selector 对注入免疫；P-t-E 防工具被替换；Map-Reduce 防跨文档污染 | P-t-E 防不住参数篡改［S15］；不适用于通用开放任务 | 明确牺牲通用性；需要按场景设计 | **中**（原理性论证 + 10 个案例，缺少统一量化） |
| 信息流控制 / 污点追踪（FIDES、FLOWSEAL、Progent 等） | 在**工具调用/数据流出**处按标签执行确定性策略 | 开启策略检查后 AgentDojo 攻击全部被挡住［S16］；隐私泄露从 52.2% 降到 0.5%［S21］；Progent 小规模自适应复现中守住［S17］ | 不开策略时与普通规划器一样脆弱［S16］；策略错误或过宽；标签伪造/数据注入类［S20］ | 规划器改造、策略编写；FIDES 在推理模型上效用反而 +16%~24%［S16］ | **中**（确定性保证 + 少量独立复现；强自适应评测仍待补充） |
| 最小权限 / 工具过滤 | 缩小注入成功后**可调用的工具集** | AgentDojo 中 ASR 从 57.7% 降到 6.8%［S9］ | 任务所需工具本身足以执行攻击（17% 的用例）、动态规划、长会话"等待"［S9］ | 低，需要按任务裁剪权限 | **中-强** |
| 网络出口白名单 / 禁止自动渲染外链和图片 | 切断最后的**外泄**通道 | 零点击 Markdown 图片外泄［S7］［S6］ | 白名单内的域被滥用：Teams 代理［S22］、api.anthropic.com Files API［S24］；诱导用户点击或复制［S11］；不防完整性破坏（误发、删除） | 低到中，会影响链接和图片体验 | **强**（确定性，有多起真实事故印证其价值与局限） |
| 人工确认（HITL） | 在**高风险动作执行前**加人工闸门 | 低频、高价值操作（付款、删除、外发）［S7］［S26］ | 审批疲劳［S14］［S23］；确认框被注入伪造（LITL）［S25］；用户无法理解晦涩命令［S15］ | 降低自主性，打断流程 | **中**（机制共识强，但缺少 Agent 场景下误批率的量化数据） |
| 沙箱（文件系统 + 网络隔离） | 限制**爆炸半径** | 本地文件破坏、SSH key 外泄、恶意下载［S23］ | 沙箱内允许的通道仍可外泄［S24］；输出内容中的信息泄露［S15］ | 环境配置；可以**减少**确认弹窗（-84%）［S23］ | **中-强** |
| （参考）模型训练类防御（SecAlign、Meta-SecAlign、RL 训练） | 模型**内在**鲁棒性 | 静态 AgentDojo 上 ASR 约 2%［S1］；Anthropic 内部自适应攻击约 1%［S5］ | 自适应攻击下 96%（Meta-SecAlign）［S1］ | 训练成本；早期 SecAlign 在 Agent 任务上效用下降明显［S31］ | 中（不在本视角重点，仅记录效果） |

---

## 本视角小结

1. **【事实，强证据】所有"概率性"防御（分类器、提示技巧、对抗训练）都已被自适应攻击打穿。**12 种防御中多数 ASR >90%，而它们原论文报告的 ASR 接近 0［S1］。人类红队对所有被测场景 100% 成功［S1］。它们的价值在于降低基线攻击量（LLMail-Inject 中叠加多层后成功率极低［S10］），不能作为安全边界。微软、Google、OpenAI、Anthropic 官方都承认无法完全阻止注入［S6］［S7］［S26］［S5］。
2. **【事实+推断】真正能"切断"攻击链的是确定性的系统层控制，但每一种都只切一环。**CaMeL 和 FIDES 切断"不可信数据→控制流/数据流出"［S14］［S16］；出口控制和禁止自动渲染切断"外泄"［S7］［S6］；最小权限和工具过滤缩小"可执行动作"［S9］；沙箱限制"爆炸半径"［S23］。已知绕过点都在各环的接缝处：白名单内的域被滥用［S22］［S24］、多 Agent 组合［S18］、伪造可信数据［S20］、侧信道［S14］。
3. **【事实】架构类防御的代价可以量化，而且在缩小。**CaMeL 的效用代价为 84% 降到 77%，Token 约 2.8 倍［S14］；FIDES 在推理模型上反而多完成 16%~24% 的任务［S16］；更强的模型能更好地适应约束［S14］［S18］。但这些都是在 AgentDojo 上测得，而该基准本身已被指出存在缺陷，并且容易饱和［S30］。
4. **【事实】人工确认是兜底手段，不是主防线。**它有疲劳问题［S14］［S23］，也可能被伪造［S25］。更好的做法是先用沙箱和确定性策略减少需要确认的次数，例如 Anthropic 报告弹窗减少 84%［S23］，只对少量高价值动作保留确认。
5. **【推断】评估方法是当前最大的不确定性。**架构类防御尚缺少与"Attacker Moves Second"同等强度的独立自适应评测，目前只有一个小规模复现，结果对防御有利［S17］。WASP 提醒，低 ASR 可能只是"security by incompetence"［S28］。所以引用任何 ASR 数字时，必须同时写明攻击是否自适应、用的是哪个基准和模型。

---

## 信源

- [S1] The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections｜Nasr, Carlini, Sitawarin, Schulhoff, Hayes, … Tramèr（Google DeepMind/OpenAI/ETH 等）｜2025-10-10｜A｜https://arxiv.org/abs/2510.09023
  摘录："we bypass 12 recent defenses (based on a diverse set of techniques) with attack success rate above 90% for most; importantly, the majority of defenses originally reported near-zero attack success rates."
  摘录："Our search-based adaptive attack (with the detector's confidence score and detection flag fed back to the attacker) achieves ASR of >90% against Protect AI, PromptGuard, and Model Armor (with Gemini-2.5 Pro as the base model). PIGuard is somewhat more resistant but still reaches 71% ASR."
  摘录："using the benchmark's static attacks, observed attack success rates (ASR) as low as 1%. However, when we applied our search-based adaptive attack, the ASR is above 95% for both defenses."
  摘录："MetaSecAlign … reports an attack success rate (ASR) of 2% on the static AgentDojo benchmark. We re-evaluated this defense … and achieved a 96% ASR."
  摘录："the search attack succeeds 69% of the time whereas the red-teaming humans collectively succeeds 100% of the time"
- [S2] LlamaFirewall: An open source guardrail system for building secure AI agents｜Meta｜2025-05-06｜A｜https://arxiv.org/abs/2505.03574
  摘录："The baseline AgentDojo Eval set without any defense exhibited an attack success rate (ASR) of 17.6% and a task utility of 47.7%. Applying PromptGuard V2 86M alone reduced the ASR to 7.5%, a 57% drop, while maintaining utility at 47.0%"
  摘录："The combined configuration PromptGuard + AlignmentCheck delivered the best defensive performance, reducing ASR to 1.75%"
- [S3] InjecGuard: Benchmarking and Mitigating Over-defense in Prompt Injection Guardrail Models｜Li et al.｜2024-10-30｜A｜https://arxiv.org/abs/2410.22770
  摘录："Our results show that state-of-the-art models suffer from over-defense issues, with accuracy dropping close to random guessing levels (60%)."
- [S4] Bypassing Meta's LLaMA Classifier: A Simple Jailbreak｜Robust Intelligence（现属 Cisco）｜2024-07-29｜B｜https://blogs.cisco.com/security/bypassing-metas-llama-classifier-a-simple-jailbreak
  摘录："the model's performance plummeted to 0.2% accuracy, misclassifying 449 out of 450 prompts as benign and demonstrating a complete circumvention of the model's safety mechanisms (Success Rate of 99.8%)."
- [S5] Mitigating the risk of prompt injections in browser use｜Anthropic｜2025-11-24｜A｜https://www.anthropic.com/research/prompt-injection-defenses
  摘录："A 1% attack success rate—while a significant improvement—still represents meaningful risk. No browser agent is immune to prompt injection"
  摘录："We scan all untrusted content that enters the model's context window, and flag potential prompt injections with classifiers."
- [S6] How Microsoft defends against indirect prompt injection attacks｜Microsoft MSRC（Andrew Paverd）｜2025-07-29｜A｜https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks
  摘录："Microsoft's approach therefore does not rely on our ability to block all prompt injections."
  摘录："deterministically block the security impact (i.e., the data exfiltration technique)"
  摘录："We developed FIDES, an approach for deterministically preventing indirect prompt injection in agentic systems"
  （注：curl 被拦截，以上摘录来自 WebFetch 工具返回的原文句子）
- [S7] Mitigating prompt injection attacks with a layered defense strategy｜Google GenAI Security Team｜2025-06-13｜A｜https://security.googleblog.com/2025/06/mitigating-prompt-injection-attacks.html
  摘录："Our markdown sanitizer identifies external image URLs and will not render them, making the "EchoLeak" 0-click image rendering exfiltration vulnerability not applicable to Gemini."
  摘录："potentially risky operations like deleting a calendar event may trigger an explicit user confirmation request"
- [S8] Defending Against Indirect Prompt Injection Attacks With Spotlighting｜Hines et al., Microsoft｜2024-03-20｜A｜https://arxiv.org/abs/2403.14720
  摘录："Using GPT-family models, we find that spotlighting reduces the attack success rate from greater than 50% to below 2% in our experiments with minimal impact on task efficacy."
- [S9] AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents｜Debenedetti et al., ETH Zurich｜2024-06-19｜A｜https://arxiv.org/abs/2406.13352
  摘录（表 5，GPT-4o）："Defenses No defense Delimiting PI detector Repeat prompt Tool filter … Targeted ASR 57.69% 41.65% 7.95% 27.82% 6.84%"
  摘录："The prompt injection detector has too many false positives, however, and significantly degrades utility. Repeating the user prompt after a tool call is a reasonable defense for our attack, but it is unlikely to withstand adaptive attacks"
  摘录："This defense fails, however, when the list of tools to use cannot be planned in advance … or when the tools required to solve the task are also sufficient to carry out the attack (this is true for 17% of our test cases)."
- [S10] LLMail-Inject: A Dataset from a Realistic Adaptive Prompt Injection Challenge｜Abdelnabi, Fay et al.（Microsoft/ISTA/ETH）｜2025-06-11｜A｜https://arxiv.org/abs/2506.09956
  摘录："Only 3,018 submissions (0.8%) resulted in successful end-to-end attacks."
  摘录："We also see that spotlighting can be more effective than some detection defenses alone, such as Prompt Shield. In addition, stacking all defenses provides a significant improvement."
  摘录："in Phase-2, using all defenses combined with GPT-4o did not result in any successful attacks."
- [S11] The Dual LLM pattern for building AI assistants that can resist prompt injection｜Simon Willison｜2023-04-25（2025-04-11 补充更新）｜B｜https://simonwillison.net/2023/Apr/25/dual-llm-pattern/
  摘录："The Privileged LLM only ever sees those variable names."
  摘录："You may have noticed something about this proposed solution: it's pretty bad! Building AI assistants in this way is likely to result in a great deal more implementation complexity and a degraded user experience."
  摘录："The social engineering aspects also mean that this isn't a 100% reliable solution."
- [S12] CaMeL offers a promising new direction for mitigating prompt injection attacks｜Simon Willison｜2025-04-11｜B｜https://simonwillison.net/2025/Apr/11/camel/
  摘录："in application security 99% is a failing grade"
  摘录："With the Dual LLM pattern the P-LLM delegates the task of finding Bob's email address to the Q-LLM—but the Q-LLM is still exposed to potentially malicious instructions."
- [S13] The lethal trifecta for AI agents: private data, untrusted content, and external communication｜Simon Willison｜2025-06-16｜B｜https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
  摘录："in web application security 95% is very much a failing grade."
  摘录："The only way to stay safe there is to avoid that lethal trifecta combination entirely."
- [S14] Defeating Prompt Injections by Design (CaMeL)｜Debenedetti, Shumailov, … Tramèr（Google/Google DeepMind/ETH）｜2025-03-24（v2 2025-06-24）｜A｜https://arxiv.org/abs/2503.18813
  摘录："We demonstrate effectiveness of CaMeL by solving 77% of tasks with provable security (compared to 84% with an undefended system) in AgentDojo."
  摘录："CaMeL requires only 2.82× more input and 2.73× more output tokens than native tool-calling"
  摘录："the number of successful attacks for Gemini 2.5 Pro drops from 300 without to 0 with CaMeL."
  摘录："No, prompt injection attacks are not fully solved. … Importantly, CaMeL suffers from users needing to codify and specify security policies and maintain them."
  摘录："This can lead to user fatigue, where users become desensitized to security prompts and may inadvertently approve malicious actions"
- [S15] Design Patterns for Securing LLM Agents against Prompt Injections｜Beurer-Kellner, Buesser, Creţu, Debenedetti, … Tramèr, Volhejn（Invariant Labs/IBM/EPFL/ETH/Google/Microsoft 等）｜2025-06-10（v3 2025-06-27）｜A｜https://arxiv.org/abs/2506.08837
  摘录："once an LLM agent has ingested untrusted input, it must be constrained so that it is impossible for that input to trigger any consequential actions"
  摘录："As long as both agents and their defenses rely on the current class of language models, we believe it is unlikely that general-purpose agents can provide meaningful and reliable safety guarantees."
  摘录："the agent's plan of tool calls is fixed, but a prompt injection can still manipulate the inputs to these tool calls"
  摘录："It would probably be easy for an attack to obfuscate using innocuous looking commands."
- [S16] Securing AI Agents with Information-Flow Control (FIDES)｜Costa, Köpf, Kolluri, Paverd, Russinovich, Salem, Tople et al., Microsoft｜2025-05-29（v2 2025-09-03）｜A｜https://arxiv.org/abs/2505.23643
  摘录："With policy checks enabled, Fides stops all prompt injection attacks in AgentDojo. Without policy checks, all planners, including Fides, succumb to practical PIAs."
  摘录："Fides completes on average about 16% more tasks than a basic planner. With further prompt tuning, this rises to 24%"
- [S17] Adaptive Evaluation of Out-of-Band Defenses Against Prompt Injection in LLM Agents｜arXiv 预印本｜2026-06-25｜A（预印本，未经同行评审）｜https://arxiv.org/abs/2606.26479
  摘录："we warn that every one of them is validated only on static benchmarks"
  摘录："Progent cut mean attack success roughly sixfold (25.8% to 4.2%), and a hand-crafted adaptive attack did not raise it (2.6%). This is one small-scale data point on a weak model with a single black-box attack template"
- [S18] Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks｜arXiv 预印本｜2026-10-05｜A（预印本）｜https://arxiv.org/abs/2610.05640
  摘录："We find that CaMeL's guarantees do not compose."
  摘录："multi-CaMeL reduces attack success rate (ASR) to 0.0%, compared with 0.2% for individual-agent CaMeL and 12.9% with no CaMeL."
- [S19] CaMeLs Can Use Computers Too: System-level Security for Computer Use Agents｜arXiv 预印本｜2026-01-14（v3）｜A（预印本）｜https://arxiv.org/abs/2601.09923
  摘录："we show that additional measures are needed to defend against Branch Steering attacks, where adversaries deceive the perception model into routing execution down attacker-preferred branches of the plan"
- [S20] Agent Data Injection Attacks are Realistic Threats to AI Agents｜arXiv 预印本｜2026-07-06｜A（预印本）｜https://arxiv.org/abs/2607.05120
  摘录："Despite the similar impact, ADI remains underexplored and easily bypasses existing IPI defenses."
- [S21] Confuse the Model, Control the Flow: … Privacy Leakage from LLM Agents with Information Flow Control (FLOWSEAL)｜arXiv 预印本｜2026-09-12｜A（预印本）｜https://arxiv.org/abs/2609.14003
  摘录："whenever enforcement is a judgment the LLM makes over the same conversational context an adversary controls, the enforcement mechanism and the attack surface coincide."
  摘录："FLOWSEAL reduces leak rates to near zero (e.g., 52.2% to 0.5% against Collaborative Workspace Lure)"
- [S22] EchoLeak: The First Real-World Zero-Click Prompt Injection Exploit in a Production LLM System｜arXiv 案例研究｜2025-09-06｜A｜https://arxiv.org/abs/2509.10540
  摘录："By chaining multiple bypasses-evading Microsofts XPIA (Cross Prompt Injection Attempt) classifier, circumventing link redaction with reference-style Markdown, exploiting auto-fetched images, and abusing a Microsoft Teams proxy allowed by the content security policy"
- [S23] Beyond permission prompts: making Claude Code more secure and autonomous｜Anthropic Engineering｜2025-10-20｜A｜https://www.anthropic.com/engineering/claude-code-sandboxing
  摘录："In our internal usage, we've found that sandboxing safely reduces permission prompts by 84%."
  摘录："Constantly clicking "approve" slows down development cycles and can lead to 'approval fatigue', where users might not pay close attention to what they're approving"
  摘录："effective sandboxing requires both filesystem and network isolation."
- [S24] Claude Pirate: Abusing Anthropic's File API For Data Exfiltration｜Johann Rehberger（Embrace The Red）｜2025（URL 路径为 2025；SecurityWeek 等媒体于 2025-11 报道；页面具体日期未核实）｜B｜https://embracethered.com/blog/posts/2025/claude-abusing-network-access-and-anthropic-api-for-data-exfiltration/
  摘录："At second glance I stopped at the first entry, api.anthropic.com, to think things through adversarially."
  摘录："The upload will not happen to the user's Anthropic account, but to the attackers, because it's using the attacker's ANTHROPIC_API_KEY here!"
- [S25] HITL Dialog Forging (aka Lies-in-the-Loop)｜OWASP 社区页（Ori Ron、Dor Tumarkin，Checkmarx Zero）｜2025（具体日期未核实）｜B｜https://owasp.org/www-community/attacks/Lies_in_the_Loop
  摘录："The LITL attack exploits the fact that HITL dialogs, which are usually the only feedback users see, are generated based on context that an attacker can control through indirect prompt injection."
- [S26] OpenAI says AI browsers may always be vulnerable to prompt injection attacks｜TechCrunch（转引 OpenAI 博客 "Hardening Atlas against prompt injection"，原文返回 403，无法直接获取）｜2025-12-22｜B｜https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/
  摘录（OpenAI 原话，经转引）："Prompt injection, much like scams and social engineering on the web, is unlikely to ever be fully 'solved,'"
  摘录（OpenAI 原话，经转引）："Wide latitude makes it easier for hidden or malicious content to influence the agent, even when safeguards are in place"
- [S27] InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated LLM Agents｜Zhan et al., UIUC｜2024-03-05｜A｜https://arxiv.org/abs/2403.02691
  摘录："InjecAgent comprises 1,054 test cases covering 17 different user tools and 62 attacker tools. … with ReAct-prompted GPT-4 vulnerable to attacks 24% of the time."
- [S28] WASP: Benchmarking Web Agent Security Against Prompt Injection Attacks｜Evtimov et al., Meta｜2025-04-22｜A｜https://arxiv.org/abs/2504.18575
  摘录："while attacks partially succeed in up to 86% of the case, even state-of-the-art agents often struggle to fully complete the attacker goals -- highlighting the current state of security by incompetence."
- [S29] Security Challenges in AI Agent Deployment: Insights from a Large Scale Public Competition (ART)｜Gray Swan 等｜2025-07-28｜A｜https://arxiv.org/abs/2507.20526
  摘录："Nearly all agents exhibit policy violations for most behaviors within 10-100 queries, with high attack transferability across models and tasks."
- [S30] Indirect Prompt Injections: Are Firewalls All You Need, or Stronger Benchmarks?｜arXiv｜2025-10-06｜A｜https://arxiv.org/abs/2510.05244
  摘录："Our analysis also reveals critical limitations in these existing benchmarks, including flawed success metrics, implementation bugs, and most importantly, weak attacks, hindering progress."
- [S31] Meta-SecAlign: Training LLMs against Prompt Injection for Robust Agents｜Chen et al., Meta｜2025-07-03｜A｜https://arxiv.org/abs/2507.02735
  摘录："we find that SecAlign actually suffers from significant utility degradation, especially in agentic tasks where the threat of prompt injection is prominent."
- [S32] Evaluating the Robustness of Large Language Model Safety Guardrails Against Adversarial Attacks｜arXiv｜2025-11-27｜A（预印本）｜https://arxiv.org/abs/2511.22047
  摘录："all models showed substantial performance degradation on unseen prompts, with Qwen3Guard dropping from 91.0% to 33.8%"
- [S33] MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents｜Zhu et al.｜2025-02-07｜A｜https://arxiv.org/abs/2502.05174
  摘录："We identify an attack if the actions generated in the original and masked executions are similar."（后被 [S1] 列为可被自适应攻击绕过的防御之一）
- [S34] Agent Security Bench (ASB)｜Zhang et al.｜2024-10-03｜A｜https://arxiv.org/abs/2410.02644
  摘录："with the highest average attack success rate of 84.30%, but limited effectiveness shown in current defenses"
