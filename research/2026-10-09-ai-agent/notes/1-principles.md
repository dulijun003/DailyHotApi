# 视角 1：原理机制

> 检索日期：2026-10-09。引文为原文摘录（英文保留原文）；摘录均通过网页抓取工具获得，个别长段只截取关键句。标注"二手"的数字未能直接核对一手文件。

## 子问题 1：大模型为什么没有"指令通道"和"数据通道"之分？为什么不存在"参数化查询"的等价物？

### 发现
- 【事实】SQL 注入有确定性的根治手段：参数化查询让数据库引擎在结构上不可能把参数当作 SQL 执行。Willison 在 2022 年首次将提示词注入类比为 SQL 注入时写道 "The best protection against SQL injection attacks is to use parameterized queries"，但随后补充说 "parameterized prompts" 在当前架构上 "extremely difficult, if not impossible, to implement"。［S1］
- 【事实】英国 NCSC 在 2025-12-08 的官方博客中明确指出两者的本质差别：SQL 注入 "can be properly mitigated with parameterised queries"，而 LLM 内部 "there is only ever 'next token'"，即开发者指令与不可信内容拼进同一个 prompt 后，模型内部没有可执行的安全边界。［S2］
- 【观点】NCSC（作者 Dave Chismon）认为，应把 LLM 看作 "an exploitation of an 'inherently confusable deputy'"（"天生可被混淆的代理人"），而不是代码注入问题；并判断 "prompt injection attacks may never be totally mitigated in the way that SQL injection attacks can be"。［S2］
- 【事实】学术测量：Zverev 等（ICLR 2024 workshop，2025-01 修订）提出"指令-数据分离"的形式化定义和 SEP 数据集，指出 "none of the existing models provide a dedicated mechanism to distinguish between instructions and data"。实测朴素分离分数约在 13.3%（Phi-3）到 73.2%（Gemma-2B）之间，GPT-4 为 20.8%。用 DPO 微调可把分离分数提高到约 96%，但效用下降约 17.8 个百分点。论文结论是所有模型都达不到高分离度，提示工程和微调要么改善有限，要么损害效用。［S3］
- 【事实】OpenAI 的 instruction hierarchy 论文（2024-04）把漏洞根源描述为 "LLMs often consider system prompts (e.g., text from an application developer) to be the same priority as text from untrusted users and third parties"。［S4］
- 【事实】Microsoft MSRC（2025-07-29）把间接注入定性为 "an inherent risk that arises from the probabilistic language modelling"。［S5］
- 【观点】Simon Willison（2025-06-16）认为 "LLMs are unable to reliably distinguish the importance of instructions based on where they came from"。［S6］

### 冲突与不确定
- "无法分离"是指当前架构下不存在确定性的分离机制，并不是说分离程度无法改善：Zverev 等的数据显示，训练可以显著提高分离分数，但要付出效用代价［S3］；IH 类训练也能提高鲁棒性［S4］［S11］。各来源的共识是：可以缓解，但没有类似参数化查询那样在结构上保证的手段。
- 有研究在 LLM 外部重建"控制流与数据流分离"，例如 CaMeL 的 "the untrusted data retrieved by the LLM can never impact the program flow"［S15］。这属于系统层的"参数化"，不在模型层，留给架构视角展开。
- 中文二手解读（tianpan.co 等，C 级）同样指出"解析器本身就是一个被训练来理解任意位置自然语言指令的模型"。仅作线索，结论已回溯到 S1–S3。

## 子问题 2：间接注入造成实际危害需要哪些条件同时成立？去掉任意一个会怎样？

### 发现
- 【观点】Simon Willison（2025-06-16）提出"lethal trifecta"：私有数据访问 + 暴露于不可信内容 + 对外通信能力。"If your agent combines these three features, an attacker can easily trick it into accessing your private data and sending it to that attacker." 他认为唯一安全的做法是 "avoid that lethal trifecta combination entirely"。［S6］
- 【事实/官方框架】Meta（2025-10-31）的 "Agents Rule of Two" 规定，在 "until robustness research allows us to reliably detect and refuse prompt injection" 之前，一个会话最多同时满足以下三项中的两项：[A] 处理不可信输入，[B] 访问敏感系统或私有数据，[C] 改变状态或对外通信。Meta 的判断是 "Prompt injection is a fundamental, unsolved weakness in all LLMs."［S7］
- 【事实/官方框架】去掉一项的效果（Meta 的示例）：
  - [AC] 组合（没有敏感数据）："the agent won't have access to any sensitive data or systems"，注入后没有可窃取的目标。
  - [AB] 组合（限制对外通信）可以 "preventing the attacker from ultimately completing their attack chain"。［S7］
- 【观点】Willison（2025-11-02）赞同 Rule of Two，并指出 trifecta "only covers the risk of data exfiltration"。Rule of Two 加入了"改变状态"，把不涉及数据窃取的工具滥用也纳入考虑。他也提出异议：即使没有敏感数据，"不可信输入 + 可改变状态"同样不安全，也就是说去掉 [B] 不能消除破坏型危害。［S8］
- 【事实】Microsoft 的实践印证了"切断外传通道"的价值：发现 markdown 图片外传漏洞后，MSRC "took steps to deterministically block the security impact (i.e., the data exfiltration technique)"，同时承认概率性防御 "may not prevent or detect every instance of the attack"。［S5］
- 【观点】Debenedetti 等（2025-06，含 IBM、Google、Microsoft 等机构作者）在 Design Patterns 论文中给出的原则是：智能体摄入不可信输入后，"it must be constrained so that it is impossible for that input to trigger any consequential actions"；并认为 "we believe it is unlikely that general-purpose agents can provide meaningful and reliable safety guarantees"（前提是继续依赖当前这类语言模型）。［S9］

### 冲突与不确定
- 条件的数量和划分有分歧。Willison 的 trifecta 只针对数据外传，有三个条件［S6］。Meta 的 Rule of Two 把"外传"和"改变状态"合并为 [C]［S7］。Willison 本人认为，即使去掉敏感数据，[A]+[C] 仍然危险［S8］，因此"去掉任意一项即安全"只对数据窃取型危害成立，对破坏型和越权操作型危害不一定成立。
- "对外通信"的边界不好界定，例如渲染图片、链接或调用任何带网络的工具都可能构成外传渠道（见 S5 的 markdown 图片案例），实际中较难彻底去除。

## 子问题 3：模型层缓解能把攻击成功率降到什么程度？为什么无法降到零？

### 发现（公开数字，均为各自设定下的厂商或作者自报结果）
- 【事实】Spotlighting（Microsoft Research，2024-03）：在 GPT 系列实验中，攻击成功率 "from greater than 50% to below 2%"。MSRC（2025-07）说明它有三种模式：delimiting（"a specific randomized text delimiter is added before and after the untrusted input"）、datamarking 和 encoding（base64/ROT13）。［S10］［S5］
- 【事实】Instruction Hierarchy（OpenAI，2024-04）：在 GPT-3.5 上，鲁棒性提升 "up to 63%"，对未见过的攻击类型（含工具调用中的注入）提升 "up to 34%"。论文承认模型 "are likely still vulnerable to powerful adversarial attacks"，并存在过度拒绝的回退。［S4］
- 【事实】IH-Challenge（OpenAI，2026-03-11）：GPT-5-Mini 在 16 个基准（含人类红队）上的 IH 鲁棒性平均 "+10.0%"（84.1% → 94.1%），不安全行为 "from 6.6% to 0.7%"。论文同时指出 "robust IH behavior is difficult to train" 且 "models can learn shortcuts such as overrefusing"。［S11］
- 【事实】Google DeepMind 对 Gemini 的对抗训练（2025-05）：在邮件场景中，Gemini 2.0 → 2.5 的 ASR 变化为 TAP 99.8% → 53.6%、Actor-Critic 66.2% → 40.8%、Beam Search 74.8% → 4.2%；在日历场景中为 TAP 100% → 94.6%。作者的结论是对抗训练 "clearly not sufficient as a defense in isolation"，"it is not possible to claim that the model is truly robust"，"Robustness requires defense in depth"；并指出 "More capable models aren't necessarily more secure"。［S12］
- 【事实】Anthropic（2025-11-24）：Claude Opus 4.5 在浏览器场景中，面对给予 100 次尝试的自适应攻击者，ASR 为 1%。原文："A 1% attack success rate—while a significant improvement—still represents meaningful risk." 以及 "No browser agent is immune to prompt injection"。［S13］
- 【事实·二手】据 The Decoder（2026-07-25）转述 Anthropic Opus 5 system card：浏览器场景 129 个环境中，开启 Auto Mode（输入扫描 + 危险动作拦截两层系统防护）时 "the attack success rate hit zero percent"，不开启时 "Opus 5 sits at 3.7 percent"；在 Gray Swan 间接注入基准上，15 次尝试的成功率 "dropped from 5.5 percent (Opus 4.8) to 2.0 percent"。未能直接核对 system card 原文。［S14］
- 【事实】Meta-SecAlign（2025-07，v4 于 2026-09 修订）报告说，原 SecAlign 在扩大规模后 "actually suffers from significant utility degradation"。未在摘要中找到 AgentDojo 具体数字。［S16］

### 为什么无法降到零
- 【观点】Google DeepMind：攻击空间无法穷举，所以不能宣称真正鲁棒（"it is not possible to claim that the model is truly robust"）。［S12］
- 【观点】OpenAI（2025-12，ChatGPT Atlas 加固博客，经 TechCrunch 等转述）："Prompt injection, much like scams and social engineering on the web, is unlikely to ever be fully 'solved'"。［S17］
- 【事实】机制层面：训练只是改变概率分布，没有建立结构性边界（NCSC："there is only ever 'next token'"）［S2］；能力更强、指令遵循更好的模型 "are in some cases easier to attack"［S12］；把阈值压得更严会引入过度拒绝和效用损失［S3］［S4］［S11］。

### 冲突与不确定
- 各厂商的数字测量设定不同：攻击者类型（静态或自适应）、尝试次数（1、10、15、100 次）、场景数、是否叠加系统层防护都不一致，不能横向比较。Anthropic 在后续文章中说明 2025-11 的结果未开启 extended thinking 且评分模型已更换（据搜索结果摘要，未直接核对）。
- Opus 5 的"0%"是"模型 + 两层系统防护"的组合结果，模型单独为 3.7%［S14］，不能当作模型层降到零的证据。独立测试与厂商数字也有出入：Gray Swan 对 Opus 4.5 的测试（The Decoder 报道）显示，单次强攻击成功率为 4.7%，10 次尝试为 33.6%，高于 Anthropic 自报的 1%（设定不同）。
- Spotlighting 自报 <2%［S10］与 "The Attacker Moves Second" 测得的自适应 ASR >95%［S18］差距很大，原因在于静态评估和自适应评估的区别（见子问题 4）。

## 子问题 4：面对自适应攻击者，检测类与模型层防御表现如何？

### 发现
- 【事实】"The Attacker Moves Second"（Nasr 等 14 位作者，来自 OpenAI、Anthropic、Google DeepMind 及学界，arXiv 2025-10-10，USENIX Security 2026）用梯度、强化学习、随机搜索和人类红队攻击 12 种防御，大多数 ASR 超过 90%，而 "the majority of defenses originally reported near-zero attack success rates"。［S18］
  - Spotlighting 和 Prompt Sandwiching：静态 ASR 最低约 1%（AgentDojo），自适应搜索 ASR >95%。
  - MetaSecAlign：原报告 2%，自适应 96%。
  - MELON：不知道防御细节时 76%，完全知情时 95%。
  - Data Sentinel：被 RL 攻击全部绕过，任务重定向准确率 >80%。
  - 检测器 Protect AI、PromptGuard、Model Armor 的自适应 ASR >90%，PIGuard 为 71%。
  - 人类红队（>500 名参与者，奖金 2 万美元）"succeeds in all the cases we evaluated"。
  - 结论原文："Our adaptive attacks continue to bypass both the target model and every detector we evaluated"；"stacking additional detectors does not resolve the underlying robustness problem"；"success on static evaluations provides only a false sense of security"。
  - 检测器失效的原因：检测器 "share the same weaknesses as any other neural networks"，且许多成功的触发文本本身不明显恶意，"the detectors cannot flag such triggers as unsafe, especially out of context"。
- 【事实】Zhan 等（2025-02，NAACL 2025 Findings）"Adaptive Attacks Break Defenses Against Indirect Prompt Injection Attacks on LLM Agents"：评估 8 种防御，"bypass all of them using adaptive attacks"，ASR "consistently achiev[e] … over 50%"。［S19］
- 【事实】Google DeepMind（2025-05）："In 16 out of 24 cases (8 defenses × 3 attacks), the adaptive attack is equal to or outperforms the non-adaptive counterpart"；"the resilience observed against non-adaptive attacks, unfortunately, does not necessarily translate to resilience against adaptive adversaries"。［S12］
- 【观点】Willison（2025-11-02）认为静态样例攻击 "an almost useless way to evaluate these defenses"，并且不认同论文作者对很快会出现可靠防御的乐观看法，主张以 Rule of Two 作为当前最佳实践。［S8］
- 【观点】NCSC 警告不要依赖拒绝列表式检测（例如屏蔽 "ignore previous instructions"），因为攻击者可以无限改写。［S2］

### 冲突与不确定
- 厂商在生产中仍然部署分类器（Anthropic 称 "We scan all untrusted content that enters the model's context window"［S13］，Microsoft 使用 Prompt Shields［S5］），并报告它们与模型训练叠加后效果很好（例如 Opus 5 + Auto Mode 为 0%［S14］）。学术自适应攻击论文则认为检测器在知情攻击者面前普遍失效［S18］［S19］。两者的差别在于威胁模型：厂商评估的是固定基准或内部攻击者，学术研究评估的是针对具体防御、计算预算很大的攻击者。目前未找到针对 Opus 5 + Auto Mode 的独立自适应攻击评估。
- "The Attacker Moves Second" 没有评估 OpenAI 的 instruction hierarchy 模型本身［S18］，所以 IH 训练在同等强度的自适应攻击下表现如何，未找到可靠来源。

## 本视角小结
1. 根本原因是结构性的：LLM 把开发者指令和外部内容都当作同一个 token 序列处理，不存在参数化查询那样的确定性边界（NCSC、Willison、Zverev 等）。因此 NCSC、OpenAI、Meta 都公开表示提示词注入可能永远无法被完全解决。
2. 危害要成立，需要"不可信输入 + 敏感数据/能力 + 外传或状态改变通道"组合在一起（lethal trifecta / Rule of Two）。去掉一项能在架构上切断数据窃取链，但 Willison 指出，对破坏型操作来说，仅去掉敏感数据并不够。
3. 模型层缓解（spotlighting、IH 训练、对抗训练、RL）可以把自报的 ASR 从 >50% 降到 0.x%–数个百分点，但这些数字依赖测量设定，并伴随过度拒绝或效用损失；没有任何一方声称单靠模型能降到零。
4. 在自适应攻击者面前，静态评估严重高估防御效果：12 种防御从近 0% 被打到大多 >90%，检测器同样被绕过，人类红队 100% 成功。检测类防御只能作为纵深防御中的一层，不能作为安全边界。
5. 能给出确定性保证的方向都在模型之外，例如确定性封堵外传通道（MSRC）、控制流与数据流分离（CaMeL：在 AgentDojo 上以 77% 对比无防御 84% 的任务完成率换取可证明的安全性）、FIDES 信息流控制。这些留给架构视角深入。

## 信源
- [S1] Prompt injection attacks against GPT-3｜Simon Willison's Weblog｜2022-09-12｜B｜https://simonwillison.net/2022/Sep/12/prompt-injection/
  摘录："The best protection against SQL injection attacks is to use parameterized queries."；（更新）"extremely difficult, if not impossible, to implement on the current architecture of large language models"
- [S2] Prompt injection is not SQL injection (it may be worse)｜UK NCSC（Dave Chismon）｜2025-12-08｜A｜https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection
  摘录："SQL injection can be properly mitigated with parameterised queries"；"there is only ever 'next token'"；"prompt injection attacks may never be totally mitigated in the way that SQL injection attacks can be"；"The best we can hope for is reducing the likelihood or impact of attacks"
- [S3] Can LLMs Separate Instructions From Data? And What Do We Even Mean By That?｜Zverev, Abdelnabi, Tabesh, Fritz, Lampert（arXiv 2403.06833）｜2024-03-11（v3 2025-01-31）｜A｜https://arxiv.org/abs/2403.06833
  摘录："none of the existing models provide a dedicated mechanism to distinguish between instructions and data"
- [S4] The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions｜OpenAI（Wallace 等，arXiv 2404.13208）｜2024-04-19｜A｜https://arxiv.org/abs/2404.13208
  摘录："LLMs often consider system prompts (e.g., text from an application developer) to be the same priority as text from untrusted users and third parties"；"drastically increases robustness"；"are likely still vulnerable to powerful adversarial attacks"
- [S5] How Microsoft defends against indirect prompt injection attacks｜Microsoft MSRC（Andrew Paverd）｜2025-07-29｜A｜https://www.microsoft.com/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks
  摘录："Indirect prompt injection is an inherent risk that arises from the probabilistic language modelling"；"took steps to deterministically block the security impact (i.e., the data exfiltration technique)"；"may not prevent or detect every instance of the attack"
- [S6] The lethal trifecta for AI agents: private data, untrusted content, and external communication｜Simon Willison's Weblog｜2025-06-16｜B｜https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
  摘录："If your agent combines these three features, an attacker can easily trick it into accessing your private data and sending it to that attacker."；"LLMs are unable to reliably distinguish the importance of instructions based on where they came from."；"in web application security 95% is very much a failing grade"
- [S7] Agents Rule of Two: A Practical Approach to AI Agent Security｜Meta AI Blog｜2025-10-31｜A｜https://ai.meta.com/blog/practical-ai-agent-security/
  摘录："Prompt injection is a fundamental, unsolved weakness in all LLMs."；"until robustness research allows us to reliably detect and refuse prompt injection"；"preventing the attacker from ultimately completing their attack chain"
- [S8] New prompt injection papers: Agents Rule of Two and The Attacker Moves Second｜Simon Willison's Weblog｜2025-11-02｜B｜https://simonwillison.net/2025/Nov/2/new-prompt-injection-papers/
  摘录："only covers the risk of data exfiltration"；"an almost useless way to evaluate these defenses"
- [S9] Design Patterns for Securing LLM Agents against Prompt Injections｜Beurer-Kellner, Debenedetti 等（arXiv 2506.08837）｜2025-06-10（v3 2025-06-27）｜A｜https://arxiv.org/abs/2506.08837
  摘录："it must be constrained so that it is impossible for that input to trigger any consequential actions"；"we believe it is unlikely that general-purpose agents can provide meaningful and reliable safety guarantees"
- [S10] Defending Against Indirect Prompt Injection Attacks With Spotlighting｜Microsoft Research（Hines 等，arXiv 2403.14720）｜2024-03-20｜A｜https://arxiv.org/abs/2403.14720
  摘录："reduces the attack success rate from greater than 50% to below 2%"
- [S11] IH-Challenge: A Training Dataset to Improve Instruction Hierarchy on Frontier LLMs｜OpenAI（arXiv 2603.10521；官方博客 https://openai.com/index/instruction-hierarchy-challenge）｜2026-03-11｜A｜https://arxiv.org/abs/2603.10521
  摘录："by +10.0% on average across 16 in-distribution, out-of-distribution, and human red-teaming benchmarks"；"from 6.6% to 0.7%"；"robust IH behavior is difficult to train"；"models can learn shortcuts such as overrefusing"
- [S12] Lessons from Defending Gemini Against Indirect Prompt Injections｜Google DeepMind（Shi 等，arXiv 2505.14534）｜2025-05-20｜A｜https://arxiv.org/abs/2505.14534
  摘录："clearly not sufficient as a defense in isolation"；"it is not possible to claim that the model is truly robust"；"Robustness requires defense in depth"；"More capable models aren't necessarily more secure"；"the resilience observed against non-adaptive attacks, unfortunately, does not necessarily translate to resilience against adaptive adversaries"
- [S13] Mitigating the risk of prompt injections in browser use｜Anthropic｜2025-11-24｜A｜https://www.anthropic.com/research/prompt-injection-defenses
  摘录："A 1% attack success rate—while a significant improvement—still represents meaningful risk."；"No browser agent is immune to prompt injection"；"We scan all untrusted content that enters the model's context window"
- [S14] Opus 5 may have solved browser-based prompt injection…｜The Decoder（转述 Anthropic Opus 5 System Card）｜2026-07-25｜B（二手，system card 原文未核对）｜https://the-decoder.com/opus-5-may-have-solved-browser-based-prompt-injection-the-biggest-security-flaw-haunting-ai-agents/
  摘录："the attack success rate hit zero percent across 129 test scenarios"；"Without them, Opus 5 sits at 3.7 percent."；"dropped from 5.5 percent (Opus 4.8) to 2.0 percent"
- [S15] Defeating Prompt Injections by Design (CaMeL)｜Debenedetti, Shumailov 等（Google DeepMind 等，arXiv 2503.18813）｜2025-03-24（v2 2025-06-24）｜A｜https://arxiv.org/abs/2503.18813
  摘录："the untrusted data retrieved by the LLM can never impact the program flow"；"solving 77% of tasks with provable security (compared to 84% with an undefended system) in AgentDojo"
- [S16] Meta-SecAlign: Training LLMs against Prompt Injection for Robust Agents｜Meta FAIR 等（arXiv 2507.02735）｜2025-07-03（v4 2026-09-28）｜A｜https://arxiv.org/abs/2507.02735
  摘录："we find that SecAlign actually suffers from significant utility degradation"
- [S17] OpenAI says AI browsers may always be vulnerable to prompt injection attacks｜TechCrunch（转述 OpenAI Atlas 加固博客）｜2025-12-22｜B｜https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/
  摘录："Prompt injection, much like scams and social engineering on the web, is unlikely to ever be fully 'solved,'"
- [S18] The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections｜Nasr, Carlini 等（OpenAI/Anthropic/Google DeepMind 等，arXiv 2510.09023；USENIX Security 2026）｜2025-10-10｜A｜https://arxiv.org/abs/2510.09023
  摘录："the majority of defenses originally reported near-zero attack success rates"；"Our adaptive attacks continue to bypass both the target model and every detector we evaluated"；"stacking additional detectors does not resolve the underlying robustness problem"；"success on static evaluations provides only a false sense of security"
- [S19] Adaptive Attacks Break Defenses Against Indirect Prompt Injection Attacks on LLM Agents｜Zhan 等（arXiv 2503.00061，NAACL 2025 Findings）｜2025-02-27｜A｜https://arxiv.org/abs/2503.00061
  摘录："evaluate eight different defenses and bypass all of them using adaptive attacks"；"consistently achieving an attack success rate of over 50%"
- [C1]（仅作线索）好帮手 AI 的悖论 / 智能体管道提示注入防御｜tianpan.co 中文博客｜2026-04/05｜C｜https://tianpan.co/zh/blog/2026-04-18-prompt-injection-agentic-pipelines-defense
  备注：中文解读，转述 Willison 的三要素和"无参数化查询等价物"观点，结论已回溯到 S1、S2、S6。未找到国内头部安全团队（腾讯朱雀、奇安信、绿盟等）就此主题发表的可靠一手解读。
