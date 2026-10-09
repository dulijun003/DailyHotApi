# 信源总表
> 合并自 notes/ 下 5 个视角，按 URL 去重，共 106 条。"视角"一列表示哪些视角引用了该信源。
> 笔记中的局部编号对照：见文末"编号对照表"（例如 4-S14 表示视角 4 笔记中的 [S14]）。

- [G1] Prompt injection attacks against GPT-3｜Simon Willison's Weblog｜2022-09-12｜B｜https://simonwillison.net/2022/Sep/12/prompt-injection/｜视角 1
  摘录："The best protection against SQL injection attacks is to use parameterized queries."；（更新）"extremely difficult, if not impossible, to implement on the current architecture of large language models"
- [G2] Prompt injection is not SQL injection (it may be worse)｜UK NCSC（Dave Chismon）｜2025-12-08｜A｜https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection｜视角 1,5
  摘录："SQL injection can be properly mitigated with parameterised queries"；"there is only ever 'next token'"；"prompt injection attacks may never be totally mitigated in the way that SQL injection attacks can be"；"The best we can hope for is reducing the likelihood or impact of attacks"
  摘录："Design protections need to therefore focus more on deterministic (non-LLM) safeguards that constrain the actions of the system, rather than just attempting to prevent malicious content reaching the LLM."；"when an LLM processes information from a party, the privileges it has drops to that of the party"；"If the system’s security cannot tolerate the remaining risk, it may not be a good use case for LLMs."
- [G3] Can LLMs Separate Instructions From Data? And What Do We Even Mean By That?｜Zverev, Abdelnabi, Tabesh, Fritz, Lampert（arXiv 2403.06833）｜2024-03-11（v3 2025-01-31）｜A｜https://arxiv.org/abs/2403.06833｜视角 1
  摘录："none of the existing models provide a dedicated mechanism to distinguish between instructions and data"
- [G4] The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions｜OpenAI（Wallace 等，arXiv 2404.13208）｜2024-04-19｜A｜https://arxiv.org/abs/2404.13208｜视角 1
  摘录："LLMs often consider system prompts (e.g., text from an application developer) to be the same priority as text from untrusted users and third parties"；"drastically increases robustness"；"are likely still vulnerable to powerful adversarial attacks"
- [G5] How Microsoft defends against indirect prompt injection attacks｜Microsoft MSRC（Andrew Paverd）｜2025-07-29｜A｜https://www.microsoft.com/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks｜视角 1,2,4,5
  摘录："Indirect prompt injection is an inherent risk that arises from the probabilistic language modelling"；"took steps to deterministically block the security impact (i.e., the data exfiltration technique)"；"may not prevent or detect every instance of the attack"
  摘录："cause the LLM output an HTML image tag or equivalent in markdown where the source URL is the attacker's server."；"the prompt injection could cause the LLM to output a clickable link to the attacker's server"
  摘录："Microsoft's approach therefore does not rely on our ability to block all prompt injections."
  摘录："deterministically block the security impact (i.e., the data exfiltration technique)"
  摘录："We developed FIDES, an approach for deterministically preventing indirect prompt injection in agentic systems"
  （注：curl 被拦截，以上摘录来自 WebFetch 工具返回的原文句子）
  摘录："a probabilistic technique to help the LLM distinguish user-provided instructions from potentially untrusted external text"；"This can be deterministically mitigated using fine-grained permissions and access controls"；"the user must explicitly approve the generated text and send the email themselves"
- [G6] The lethal trifecta for AI agents: private data, untrusted content, and external communication｜Simon Willison's Weblog｜2025-06-16｜B｜https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/｜视角 1,2,4,5
  摘录："If your agent combines these three features, an attacker can easily trick it into accessing your private data and sending it to that attacker."；"LLMs are unable to reliably distinguish the importance of instructions based on where they came from."；"in web application security 95% is very much a failing grade"
  摘录："Exposure to untrusted content"；"If a tool can make an HTTP request—to an API, or to load an image, or even providing a link for a user to click"
  摘录："in web application security 95% is very much a failing grade."
  摘录："The only way to stay safe there is to avoid that lethal trifecta combination entirely."
  摘录："an attacker can easily trick it into accessing your private data and sending it to that attacker"；"The only way to stay safe there is to avoid that lethal trifecta combination entirely."
- [G7] Agents Rule of Two: A Practical Approach to AI Agent Security｜Meta AI Blog｜2025-10-31｜A｜https://ai.meta.com/blog/practical-ai-agent-security/｜视角 1,5
  摘录："Prompt injection is a fundamental, unsolved weakness in all LLMs."；"until robustness research allows us to reliably detect and refuse prompt injection"；"preventing the attacker from ultimately completing their attack chain"
  摘录："[A] An agent can process untrustworthy inputs"；"[B] An agent can have access to sensitive systems or private data"；"[C] An agent can change state or communicate externally"
- [G8] New prompt injection papers: Agents Rule of Two and The Attacker Moves Second｜Simon Willison's Weblog｜2025-11-02｜B｜https://simonwillison.net/2025/Nov/2/new-prompt-injection-papers/｜视角 1
  摘录："only covers the risk of data exfiltration"；"an almost useless way to evaluate these defenses"
- [G9] Design Patterns for Securing LLM Agents against Prompt Injections｜Beurer-Kellner, Debenedetti 等（arXiv 2506.08837）｜2025-06-10（v3 2025-06-27）｜A｜https://arxiv.org/abs/2506.08837｜视角 1,4,5
  摘录："it must be constrained so that it is impossible for that input to trigger any consequential actions"；"we believe it is unlikely that general-purpose agents can provide meaningful and reliable safety guarantees"
  摘录："once an LLM agent has ingested untrusted input, it must be constrained so that it is impossible for that input to trigger any consequential actions"
  摘录："As long as both agents and their defenses rely on the current class of language models, we believe it is unlikely that general-purpose agents can provide meaningful and reliable safety guarantees."
  摘录："the agent's plan of tool calls is fixed, but a prompt injection can still manipulate the inputs to these tool calls"
  摘录："It would probably be easy for an attack to obfuscate using innocuous looking commands."
  摘录："once an LLM agent has ingested untrusted input, it must be constrained so that it is impossible"（后半句：该输入不能触发任何有负面副作用的动作）
- [G10] Defending Against Indirect Prompt Injection Attacks With Spotlighting｜Microsoft Research（Hines 等，arXiv 2403.14720）｜2024-03-20｜A｜https://arxiv.org/abs/2403.14720｜视角 1,4
  摘录："reduces the attack success rate from greater than 50% to below 2%"
  摘录："Using GPT-family models, we find that spotlighting reduces the attack success rate from greater than 50% to below 2% in our experiments with minimal impact on task efficacy."
- [G11] IH-Challenge: A Training Dataset to Improve Instruction Hierarchy on Frontier LLMs｜OpenAI（arXiv 2603.10521；官方博客 https://openai.com/index/instruction-hierarchy-challenge）｜2026-03-11｜A｜https://arxiv.org/abs/2603.10521｜视角 1
  摘录："by +10.0% on average across 16 in-distribution, out-of-distribution, and human red-teaming benchmarks"；"from 6.6% to 0.7%"；"robust IH behavior is difficult to train"；"models can learn shortcuts such as overrefusing"
- [G12] Lessons from Defending Gemini Against Indirect Prompt Injections｜Google DeepMind（Shi 等，arXiv 2505.14534）｜2025-05-20｜A｜https://arxiv.org/abs/2505.14534｜视角 1
  摘录："clearly not sufficient as a defense in isolation"；"it is not possible to claim that the model is truly robust"；"Robustness requires defense in depth"；"More capable models aren't necessarily more secure"；"the resilience observed against non-adaptive attacks, unfortunately, does not necessarily translate to resilience against adaptive adversaries"
- [G13] Mitigating the risk of prompt injections in browser use｜Anthropic｜2025-11-24｜A｜https://www.anthropic.com/research/prompt-injection-defenses｜视角 1,2,4,5
  摘录："A 1% attack success rate—while a significant improvement—still represents meaningful risk."；"No browser agent is immune to prompt injection"；"We scan all untrusted content that enters the model's context window"
  摘录："every webpage an agent visits is a potential vector for attack"；"every webpage, embedded document, advertisement, and dynamically loaded script"
  摘录："A 1% attack success rate—while a significant improvement—still represents meaningful risk. No browser agent is immune to prompt injection"
  摘录："We scan all untrusted content that enters the model's context window, and flag potential prompt injections with classifiers."
  摘录："No browser agent is immune to prompt injection."；"A 1% attack success rate—while a significant improvement—still represents meaningful risk."
- [G14] Opus 5 may have solved browser-based prompt injection…｜The Decoder（转述 Anthropic Opus 5 System Card）｜2026-07-25｜B（二手，system card 原文未核对）｜https://the-decoder.com/opus-5-may-have-solved-browser-based-prompt-injection-the-biggest-security-flaw-haunting-ai-agents/｜视角 1
  摘录："the attack success rate hit zero percent across 129 test scenarios"；"Without them, Opus 5 sits at 3.7 percent."；"dropped from 5.5 percent (Opus 4.8) to 2.0 percent"
- [G15] Defeating Prompt Injections by Design (CaMeL)｜Debenedetti, Shumailov 等（Google DeepMind 等，arXiv 2503.18813）｜2025-03-24（v2 2025-06-24）｜A｜https://arxiv.org/abs/2503.18813｜视角 1,4,5
  摘录："the untrusted data retrieved by the LLM can never impact the program flow"；"solving 77% of tasks with provable security (compared to 84% with an undefended system) in AgentDojo"
  摘录："We demonstrate effectiveness of CaMeL by solving 77% of tasks with provable security (compared to 84% with an undefended system) in AgentDojo."
  摘录："CaMeL requires only 2.82× more input and 2.73× more output tokens than native tool-calling"
  摘录："the number of successful attacks for Gemini 2.5 Pro drops from 300 without to 0 with CaMeL."
  摘录："No, prompt injection attacks are not fully solved. … Importantly, CaMeL suffers from users needing to codify and specify security policies and maintain them."
  摘录："This can lead to user fatigue, where users become desensitized to security prompts and may inadvertently approve malicious actions"
  摘录："explicitly extracts the control and data flows from the (trusted) query"；"solving 77% of tasks with provable security"（无防御系统为 84%）
- [G16] Meta-SecAlign: Training LLMs against Prompt Injection for Robust Agents｜Meta FAIR 等（arXiv 2507.02735）｜2025-07-03（v4 2026-09-28）｜A｜https://arxiv.org/abs/2507.02735｜视角 1,4
  摘录："we find that SecAlign actually suffers from significant utility degradation"
  摘录："we find that SecAlign actually suffers from significant utility degradation, especially in agentic tasks where the threat of prompt injection is prominent."
- [G17] OpenAI says AI browsers may always be vulnerable to prompt injection attacks｜TechCrunch（转述 OpenAI Atlas 加固博客）｜2025-12-22｜B｜https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/｜视角 1,4
  摘录："Prompt injection, much like scams and social engineering on the web, is unlikely to ever be fully 'solved,'"
  摘录（OpenAI 原话，经转引）："Prompt injection, much like scams and social engineering on the web, is unlikely to ever be fully 'solved,'"
  摘录（OpenAI 原话，经转引）："Wide latitude makes it easier for hidden or malicious content to influence the agent, even when safeguards are in place"
- [G18] The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections｜Nasr, Carlini 等（OpenAI/Anthropic/Google DeepMind 等，arXiv 2510.09023；USENIX Security 2026）｜2025-10-10｜A｜https://arxiv.org/abs/2510.09023｜视角 1,4
  摘录："the majority of defenses originally reported near-zero attack success rates"；"Our adaptive attacks continue to bypass both the target model and every detector we evaluated"；"stacking additional detectors does not resolve the underlying robustness problem"；"success on static evaluations provides only a false sense of security"
  摘录："we bypass 12 recent defenses (based on a diverse set of techniques) with attack success rate above 90% for most; importantly, the majority of defenses originally reported near-zero attack success rates."
  摘录："Our search-based adaptive attack (with the detector's confidence score and detection flag fed back to the attacker) achieves ASR of >90% against Protect AI, PromptGuard, and Model Armor (with Gemini-2.5 Pro as the base model). PIGuard is somewhat more resistant but still reaches 71% ASR."
  摘录："using the benchmark's static attacks, observed attack success rates (ASR) as low as 1%. However, when we applied our search-based adaptive attack, the ASR is above 95% for both defenses."
  摘录："MetaSecAlign … reports an attack success rate (ASR) of 2% on the static AgentDojo benchmark. We re-evaluated this defense … and achieved a 96% ASR."
  摘录："the search attack succeeds 69% of the time whereas the red-teaming humans collectively succeeds 100% of the time"
- [G19] Adaptive Attacks Break Defenses Against Indirect Prompt Injection Attacks on LLM Agents｜Zhan 等（arXiv 2503.00061，NAACL 2025 Findings）｜2025-02-27｜A｜https://arxiv.org/abs/2503.00061｜视角 1
  摘录："evaluate eight different defenses and bypass all of them using adaptive attacks"；"consistently achieving an attack success rate of over 50%"
- [G20] （仅作线索）好帮手 AI 的悖论 / 智能体管道提示注入防御｜tianpan.co 中文博客｜2026-04/05｜C｜https://tianpan.co/zh/blog/2026-04-18-prompt-injection-agentic-pipelines-defense｜视角 1
  备注：中文解读，转述 Willison 的三要素和"无参数化查询等价物"观点，结论已回溯到 S1、S2、S6。未找到国内头部安全团队（腾讯朱雀、奇安信、绿盟等）就此主题发表的可靠一手解读。
- [G21] Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection｜Greshake, Abdelnabi, Mishra, Endres, Holz, Fritz（arXiv 2302.12173 / AISec'23）｜2023-02-23（v2 2023-05-05）｜A｜https://arxiv.org/abs/2302.12173｜视角 2
  摘录："Passive methods (by retrieval)" / "Active methods (e.g., emails)" / "User-driven injections" / "Hidden injections"；"any prompts/instructions written on a page (while being invisible to the user) can be effectively injected and affect the model"；"data theft, worming, information ecosystem contamination"
- [G22] LLM01:2025 Prompt Injection｜OWASP GenAI Security Project｜2024-11（2025 版）｜A｜https://genai.owasp.org/llmrisk/llm01-prompt-injection/｜视角 2,5
  摘录："Indirect prompt injections occur when an LLM accepts input from external sources, such as websites or files."；"These inputs can affect the model even if they are imperceptible to humans"；"Providing unauthorized access to functions available to the LLM"
  摘录："Require human approval for high-risk actions"；"Segregate and identify external content: Separate and clearly denote untrusted content to limit its influence on user prompts."
- [G23] MITRE ATLAS 数据（ATLAS.yaml v5.6.0，GitHub mitre-atlas/atlas-data，文件头标注已 deprecated）｜MITRE｜各技术条目修改日期 2023-10 至 2025-11｜A｜https://github.com/mitre-atlas/atlas-data （raw: https://raw.githubusercontent.com/mitre-atlas/atlas-data/main/dist/ATLAS.yaml）｜视角 2
  摘录：AML.T0051.001 "An adversary may inject prompts indirectly via separate data channel ingested by the LLM such as include text or multimedia pulled from databases or websites."；AML.T0068 "small text, text colored the same as the background, or hidden HTML elements"；AML.T0080.000 "an adversary can inject memories via Direct or Indirect Prompt Injection"；AML.T0061 "This allows the prompt to propagate to other LLMs and persist on the system."
- [G24] OWASP Top 10 for Agentic Applications for 2026（PDF）｜OWASP GenAI Security Project – Agentic Security Initiative｜2025-12-09｜A｜https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/｜视角 2
  摘录："agents and the underlying model cannot reliably distinguish instructions from related content."；"Unlike LLM01:2025, which focuses on altering a single model response, ASI01 captures the broader agentic impact"；"Tool-descriptor injection: An attacker embeds hidden instructions or malicious payloads into a tool's metadata or MCP/agent-card"
- [G25] MCP Security Notification: Tool Poisoning Attacks｜Invariant Labs｜2025-04-01｜B（一手研究博客）｜https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks｜视角 2
  摘录："malicious instructions are embedded within MCP tool descriptions that are invisible to users but visible to AI models"；"a malicious server can change the tool description after the client has already approved it"
- [G26] GitHub MCP Exploited: Accessing private repositories via MCP｜Invariant Labs｜2025-05-26｜B｜https://invariantlabs.ai/blog/mcp-github-vulnerability｜视角 2,3
  摘录："The vulnerability allows an attacker to hijack a user's agent via a malicious GitHub Issue"；"coerce it into leaking data from private repositories"
  摘录："this is not a flaw in the GitHub MCP server code itself"；"a fundamental architectural issue that must be addressed at the agent system level"；"GitHub alone cannot resolve this vulnerability through server-side patches"
- [G27] Hiding and Finding Text with Unicode Tags｜Johann Rehberger (Embrace The Red)｜2024-01-14｜B｜https://embracethered.com/blog/posts/2024/hiding-and-finding-text-with-unicode-tags/｜视角 2
  摘录："The Tags Unicode Block mirrors ASCII"；"because it is often not rendered in the UI, the special text remains unnoticable to users"；"allows smuggling of data in plain sight!"
- [G28] Defending LLM applications against Unicode character smuggling｜AWS Security Blog｜2025-09-30｜A｜https://aws.amazon.com/blogs/security/defending-llm-applications-against-unicode-character-smuggling/｜视角 2
  摘录："a specific range of characters spanning from U+E0000 to U+E007F"；"can read, interpret, and act on these hidden characters placed with Unicode tags"
- [G29] Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems｜Lee & Tiwari（arXiv 2410.07283）｜2024-10-09｜A｜https://arxiv.org/abs/2410.07283｜视角 2
  摘录："a novel attack where malicious prompts self-replicate across interconnected agents"
- [G30] PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of LLMs｜Zou et al.（USENIX Security 2025）｜2024-02-12（v3 2024-08-13）｜A｜https://arxiv.org/abs/2402.07867｜视角 2
  摘录："PoisonedRAG could achieve a 90% attack success rate when injecting five malicious texts"
- [G31] Memory Injection Attacks on LLM Agents via Query-Only Interaction（MINJA）｜arXiv 2503.03704｜2025-03-05（v5 2026-02-12）｜A｜https://arxiv.org/abs/2503.03704｜视角 2
  摘录："The attacker injects malicious records into the memory bank by only interacting with the agent via queries"
- [G32] Invitation Is All You Need: Hacking Gemini｜SafeBreach Labs（Nassi, Cohen, Yair）｜2025-08-06｜B｜https://www.safebreach.com/blog/invitation-is-all-you-need-hacking-gemini/｜视角 2
  摘录："simply by sending them a Google calendar invite"；"Remotely control a victim's home appliances (e.g., connected windows, boiler, lights)"；"Exfiltrate a victim's emails"
- [G33] Agentic Browser Security: Indirect Prompt Injection in Perplexity Comet｜Brave｜2025-08-20｜B｜https://brave.com/blog/comet-prompt-injection/｜视角 2,3
  摘录："the prompt injection instructions hidden behind the spoiler tag"；"Exfiltrate both the email address and the OTP by replying to the original Reddit comment."
  摘录："feeds a part of the webpage directly to its LLM without distinguishing between the user's instructions and untrusted content"；"Unable to distinguish between the content it should summarize and instructions it should not follow, the AI treats everything as user requests."；"Perplexity still hasn't fully mitigated the kind of attack described here."
- [G34] Fooling AI Agents: Web-Based Indirect Prompt Injection Observed in the Wild｜Palo Alto Networks Unit 42｜2026-03-03｜A（一手遥测数据）｜https://unit42.paloaltonetworks.com/ai-agent-prompt-injection/｜视角 2
  摘录："Our research identified 22 distinct techniques attackers used in the wild to put together payloads"；"Setting font-size: 0px and line-height: 0 to shrink text until it physically disappears"；"To our knowledge, this is the first reported detection of a real-world example of malicious IDPI"
- [G35] AI threats in the wild: The current state of prompt injections on the web｜Google（Brunner, Liu, Pande）｜2026-04-23｜A｜https://blog.google/security/prompt-injections-web/｜视角 2
  摘录："We saw a relative increase of 32% in the malicious category between November 2025 and February 2026."；"While the observed activity suggests limited sophistication, this might be only part of the bigger picture."
- [G36] EchoLeak: The First Real-World Zero-Click Prompt Injection Exploit in a Production LLM System｜arXiv 2509.10540（AAAI Fall Symposium 2025）｜2025-09-06｜A｜https://arxiv.org/abs/2509.10540｜视角 2,3,4
  摘录："a zero-click prompt injection vulnerability in Microsoft 365 Copilot"（Aim Security 原博客返回 403，未能抓取）
  摘录："carefully phrased to evade detection, as though it was written as a normal request to the human recipient"；"sidestepped this by exploiting reference-style links, instead of inline syntax"；"Microsoft deployed a server-side fix in May 2025"；"Microsoft stated that no customer action was required and there was no evidence of in-the-wild exploitation"
  摘录："By chaining multiple bypasses-evading Microsofts XPIA (Cross Prompt Injection Attempt) classifier, circumventing link redaction with reference-style Markdown, exploiting auto-fetched images, and abusing a Microsoft Teams proxy allowed by the content security policy"
- [G37] Spyware Injection Into Your ChatGPT's Long-Term Memory (SpAIware)｜Johann Rehberger｜2024-09-20｜B｜https://embracethered.com/blog/posts/2024/chatgpt-macos-app-persistent-data-exfiltration/｜视角 2
  摘录："Through prompt injection from untrusted data, attackers could insert long-term persistent spyware into ChatGPT's memory."；"continuous data exfiltration of any information the user typed"
- [G38] Hacking Gemini's Memory with Prompt Injection and Delayed Tool Invocation｜Johann Rehberger｜2025-02-10｜B｜https://embracethered.com/blog/posts/2025/gemini-memory-persistence-prompt-injection/｜视角 2
  摘录："Delayed Tool Invocation just means that the attacker "pollutes" the chat context with instructions and a trigger action"；"Gemini is tricked, and it saves the attacker's chosen information to long-term memory"
- [G39] GitHub Copilot: Remote Code Execution via Prompt Injection (CVE-2025-53773)｜Johann Rehberger｜2025-08-12｜B｜https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/｜视角 2,3
  摘录："a prompt injection planted in a source code file, web page, GitHub issue"；"\"chat.tools.autoApprove\": true"
  摘录："can create and write to files in the workspace without user approval"；"The edits are immediately persistent, they are not in-memory as a diff to review."；"a not uncommon design flaw in agentic systems"；"With the August Patch Tuesday release this is now fixed."
- [G40] CamoLeak: Critical GitHub Copilot Vulnerability Leaks Private Source Code｜Legit Security（Omer Mayraz）｜2025-10-08（更新 2026-02-12）｜B｜https://www.legitsecurity.com/blog/camoleak-critical-github-copilot-vulnerability-leaks-private-source-code｜视角 2
  摘录："I tried the same prompt but this time as a hidden comment inside the PR description."；"GitHub fixed it by disabling image rendering in Copilot Chat completely."
- [G41] ForcedLeak: AI Agent Risks Exposed in Salesforce Agentforce｜Noma Security｜2025-09-25｜B｜https://noma.security/blog/forcedleak-agent-risks-exposed-in-salesforce-agentforce/｜视角 2
  摘录："The attacker places malicious content in a web form, which gets stored in the system's database."；"The domain my-salesforce-cms.com was whitelisted but had expired and become available for purchase"
- [G42] Cato CTRL PoC attack targeting Atlassian's MCP（经 Simon Willison 转引四步链路；Cato 原文抓取为空）｜Cato Networks / simonwillison.net｜2025-06-19｜B｜https://simonwillison.net/2025/Jun/19/atlassian-prompt-injection-mcp/ （原文 https://www.catonetworks.com/blog/cato-ctrl-poc-attack-targeting-atlassians-mcp/）｜视角 2
  摘录："A threat actor (acting as an external user) submits a malicious support ticket."；"A prompt injection payload in the malicious support ticket is executed with internal privileges."
- [G43] AI Agent-to-Agent Discovery Prompt Injection (ServiceNow Now Assist)｜AppOmni AO Labs（Aaron Costello）｜2025-11-19｜B｜https://appomni.com/ao-labs/ai-agent-to-agent-discovery-prompt-injection/｜视角 2
  摘录："Through second-order prompt injection, an attacker can redirect a benign task assigned to an innocuous agent"；"all while the ServiceNow prompt injection protection feature was enabled"
- [G44] Weaponizing image scaling against production AI systems｜Trail of Bits｜2025-08-21｜B｜https://blog.trailofbits.com/2025/08/21/weaponizing-image-scaling-against-production-ai-systems/｜视角 2
  摘录："when scaled, these images can reveal prompt injections that are not visible at full resolution"；"exfiltrates user data stored in Google Calendar"
- [G45] Unseeable prompt injections in screenshots: more vulnerabilities in Comet and other AI browsers｜Brave｜2025-10-21（更新 2025-10-31）｜B｜https://brave.com/blog/unseeable-prompt-injections/｜视角 2,3
  摘录："Malicious instructions embedded as nearly-invisible text within the image"；"simply asking the browser to go to a website causes the browser to send the website's content to their LLM"
  摘录："Malicious instructions embedded as nearly-invisible text within the image are processed as commands"；"indirect prompt injection is not an isolated issue, but a systemic challenge"；"isolate agentic browsing from regular browsing"
- [G46] New Vulnerability in GitHub Copilot and Cursor: How Hackers Can Weaponize Code Agents (Rules File Backdoor)｜Pillar Security｜2025-03-18｜B｜https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents｜视角 2
  摘录："invisible Unicode characters such as zero-width joiners and bidirectional text markers"
- [G47] Model Context Protocol has prompt injection security problems｜Simon Willison｜2025-04-09｜B｜https://simonwillison.net/2025/Apr/9/mcp-prompt-injection/｜视角 2
  摘录："MCP tools can mutate their own definitions after installation."；"With multiple servers connected to the same agent, a malicious one can override or intercept calls made to a trusted one."
- [G48] MCP Specification 2025-06-18 – Server/Tools｜Model Context Protocol｜2025-06-18｜A｜https://modelcontextprotocol.io/specification/2025-06-18/server/tools｜视角 2
  摘录："clients MUST consider tool annotations to be untrusted unless they come from trusted servers."；"When the list of available tools changes, servers that declared the listChanged capability SHOULD send a notification"
- [G49] Here Comes The AI Worm: Unleashing Zero-click Worms that Target GenAI-Powered Applications（Morris II）｜Cohen, Bitton, Nassi（arXiv 2403.02817）｜2024-03-05（v2 2025-01-30）｜A｜https://arxiv.org/abs/2403.02817｜视角 2
  摘录："an attacker can initiate a computer worm-like chain reaction that we call Morris-II"
- [G50] OpenAI says prompt injections may never be fully solved（报道转引 OpenAI 官方博客 "Continuously hardening ChatGPT Atlas against prompt injection"，原文抓取 403）｜Fortune（Beatrice Nolan）｜2025-12-23｜B｜https://fortune.com/2025/12/23/openai-ai-browser-prompt-injections-cybersecurity-hackers/｜视角 2
  摘录：OpenAI 称提示注入"much like scams and social engineering on the web, is unlikely to ever be fully 'solved.'"；"agent mode" in ChatGPT Atlas "expands the security threat surface."
- [G51] CVE-2025-32711 "M365 Copilot Information Disclosure Vulnerability"｜Microsoft（CNA）/ CVE.org｜2025-06-11｜A｜https://cveawg.mitre.org/api/cve/CVE-2025-32711 （MSRC 页面：https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-32711 ）｜视角 3
  摘录："Ai command injection in M365 Copilot allows an unauthorized attacker to disclose information over a network."；CVSS 3.1 9.3，"CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N/E:U/RL:O/RC:C"；CWE-74
- [G52] CVE-2025-53773 "GitHub Copilot and Visual Studio Remote Code Execution Vulnerability"｜Microsoft（CNA）/ CVE.org｜2025-08-12｜A｜https://cveawg.mitre.org/api/cve/CVE-2025-53773｜视角 3
  摘录："Improper neutralization of special elements used in a command ('command injection') in GitHub Copilot and Visual Studio allows an unauthorized attacker to execute code locally."；CVSS 7.8，"AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H/E:U/RL:O/RC:C"
- [G53] Breaking down 'EchoLeak'…｜Simon Willison's Weblog｜2025-06-11｜B（逐段引用 Aim Labs 原文 https://www.aim.security/lp/aim-labs-echoleak-blogpost ，该原文本次访问返回 403）｜https://simonwillison.net/2025/Jun/11/echoleak/｜视角 3
  摘录："they had forgotten to implement that filter for Markdown's other lesser-known link format"；"the CSP allow-list is pretty wide, and included `*.teams.microsoft.com`"；"It turns out that domain hosted an open redirect URL, which is all that's needed."
- [G54] GitHub MCP exploited: Accessing private repositories via MCP｜Simon Willison's Weblog｜2025-05-26｜B｜https://simonwillison.net/2025/May/26/github-mcp-exploited/｜视角 3
  摘录："the result of an LLM acting on this issue is a new PR which exposes the names of those private repos!"；"It turns out GitHub's MCP combines all three ingredients in a single package!"
- [G55] The GitHub MCP Server adds support for tool-specific configuration, and more｜GitHub Changelog｜2025-12-10｜A｜https://github.blog/changelog/2025-12-10-the-github-mcp-server-adds-support-for-tool-specific-configuration-and-more｜视角 3
  摘录："Lockdown mode ensures that only content from trusted collaborators with push access is surfaced"；"comprehensive content sanitization is now enabled by default to protect against prompt injection attacks."
- [G56] CVE-2026-48529 "GitHub MCP Server: Lockdown mode singleton in HTTP server causes cross-user GraphQL client confusion"｜GitHub（CNA）/ CVE.org｜2026-06-26｜A｜https://cveawg.mitre.org/api/cve/CVE-2026-48529 （GHSA-pjp5-fpmr-3349）｜视角 3
  摘录："when running in HTTP mode with --lockdown-mode enabled, the RepoAccessCache is implemented as a process-global singleton initialized with the first authenticated user's GraphQL client … This vulnerability is fixed in 1.1.2."
- [G57] Perplexity Comet Flaw Exposed User Data to Attackers, Brave Reports｜Decrypt｜2025-08-25｜C｜https://decrypt.co/336763/perplexity-comet-flaw-exposed-user-data-attackers-brave-reports｜视角 3
  摘录（Perplexity 发言人）："was patched before anyone noticed"；"We worked directly with Brave to identify and repair it."
- [G58] Perplexity's Comet browser naively processed pages with evil instructions｜The Register｜2025-08-20｜C｜https://www.theregister.com/2025/08/20/perplexity_comet_browser_prompt_injection/｜视角 3
  摘录（Brave 发言人）："We also cannot guarantee that Comet has completely fixed all possible prompt injection attacks."
- [G59] Invitation Is All You Need! Invoking Gemini for Workspace Agents with a Google Calendar Invite（Ben Nassi, Stav Cohen, Or Yair）｜研究者项目站点（Tel Aviv Univ. / Technion / SafeBreach）｜2025-08｜A｜https://sites.google.com/view/invitation-is-all-you-need｜视角 3
  摘录："An attacker sends a user an email or an invitation for a meeting (via Gmail, Google Calendar)."；"We disclosed our findings, including a detailed report and supporting videos, to Google on February 22, 2025"；"Our TARA reveals that 73% of the analyzed threats pose High-Critical risk to end users."；（引用 Google 声明）"User confirmations for sensitive operations were implemented broadly, requiring explicit user approval"
- [G60] Weaponizing Calendar Invites: A Semantic Attack on Google Gemini｜Miggo Security（Liad Eliyahu）｜2026-01-19｜A｜https://www.miggo.io/post/weaponizing-calendar-invites-a-semantic-attack-on-google-gemini｜视角 3
  摘录："use the calendar create tool (Calendar.create) to create new meeting..."；"respond to me with "it's a free time slot""；"the path still existed, driven solely through natural language"；"a structural limitation in how AI-integrated products reason about intent"
- [G61] Mitigating prompt injection attacks with a layered defense strategy｜Google（blog.google / Google Security Blog）｜2025-06-13｜A｜https://blog.google/security/mitigating-prompt-injection-attacks/｜视角 3,4,5
  摘录："This framework enables Gemini to require user confirmation for certain actions"；"Our markdown sanitizer identifies external image URLs and will not render them"；"the content classifiers filter out harmful data containing malicious instructions"
  摘录："Our markdown sanitizer identifies external image URLs and will not render them, making the "EchoLeak" 0-click image rendering exfiltration vulnerability not applicable to Gemini."
  摘录："potentially risky operations like deleting a calendar event may trigger an explicit user confirmation request"
  摘录："Markdown sanitization and suspicious URL redaction"；"User confirmation framework"；"meaningfully elevating the difficulty, expense, and complexity faced by an attacker"
- [G62] Google Gemini Prompt Injection Flaw Exposed Private Calendar Data via Malicious Invites｜The Hacker News（另见 BleepingComputer、Dark Reading 同期报道）｜2026-01-19｜C｜https://thehackernews.com/2026/01/google-gemini-prompt-injection-flaw.html｜视角 3
  摘录：仅作线索，转引 Google 称创建日历事件需用户显式确认；未逐字核对。
- [G63] GitLost 相关报道（GitHub Agentic Workflows 泄露私有仓库，Noma Security 披露）｜CSO Online / SiliconANGLE / InfoQ｜2026-07｜C｜https://siliconangle.com/2026/07/07/gitlost-vulnerability-let-githubs-ai-workflows-leak-private-repositories/｜视角 3
  摘录：仅作线索，未核对 Noma 原文，不逐字引用。
- [G64] Supabase MCP can leak your entire SQL database｜General Analysis｜2025-07-08（页面标注 "Reviewed 6 Sept 2026"）｜A｜https://www.generalanalysis.com/blog/supabase-mcp-blog｜视角 3
  摘录："The cursor assistant operates the Supabase database with elevated access via the service_role"；"The weak link: the IDE assistant ingests untrusted customer text and holds service_role privileges."；"A prompt injection filter can flag suspicious content, but it cannot grant or restrict database permissions."
- [G65] Supabase MCP can leak your entire SQL database｜Simon Willison's Weblog｜2025-07-06｜B｜https://simonwillison.net/2025/Jul/6/supabase-mcp-lethal-trifecta/｜视角 3
  摘录："The Supabase MCP, like the GitHub MCP before it, can provide all three from a single MCP."；（引 Supabase 文档）"We recommend these settings to prevent the agent from making unintended changes to your database."
- [G66] LlamaFirewall: An open source guardrail system for building secure AI agents｜Meta｜2025-05-06｜A｜https://arxiv.org/abs/2505.03574｜视角 4
  摘录："The baseline AgentDojo Eval set without any defense exhibited an attack success rate (ASR) of 17.6% and a task utility of 47.7%. Applying PromptGuard V2 86M alone reduced the ASR to 7.5%, a 57% drop, while maintaining utility at 47.0%"
  摘录："The combined configuration PromptGuard + AlignmentCheck delivered the best defensive performance, reducing ASR to 1.75%"
- [G67] InjecGuard: Benchmarking and Mitigating Over-defense in Prompt Injection Guardrail Models｜Li et al.｜2024-10-30｜A｜https://arxiv.org/abs/2410.22770｜视角 4
  摘录："Our results show that state-of-the-art models suffer from over-defense issues, with accuracy dropping close to random guessing levels (60%)."
- [G68] Bypassing Meta's LLaMA Classifier: A Simple Jailbreak｜Robust Intelligence（现属 Cisco）｜2024-07-29｜B｜https://blogs.cisco.com/security/bypassing-metas-llama-classifier-a-simple-jailbreak｜视角 4
  摘录："the model's performance plummeted to 0.2% accuracy, misclassifying 449 out of 450 prompts as benign and demonstrating a complete circumvention of the model's safety mechanisms (Success Rate of 99.8%)."
- [G69] AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents｜Debenedetti et al., ETH Zurich｜2024-06-19｜A｜https://arxiv.org/abs/2406.13352｜视角 4
  摘录（表 5，GPT-4o）："Defenses No defense Delimiting PI detector Repeat prompt Tool filter … Targeted ASR 57.69% 41.65% 7.95% 27.82% 6.84%"
  摘录："The prompt injection detector has too many false positives, however, and significantly degrades utility. Repeating the user prompt after a tool call is a reasonable defense for our attack, but it is unlikely to withstand adaptive attacks"
  摘录："This defense fails, however, when the list of tools to use cannot be planned in advance … or when the tools required to solve the task are also sufficient to carry out the attack (this is true for 17% of our test cases)."
- [G70] LLMail-Inject: A Dataset from a Realistic Adaptive Prompt Injection Challenge｜Abdelnabi, Fay et al.（Microsoft/ISTA/ETH）｜2025-06-11｜A｜https://arxiv.org/abs/2506.09956｜视角 4
  摘录："Only 3,018 submissions (0.8%) resulted in successful end-to-end attacks."
  摘录："We also see that spotlighting can be more effective than some detection defenses alone, such as Prompt Shield. In addition, stacking all defenses provides a significant improvement."
  摘录："in Phase-2, using all defenses combined with GPT-4o did not result in any successful attacks."
- [G71] The Dual LLM pattern for building AI assistants that can resist prompt injection｜Simon Willison｜2023-04-25（2025-04-11 补充更新）｜B｜https://simonwillison.net/2023/Apr/25/dual-llm-pattern/｜视角 4
  摘录："The Privileged LLM only ever sees those variable names."
  摘录："You may have noticed something about this proposed solution: it's pretty bad! Building AI assistants in this way is likely to result in a great deal more implementation complexity and a degraded user experience."
  摘录："The social engineering aspects also mean that this isn't a 100% reliable solution."
- [G72] CaMeL offers a promising new direction for mitigating prompt injection attacks｜Simon Willison｜2025-04-11｜B｜https://simonwillison.net/2025/Apr/11/camel/｜视角 4
  摘录："in application security 99% is a failing grade"
  摘录："With the Dual LLM pattern the P-LLM delegates the task of finding Bob's email address to the Q-LLM—but the Q-LLM is still exposed to potentially malicious instructions."
- [G73] Securing AI Agents with Information-Flow Control (FIDES)｜Costa, Köpf, Kolluri, Paverd, Russinovich, Salem, Tople et al., Microsoft｜2025-05-29（v2 2025-09-03）｜A｜https://arxiv.org/abs/2505.23643｜视角 4
  摘录："With policy checks enabled, Fides stops all prompt injection attacks in AgentDojo. Without policy checks, all planners, including Fides, succumb to practical PIAs."
  摘录："Fides completes on average about 16% more tasks than a basic planner. With further prompt tuning, this rises to 24%"
- [G74] Adaptive Evaluation of Out-of-Band Defenses Against Prompt Injection in LLM Agents｜arXiv 预印本｜2026-06-25｜A（预印本，未经同行评审）｜https://arxiv.org/abs/2606.26479｜视角 4
  摘录："we warn that every one of them is validated only on static benchmarks"
  摘录："Progent cut mean attack success roughly sixfold (25.8% to 4.2%), and a hand-crafted adaptive attack did not raise it (2.6%). This is one small-scale data point on a weak model with a single black-box attack template"
- [G75] Can CaMeLs Talk? Securing Multi-Agent Systems Against Indirect Prompt Injection Attacks｜arXiv 预印本｜2026-10-05｜A（预印本）｜https://arxiv.org/abs/2610.05640｜视角 4
  摘录："We find that CaMeL's guarantees do not compose."
  摘录："multi-CaMeL reduces attack success rate (ASR) to 0.0%, compared with 0.2% for individual-agent CaMeL and 12.9% with no CaMeL."
- [G76] CaMeLs Can Use Computers Too: System-level Security for Computer Use Agents｜arXiv 预印本｜2026-01-14（v3）｜A（预印本）｜https://arxiv.org/abs/2601.09923｜视角 4
  摘录："we show that additional measures are needed to defend against Branch Steering attacks, where adversaries deceive the perception model into routing execution down attacker-preferred branches of the plan"
- [G77] Agent Data Injection Attacks are Realistic Threats to AI Agents｜arXiv 预印本｜2026-07-06｜A（预印本）｜https://arxiv.org/abs/2607.05120｜视角 4
  摘录："Despite the similar impact, ADI remains underexplored and easily bypasses existing IPI defenses."
- [G78] Confuse the Model, Control the Flow: … Privacy Leakage from LLM Agents with Information Flow Control (FLOWSEAL)｜arXiv 预印本｜2026-09-12｜A（预印本）｜https://arxiv.org/abs/2609.14003｜视角 4
  摘录："whenever enforcement is a judgment the LLM makes over the same conversational context an adversary controls, the enforcement mechanism and the attack surface coincide."
  摘录："FLOWSEAL reduces leak rates to near zero (e.g., 52.2% to 0.5% against Collaborative Workspace Lure)"
- [G79] Beyond permission prompts: making Claude Code more secure and autonomous｜Anthropic Engineering｜2025-10-20｜A｜https://www.anthropic.com/engineering/claude-code-sandboxing｜视角 4,5
  摘录："In our internal usage, we've found that sandboxing safely reduces permission prompts by 84%."
  摘录："Constantly clicking "approve" slows down development cycles and can lead to 'approval fatigue', where users might not pay close attention to what they're approving"
  摘录："effective sandboxing requires both filesystem and network isolation."
  摘录："sandboxing safely reduces permission prompts by 84%"；"effective sandboxing requires both filesystem and network isolation"
- [G80] Claude Pirate: Abusing Anthropic's File API For Data Exfiltration｜Johann Rehberger（Embrace The Red）｜2025（URL 路径为 2025；SecurityWeek 等媒体于 2025-11 报道；页面具体日期未核实）｜B｜https://embracethered.com/blog/posts/2025/claude-abusing-network-access-and-anthropic-api-for-data-exfiltration/｜视角 4
  摘录："At second glance I stopped at the first entry, api.anthropic.com, to think things through adversarially."
  摘录："The upload will not happen to the user's Anthropic account, but to the attackers, because it's using the attacker's ANTHROPIC_API_KEY here!"
- [G81] HITL Dialog Forging (aka Lies-in-the-Loop)｜OWASP 社区页（Ori Ron、Dor Tumarkin，Checkmarx Zero）｜2025（具体日期未核实）｜B｜https://owasp.org/www-community/attacks/Lies_in_the_Loop｜视角 4
  摘录："The LITL attack exploits the fact that HITL dialogs, which are usually the only feedback users see, are generated based on context that an attacker can control through indirect prompt injection."
- [G82] InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated LLM Agents｜Zhan et al., UIUC｜2024-03-05｜A｜https://arxiv.org/abs/2403.02691｜视角 4
  摘录："InjecAgent comprises 1,054 test cases covering 17 different user tools and 62 attacker tools. … with ReAct-prompted GPT-4 vulnerable to attacks 24% of the time."
- [G83] WASP: Benchmarking Web Agent Security Against Prompt Injection Attacks｜Evtimov et al., Meta｜2025-04-22｜A｜https://arxiv.org/abs/2504.18575｜视角 4
  摘录："while attacks partially succeed in up to 86% of the case, even state-of-the-art agents often struggle to fully complete the attacker goals -- highlighting the current state of security by incompetence."
- [G84] Security Challenges in AI Agent Deployment: Insights from a Large Scale Public Competition (ART)｜Gray Swan 等｜2025-07-28｜A｜https://arxiv.org/abs/2507.20526｜视角 4
  摘录："Nearly all agents exhibit policy violations for most behaviors within 10-100 queries, with high attack transferability across models and tasks."
- [G85] Indirect Prompt Injections: Are Firewalls All You Need, or Stronger Benchmarks?｜arXiv｜2025-10-06｜A｜https://arxiv.org/abs/2510.05244｜视角 4
  摘录："Our analysis also reveals critical limitations in these existing benchmarks, including flawed success metrics, implementation bugs, and most importantly, weak attacks, hindering progress."
- [G86] Evaluating the Robustness of Large Language Model Safety Guardrails Against Adversarial Attacks｜arXiv｜2025-11-27｜A（预印本）｜https://arxiv.org/abs/2511.22047｜视角 4
  摘录："all models showed substantial performance degradation on unseen prompts, with Qwen3Guard dropping from 91.0% to 33.8%"
- [G87] MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents｜Zhu et al.｜2025-02-07｜A｜https://arxiv.org/abs/2502.05174｜视角 4
  摘录："We identify an attack if the actions generated in the original and masked executions are similar."（后被 [S1] 列为可被自适应攻击绕过的防御之一）
- [G88] Agent Security Bench (ASB)｜Zhang et al.｜2024-10-03｜A｜https://arxiv.org/abs/2410.02644｜视角 4
  摘录："with the highest average attack success rate of 84.30%, but limited effectiveness shown in current defenses"
- [G89] OWASP Top 10 for Agentic Applications 2026｜OWASP GenAI Security Project, Agentic Security Initiative｜2025-12（Version 2026）｜A｜genai.owasp.org（PDF；资源页准确路径未逐一核对）｜视角 5
  摘录："Treat all natural-language inputs (e.g., user-provided text, uploaded documents, retrieved content) as untrusted."；"Policy Enforcement Middleware (“Intent Gate”). Treat LLM or planner outputs as untrusted."；"provide plain-language risk summary (not model-generated rationales)"；"deploying agentic behavior where it is not needed expands the attack surface without adding value."
- [G90] NIST AI 100-2e2025 Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations｜NIST｜2025-03｜A｜https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-2e2025.pdf｜视角 5
  摘录："Because current mitigations do not offer full protection against all attacker techniques, application designers may design systems with the assumption that prompt injection attacks are possible if a model is exposed to untrusted input sources, such as by using multiple LLMs with different permissions"
- [G91] Technical Blog: Strengthening AI Agent Hijacking Evaluations｜NIST CAISI｜2025-01-17（2025-12-19 更新）｜A｜https://www.nist.gov/node/1872381｜视角 5
  摘录："Testing the success of attacks on multiple attempts may yield more realistic evaluation results."；"analyze task-specific attack performance in addition to aggregate performance"
- [G92] Insights into AI Agent Security from a Large-Scale Red-Teaming Competition｜NIST CAISI｜2026-03-23｜A｜https://www.nist.gov/blogs/caisi-research-blog/insights-ai-agent-security-large-scale-red-teaming-competition｜视角 5
  摘录："at least one successful attack was found against all of the target frontier models"
- [G93] Piloting Claude for Chrome｜Anthropic｜2025-08-25（2025-11-24、2025-12-18 更新）｜A｜https://claude.com/blog/claude-for-chrome｜视角 5
  摘录："Claude asks users before taking high-risk actions like publishing, purchasing, or sharing personal data."；"Browser use without our safety mitigations showed a 23.6% attack success rate when deliberately targeted by malicious actors."
- [G94] How we built Claude Code auto mode: a safer way to skip permissions｜Anthropic Engineering｜2026-03-25｜A｜https://www.anthropic.com/engineering/claude-code-auto-mode｜视角 5
  摘录："Claude Code users approve 93% of permission prompts."；"It is not a drop-in replacement for careful human review on high-stakes infrastructure."
- [G95] How we contain Claude across products｜Anthropic Engineering｜2026-05-25｜A｜https://www.anthropic.com/engineering/how-we-contain-claude｜视角 5
  摘录："Design for containment at the environment layer first, then steer behavior at the model layer."；"Every function reachable through any domain on an allowlist is now an attack surface."；"protection in the model layer will never be 100% effective, which is why it can't stand alone."
- [G96] Safety in building agents｜OpenAI 开发者文档｜未标日期（2026-10 访问）｜A｜https://developers.openai.com/api/docs/guides/agent-builder-safety｜视角 5
  摘录："injecting untrusted input directly into developer messages gives attackers the highest degree of control"；"always enable tool approvals so end users can review and confirm every operation, including reads and writes"
- [G97] Agent approvals & security（Codex 文档）｜OpenAI｜未标日期（2026-10 访问）｜A｜https://learn.chatgpt.com/docs/agent-approvals-security｜视角 5
  摘录："Defaults include no network access and write permissions limited to the active workspace."；"Prompt injection can cause the agent to fetch and follow untrusted instructions."
- [G98] OpenAI CISO Dane Stuckey on ChatGPT Atlas（转引 CISO 公开声明并附评论）｜Simon Willison's Weblog｜2025-10-22｜B（引述内容为 OpenAI 官方表态）｜https://simonwillison.net/2025/Oct/22/openai-ciso-on-atlas/｜视角 5
  摘录："prompt injection remains a frontier, unsolved security problem"；"We recommend this mode when you don't need to take action within your accounts."；（Willison 评论）"an unfair burden to place on almost any user"
  补充：OpenAI 2025-12 的 Atlas 加固博文原文访问返回 403，只见到 TechCrunch 等报道（https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/，C 级线索）。
- [G99] Architecting Security for Agentic Capabilities in Chrome｜Google Chrome Security（Nathan Parker）｜2025-12-08｜A｜https://security.googleblog.com/2025/12/architecting-security-for-agentic.html｜视角 5
  摘录："The User Alignment Critic runs after the planning is complete to double-check each proposed action."；"Read-writable origins are those on which the agent is allowed to actuate (e.g., click, type)."；"based on a deterministic check against a list of sensitive sites"
- [G100] Defend against agentic risks with multi-layered protections in Google Workspace Studio｜Google Workspace Blog｜2026-08-26｜A｜https://workspace.google.com/blog/identity-and-security/defend-against-agentic-risks-with-multi-layered-protections-in-google-workspace-studio｜视角 5
  摘录："Studio generates a dedicated OAuth Client ID that is restricted to a least privileged subset of the owner's permissions"；"any steps executed by Gemini are prohibited from referencing context in protected Drive files"
- [G101] Strengthen agent security with near-real-time protection in Microsoft Copilot Studio｜Microsoft Copilot Blog｜2025-09-08｜A｜https://microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/strengthen-agent-security-with-near-real-time-protection-in-microsoft-copilot-studio｜视角 5
  摘录："Copilot Studio includes default protections against both XPIA and user prompt injection attacks (UPIA)."；"If no response arrives in time, the agent assumes approval and continues."
- [G102] Security Best Practices｜Model Context Protocol 规范（draft 版）｜2026-10 访问（持续更新）｜A｜https://modelcontextprotocol.io/specification/draft/basic/security_best_practices｜视角 5
  摘录："MCP servers **MUST NOT** accept any tokens that were not explicitly issued for the MCP server."；"Consent abandonment: users decline dialogs listing excessive scopes"；"Execute MCP server commands in a sandboxed environment with minimal default privileges"
- [G103] Tools｜Model Context Protocol 规范 2025-11-25｜2025-11-25｜A｜https://modelcontextprotocol.io/specification/2025-11-25/server/tools｜视角 5
  摘录："For trust & safety and security, there **SHOULD** always be a human in the loop with the ability to deny tool invocations."；"Show tool inputs to the user before calling the server, to avoid malicious or accidental data exfiltration"；"clients **MUST** consider tool annotations to be untrusted unless they come from trusted servers."
- [G104] Threat modeling your generative AI workload to evaluate security risk｜AWS Security Blog｜2024-11-18｜A（超过 12 个月，仅用于方法论）｜https://aws.amazon.com/blogs/security/threat-modeling-your-generative-ai-workload-to-evaluate-security-risk｜视角 5
  摘录："You can also use a structured framework such as STRIDE to aid you in your thinking."；"Embed an indirect prompt injection in a webpage"
- [G105] Agentic AI Threat Modeling Framework: MAESTRO｜Cloud Security Alliance（Ken Huang）｜2025｜B（只读到检索摘要，未读原文）｜https://cloudsecurityalliance.org/articles/agentic-ai-threat-modeling-framework-maestro｜视角 5
  摘录：未获取原文逐字摘录。检索摘要称其为 7 层框架，建立在 STRIDE、PASTA、LINDDUN 之上。
- [G106] OWASP Agentic AI – Threats and Mitigations（T10 Overwhelming Human in the Loop）｜OWASP（经 HUMAN Security 等二手介绍）｜2025-02｜C（线索）｜https://humansecurity.com/learn/blog/agentic-ai-security-owasp-threats｜视角 5
  摘录：未获取 OWASP 原文逐字摘录。二手描述为 agent 产生超过人能审阅数量的审批请求，且可被攻击者故意放大。

## 编号对照表
| 笔记编号 | 总表编号 |
|---|---|
| 1-C1 | G20 |
| 1-S1 | G1 |
| 1-S10 | G10 |
| 1-S11 | G11 |
| 1-S12 | G12 |
| 1-S13 | G13 |
| 1-S14 | G14 |
| 1-S15 | G15 |
| 1-S16 | G16 |
| 1-S17 | G17 |
| 1-S18 | G18 |
| 1-S19 | G19 |
| 1-S2 | G2 |
| 1-S3 | G3 |
| 1-S4 | G4 |
| 1-S5 | G5 |
| 1-S6 | G6 |
| 1-S7 | G7 |
| 1-S8 | G8 |
| 1-S9 | G9 |
| 2-S1 | G21 |
| 2-S10 | G30 |
| 2-S11 | G31 |
| 2-S12 | G32 |
| 2-S13 | G33 |
| 2-S14 | G34 |
| 2-S15 | G35 |
| 2-S16 | G36 |
| 2-S17 | G37 |
| 2-S18 | G38 |
| 2-S19 | G39 |
| 2-S2 | G22 |
| 2-S20 | G40 |
| 2-S21 | G41 |
| 2-S22 | G42 |
| 2-S23 | G43 |
| 2-S24 | G44 |
| 2-S25 | G45 |
| 2-S26 | G13 |
| 2-S27 | G46 |
| 2-S28 | G5 |
| 2-S29 | G6 |
| 2-S3 | G23 |
| 2-S30 | G47 |
| 2-S31 | G48 |
| 2-S32 | G49 |
| 2-S33 | G50 |
| 2-S4 | G24 |
| 2-S5 | G25 |
| 2-S6 | G26 |
| 2-S7 | G27 |
| 2-S8 | G28 |
| 2-S9 | G29 |
| 3-S1 | G51 |
| 3-S10 | G57 |
| 3-S11 | G58 |
| 3-S12 | G59 |
| 3-S13 | G60 |
| 3-S14 | G61 |
| 3-S15 | G62 |
| 3-S16 | G39 |
| 3-S17 | G63 |
| 3-S18 | G64 |
| 3-S19 | G65 |
| 3-S1b | G52 |
| 3-S2 | G36 |
| 3-S3 | G53 |
| 3-S4 | G26 |
| 3-S5 | G54 |
| 3-S6 | G55 |
| 3-S7 | G56 |
| 3-S8 | G33 |
| 3-S9 | G45 |
| 4-S1 | G18 |
| 4-S10 | G70 |
| 4-S11 | G71 |
| 4-S12 | G72 |
| 4-S13 | G6 |
| 4-S14 | G15 |
| 4-S15 | G9 |
| 4-S16 | G73 |
| 4-S17 | G74 |
| 4-S18 | G75 |
| 4-S19 | G76 |
| 4-S2 | G66 |
| 4-S20 | G77 |
| 4-S21 | G78 |
| 4-S22 | G36 |
| 4-S23 | G79 |
| 4-S24 | G80 |
| 4-S25 | G81 |
| 4-S26 | G17 |
| 4-S27 | G82 |
| 4-S28 | G83 |
| 4-S29 | G84 |
| 4-S3 | G67 |
| 4-S30 | G85 |
| 4-S31 | G16 |
| 4-S32 | G86 |
| 4-S33 | G87 |
| 4-S34 | G88 |
| 4-S4 | G68 |
| 4-S5 | G13 |
| 4-S6 | G5 |
| 4-S7 | G61 |
| 4-S8 | G10 |
| 4-S9 | G69 |
| 5-S1 | G22 |
| 5-S10 | G94 |
| 5-S11 | G95 |
| 5-S12 | G96 |
| 5-S13 | G97 |
| 5-S14 | G98 |
| 5-S15 | G61 |
| 5-S16 | G99 |
| 5-S17 | G100 |
| 5-S18 | G5 |
| 5-S19 | G101 |
| 5-S2 | G89 |
| 5-S20 | G102 |
| 5-S21 | G103 |
| 5-S22 | G7 |
| 5-S23 | G6 |
| 5-S24 | G9 |
| 5-S25 | G15 |
| 5-S26 | G104 |
| 5-S27 | G105 |
| 5-S28 | G106 |
| 5-S3 | G90 |
| 5-S4 | G91 |
| 5-S5 | G92 |
| 5-S6 | G2 |
| 5-S7 | G13 |
| 5-S8 | G93 |
| 5-S9 | G79 |
