# E 语言选择与 AI 运营

> 研究日期：2026-10-06。研究者：E 视角子研究员。
> **重要方法说明**：help.x.com（规则原文所在域）对本研究环境返回 Cloudflare 403（WebFetch、curl、r.jina.ai 都试过），archive.org 也限流了，所以**没能逐页直接打开规则原文**。下文里标"原文（经搜索引擎索引摘录）"的句子，来自限定 `help.x.com` 域名后搜索引擎返回的页面摘要，再和开发者社区帖、第三方转述交叉核对过。成稿前请人工在浏览器打开对应页面复核措辞。docs.x.com（开发者政策、API 定价）已直接打开精读。

## 来源

| 编号 | 标题 | 机构/作者 | 日期 | 等级 | URL |
|---|---|---|---|---|---|
| E-S1 | Automation rules | X 帮助中心 | 页面据报 2026-04 更新（未能直连核实） | A（经搜索摘录） | https://help.x.com/en/rules-and-policies/x-automation |
| E-S2 | Authenticity（原 Platform manipulation and spam policy） | X 帮助中心 | 未知（未能直连） | A（经搜索摘录） | https://help.x.com/en/rules-and-policies/platform-manipulation |
| E-S3 | Original Content Rewards | X 帮助中心 | 2026（未能直连） | A（经搜索摘录） | https://help.x.com/en/using-x/original-content-rewards |
| E-S4 | Grok Bot Template Rewards Pilot | X 帮助中心 | 2026-09 前后 | A（经搜索摘录） | https://help.x.com/en/using-x/grok-bot-template-rewards-pilot |
| E-S5 | Developer Policy | X 开发者文档 docs.x.com | 未标注日期，2026-10-06 访问 | A | https://docs.x.com/developer-terms/policy |
| E-S6 | X API Pricing（pay-per-usage） | X 开发者文档 docs.x.com | 2026-10-06 访问 | A | https://docs.x.com/x-api/getting-started/pricing |
| E-S7 | Nikita Bier 帖子："We're rolling out auto-translate worldwide…" | X 产品负责人 Nikita Bier | 2026-04-07 | A | https://x.com/nikitabier/status/2041335306331549699 |
| E-S8 | X is rolling out automatic translation and photo editing powered by Grok | TechCrunch / Ivan Mehta | 2026-04-08 | B | https://techcrunch.com/2026/04/08/x-is-rolling-out-automatic-translation-and-photo-editing-powered-by-grok/ |
| E-S9 | X translation Japanese（日语自动翻译上线） | GIGAZINE | 2026-03-31 | B | https://gigazine.net/gsc_news/en/20260331-x-translation-japanese |
| E-S10 | Musk: Grok auto-translate & recommend foreign-language posts | PiunikaWeb | 2026-03-30 | C | https://piunikaweb.com/2026/03/30/elon-musk-grok-auto-translate-recommend-foreign-language-posts-x/ |
| E-S11 | X 平台面向全球推出 Grok 自动翻译（中文） | IT之家 | 2026-05-29 | B | https://www.ithome.com/0/956/853.htm |
| E-S12 | 马斯克中文推文是否 Grok 翻译 | 机核 gcores | 2026-05 | C | https://www.gcores.com/articles/214506 |
| E-S13 | Auto-translation & Japanese social media | Unseen Japan | 2026-07 之后（引用 7/1 帖子） | B- | https://unseen-japan.com/auto-translation-japanese-social-media/ |
| E-S14 | Essential X stats（Digital 2025） | DataReportal / Kepios | 2025-03-12（数据 2025-01） | A-（原始数据报告，基于 X 广告工具） | https://datareportal.com/essential-x-stats |
| E-S15 | Digital 2026: Taiwan | DataReportal | 数据 2025-10，发布 2025-11 前后 | A- | https://datareportal.com/reports/digital-2026-taiwan |
| E-S16 | Digital 2026: Hong Kong | DataReportal | 数据 2025-10 | A- | https://datareportal.com/reports/digital-2026-hong-kong |
| E-S17 | 各类"X 用户国家分布 2026"汇总 | searchengineland / demandsage / Semrush 等 | 2025-12 至 2026 | C | https://searchengineland.com/guide/twitter-users ；https://www.semrush.com/website/x.com/overview |
| E-S18 | Twitter estimates it has 10 million users in China | TechCrunch / Fortune | 2016-07 | B（但已过时） | https://fortune.com/2016/07/05/twitter-china-users |
| E-S19 | X live-tweets its fight against chatbot spam in real time | Search Engine Journal / Roger Montti | 2026-07-26 | B | https://www.searchenginejournal.com/x-live-tweets-its-fight-against-chatbot-spam-in-real-time/ |
| E-S20 | X Says It Removed 42,000 Chatbot Reply Accounts | LetsDataScience | 2026-07-27 | C | https://letsdatascience.com/news/x-says-it-removed-42000-chatbot-reply-accounts-0e994445 |
| E-S21 | X removed over 1.7 million bots; DM spam next | WION | 2025-10-13 | B | https://www.wionews.com/technology/x-removed-over-1-7-million-bots-dm-spam-next-says-product-head-nikita-bier-1760344720045/amp |
| E-S22 | X continues massive ban wave, 208 bots per minute | Roboin | 2026-04-09 | C | https://roboin.io/article/en/2026/04/09/x-continues-massive-ban-wave-removing-208-bots-per-minute/ |
| E-S23 | X rolls out dislike button test… "Give me 60 seconds" | Storyboard18 | 2026-03-18 | B- | https://www.storyboard18.com/brand-makers/x-rolls-out-dislike-button-test-after-product-heads-give-me-60-seconds-response-to-user-suggestion-92566.htm |
| E-S24 | Elon Musk's X bans access for InfoFi crypto projects after AI slop backlash | Decrypt | 2026-01 | B | https://decrypt.co/354736/elon-musks-x-bans-access-infofi-crypto-projects-ai-slop-backlash |
| E-S25 | X to require AI labels on armed conflict videos from paid creators | Engadget / Andre Revilla | 2026-03-03 | B | https://engadget.com/social-media/x-to-require-ai-labels-on-armed-conflict-videos-from-paid-creators-citing-times-of-war-183631400.html |
| E-S26 | X adds AI labels and paid partnership labels | Roboin | 2026-03-03 | C | https://roboin.io/article/en/2026/03/03/x-adds-ai-and-paid-partnership-labels-to-boost-content-transparency/ |
| E-S27 | X ending creator revenue sharing, launching Original Content Rewards | GIGAZINE | 2026-08-08 | B | https://gigazine.net/gsc_news/en/20260808-x-original-content-rewards-program/ |
| E-S28 | Hypefury 定价页 FAQ | Hypefury 官方 | 2026-10-06 访问 | A（工具方一手） | https://hypefury.com/pricing/ |
| E-S29 | Hypefury dropped X support | Eden（竞品博客） | 2026-08 | C | https://eden.so/blog/hypefury-dropped-x-support/ |
| E-S30 | Hypefury vs Typefully 2026 等工具对比 | wearefounders / socialpilot | 2026 | C | https://www.wearefounders.uk/hypefury-vs-typefully-2026-which-x-tool-is-worth-paying-for/ |
| E-S31 | Grok 帖子"Enhance your post"/校对功能 | TestingCatalog / Basenor | 2025-01 至 2026-03 | C | https://www.testingcatalog.com/new-x-feature-lets-users-proofread-and-rewrite-posts-with-grok.md |
| E-S32 | Raptive study shows AI content cuts reader trust by half | PPC Land（报道 Raptive 调研） | 2025-07-16 | B-（商业方委托调研） | https://ppc.land/raptive-study-shows-ai-content-cuts-reader-trust-by-half/ |
| E-S33 | How Americans View AI and Its Impact on People and Society | Pew Research Center | 2025-09-17 | A | https://www.pewresearch.org/science/2025/09/17/how-americans-view-ai-and-its-impact-on-people-and-society/ |
| E-S34 | Musk：X 将移除启发式推荐算法、由 Grok 接手 | IT之家 | 2025-10-21 | B | https://www.ithome.com/0/891/072.htm |
| E-S35 | 16 days of building in public（华人开发者 Leo Zhang 案例） | dev.to 个人博客 | 2025-2026 | C | https://dev.to/leozhang8285/16-days-of-building-in-public-what-actually-moves-the-needle-hj1 |
| E-S36 | X 开发者论坛 AI reply bot 审批请求帖 | devcommunity.x.com | 2026-08 至 09 | B（论坛，含官方员工回复的二手转述） | https://devcommunity.x.com/t/request-for-prior-written-approval-for-ai-generated-replies/273526 |

---

## 事实卡片

### E1 语言选择

[E-F1] X 用户的国家分布高度集中：按 DataReportal 2025 年 1 月的广告受众，美国 1.04 亿、日本 7090 万，此后依次是印尼 2520 万、印度 2410 万、英国 2290 万；全球广告受众 5.86 亿，同比降 5.3%。
- 来源：[E-S14] ｜ A- ｜ 交叉验证：Semrush/Similarweb 类流量数据（[E-S17]，C）显示 x.com 流量美国约 22%、日本约 15%（2025-12），排序一致；2026 年各国 MAU 的汇总数字彼此冲突（美国 9500 万到 1.2 亿不等，印度 2500 万到 1 亿不等），**不建议引用具体的 2026 国别 MAU**。
- 原文关键句：DataReportal 提示，ad reach "not a direct proxy for metrics like monthly active users"，并且包含重复和非真人账号。
- 对创作者的含义：X 实际上是"美国 + 日本"的双核平台；英文区规模比任何中文受众大一个数量级以上。

[E-F2] 台湾 X 广告受众 601 万（占总人口 26.0%，同比 +15.7%），和 Threads（665 万）差不多，远低于 Facebook（1730 万）、Instagram（1220 万）。
- 来源：[E-S15] ｜ A- ｜ 交叉验证：只有单一来源；DataReportal 自己也提示 X 广告工具近期有"unusual trends"。
- 对创作者的含义：台湾是中文 X 受众的真实基本盘之一，但在当地 X 不是主流平台；Threads 在台湾和 X 体量相当，是中文创作者的同等级备选。

[E-F3] **香港 X 广告受众 1240 万，相当于总人口的 168%**（同比 +38.6%），明显超过 Facebook（470 万）和 Instagram（405 万）。
- 来源：[E-S16] ｜ A- ｜ 交叉验证：只有单一来源。DataReportal 自己说百分比超过 100% 属于报告异常，提醒谨慎解读。
- 推断（标注为推断，未找到一手证据）：超出香港人口的部分，很可能是大量使用香港节点翻墙的大陆用户被 X 归到了香港。这间接说明"翻墙大陆用户"是中文 X 受众里很大的一块，但**没有可靠来源给出大陆用户的具体数量**。唯一的官方估计是 2016 年 Twitter 内部说的"中国约 1000 万用户"（[E-S18]，已过时 10 年）。
- 对创作者的含义：中文受众的构成是：大陆翻墙用户（可能最多）+ 台湾 + 香港 + 海外华人；各部分的规模都没有可靠的 2026 数据。

[E-F4] 2026-03-29/30，马斯克宣布 Grok "automatically translating and recommending 𝕏 posts from other languages is starting to work"；3 月 30 日起日本用户看到的外语帖子默认直接显示为日语译文，不用点按钮。
- 来源：[E-S9]（B）、[E-S10]（C）｜ 交叉验证：两家媒体对马斯克原话的引用一致；xAI 工程师 Rei Hotate 说是他在 Grok 多语言后训练之后搭建的这套系统（[E-S9]）。
- 对创作者的含义：X 官方的意图不只是"翻译"，还包括**跨语言推荐**，也就是把外语帖子推进你的推荐流。

[E-F5] 2026-04-07，Nikita Bier 宣布自动翻译全球上线："We're rolling out auto-translate worldwide to give posts in any language global reach on X. The translations are powered by Grok…If you prefer to read in the original language, you can always turn off auto-translate"。
- 来源：[E-S7]（A）、[E-S8]（B）｜ 交叉验证：TechCrunch 引用一致。
- 冲突/补充：IT之家（[E-S11]）根据用户反馈报道，**中文的自动翻译似乎到 2026-05-28 左右才上线**，说明各语言是分批开通的。关闭方式是点译文帖子上的齿轮图标，可以按语言单独关闭；这是**读者端**的开关。**没有找到作者端可以禁止自己帖子被翻译的选项。**
- 对创作者的含义：现在用中文发帖，理论上也会以英文、日文等译文出现在外语用户面前，"中文帖 = 只有中文受众"的假设已经不成立。

[E-F6] 自动翻译确实能让原本只在单一语言里传播的帖子破圈，但质量和语境风险都是真实存在的：日本漫画家ふとしSLIM 的一条日语帖子经翻译后拿到约 2400 万浏览、8.19 万赞；《游戏人生》作者榎宫祐（Yuu Kamiya）批评自动翻译"genuinely garbage"，会"arbitrarily paraphrases"，原帖获约 8.4 万赞（2026-07-01）。Bier 称这次上线是"the largest cultural exchange event in history"，并鼓励创作者"post in their own language about their culture and daily life"。
- 来源：[E-S13]（B-）、[E-S10]（C）｜ 交叉验证：Bier 两句话分别来自两个来源，没有在 X 原帖上逐字核对；破圈案例只有单一来源。
- 对创作者的含义：用母语写"本地视角、文化、日常"的内容，是 X 官方明确鼓励的方向；但涉及政治、宗教、反讽和梗的内容，翻译后容易被误读，从而引来外语区的争吵。

[E-F7] X 推荐系统正在转向由 Grok 理解内容本身：马斯克 2025-10 说将"完全移除启发式推荐算法"，由 Grok "读取和观看全部内容"来匹配兴趣；2026-01 又宣布做"可用提示词控制的推荐流"。
- 来源：[E-S34]（B），以及 LetsDataScience 2026-01-18 的报道（C）｜ 交叉验证：两家媒体都记录了马斯克的表态；实际上线到什么程度，未找到一手技术文档。
- 对创作者的含义：语义理解加上翻译，意味着"内容好不好"比"用什么语言写"更能决定能不能被推荐。不过这是平台的方向表态，不是已被验证的效果。

[E-F8] 2026 年 X 的创作者分成规则改成了按 **Premium（付费认证）用户产生的有效曝光**计算：Creator Revenue Sharing 于 2026-09-07 结束，换成 Original Content Rewards（OCR）。门槛是 Premium 订阅、500+ 认证粉丝、近 90 天来自认证用户的首页时间线曝光 50 万+；按"unique impressions recorded by premium users when more than 50% of the post is displayed on the home timeline"计算，搬运和聚合内容不算。
- 来源：[E-S3]（A，经搜索摘录）、[E-S27]（B）｜ 交叉验证：两个来源对门槛的描述一致。冲突：OCR 首次付款和申请开放的日期，GIGAZINE 写的是"8/28 首付，9/8 CRS 用户可申请"，其他二手来源写的是"9/8 开放"，以官方页面为准。
- 对创作者的含义（推断）：收益取决于 Premium 用户看了多少。Premium 用户在各国的分布**未找到可靠数据**，所以"英文受众的 Premium 比例更高、更赚钱"这个说法目前**没有证据支撑**，只能当作假设。

[E-F9] 关于"中文创作者做英文账号"的成功案例，**未找到 B 级以上来源的系统性案例**。只找到个人博客级别的案例，比如华人开发者 Leo Zhang 说同一条内容发到 X 的 Build in Public 社区，比直接发时间线的互动高约 12 倍（36 vs 3 次浏览，样本极小）。
- 来源：[E-S35] ｜ C ｜ 交叉验证：无。
- 对创作者的含义：独立开发者赛道的英文 build in public 有一套成熟打法（社区投放、公开收入），但中文作者转英文的成功率和转化数据都没有可靠证据。

[E-F10] 语言对品牌商单报价的影响：**未找到可靠来源**。中英文受众的 CPM、商单报价差异，在本轮搜索里没有找到可信的公开数据。

### E2 AI 辅助运营

[E-F11] X 自动化规则对 **AI 回复机器人**的原文要求：可以用 AI 做"context-aware"的自动回复机器人，但"the deployment or operation of any AI reply bot requires prior written and explicit approval from X"。
- 来源：[E-S1]（A，经搜索摘录）｜ 交叉验证：开发者论坛上有大量"AI reply bot approval request"帖子（[E-S36]），vorplabs、PublishPort 也独立转述了这条规定，说该页 2026-04 更新过。补充（二手）：据转述，X 员工在 2026-08、09 的论坛回复里说，没有单独的审批表单；用户主动 @、一次互动只回复一次、带 Automated 标签的提及触发式机器人不需要额外审批。这一点只有二手转述，未核实原帖。
- 对创作者的含义：个人账号用 AI 自动生成并发送回复，在规则上属于需要 X 书面批准的行为。普通创作者基本拿不到批准，等于**红线**。

[E-F12] 自动化规则其他条款（原文经搜索摘录）：
- "You may not like posts or hide replies in an automated manner."（禁止自动点赞）
- 不允许以未经请求的方式自动 @ 或回复大量用户，"sending automated replies to posts based on keyword searches alone is not permitted"。
- 自动回复只有在对方事先请求或明确表示愿意被联系、提供退出方式、一次互动只回复一次、并且是回复对方原帖时才允许。
- 自动发帖可以用于"entertainment, informational, or novelty purposes"，但不能是 spam。
- 不允许用多个账号刷趋势和话题标签。
- 来源：[E-S1]（A，经搜索摘录）｜ 交叉验证：docs.x.com 开发者政策（[E-S5]，A，已直接精读）写着"Always get explicit consent before sending people automated replies or Direct Messages"，以及"If you're operating an API-based bot account you must clearly indicate what the account is and who is responsible for it"，同时要求写操作服务遵守 Automation Rules，禁止多个账号发相同内容。两个来源一致。
- 对创作者的含义：**定时发布自己写的原创帖子是合规的**（工具调 API 发帖）；自动点赞、按关键词自动回复、自动关注和取关都违规。

[E-F13] Authenticity（平台操纵）政策：禁止用多个账号对相同内容互动来抬高热度，禁止"coordinating to exchange engagement"（互赞、互转、互关、刷浏览这类互助群）。处罚包括限流（不进搜索和趋势、回复区降权）、锁号验证、封号。
- 来源：[E-S2]（A，经搜索摘录）｜ 交叉验证：开发者政策 [E-S5] 也禁止多账号发相同内容；执法报道见 E-F14。
- 对创作者的含义：中文区常见的"互关群""互助转发群"在规则上属于违规的协调互动。

[E-F14] X 清理 bot 和 AI 回复的执法时间线（都出自 X 产品负责人 Nikita Bier 的公开帖子）：
- 2025-10：一周内清理 170 万个刷回复的 bot（"This week we purged 1.7 million bots engaging in reply spam"）。[E-S21] B
- 2026-01-15：吊销"发帖得奖励"类 InfoFi 应用（如 Kaito Yaps）的 API 权限，理由是这类应用"led to a tremendous amount of AI slop and reply spam"；Kaito 随后关停 Yaps。[E-S24] B
- 2026-03-18 前后：回复区开始测试"踩"按钮。不公开计数，只作为排序信号，反馈理由里有"AI generated"和"Spam"。[E-S23] B-
- 2026-04-03 至 09：针对回复 bot 的封号潮，Bier 说"identifying and suspending 208 bots per minute"，日本是回复垃圾最多的国家。[E-S22] C
- 2026-07-24/25：清除 42,000 个"用聊天机器人自动回复"的账号。Bier 原话："using AI to programmatically engage with users without a human in the loop runs counter to our mission"；他还说这类 spam 是为了涨粉后接 AI 公司的付费推广，并且封掉了用 Grok 生成回复的那条路（"We blocked the Grok one yesterday"）。[E-S19] B、[E-S20] C
- 交叉验证：42,000 和"human in the loop"有 SEJ 和 LetsDataScience 两个来源；所有数字都是 X 的自报口径，没有第三方审计。
- 对创作者的含义：X 划的线很清楚，**是否有人在环（human in the loop）是关键**。AI 帮你写、你自己看过再发，属于人在环；AI 自动替你互动，属于打击对象。

[E-F15] AI 内容披露：2026-03-01，X Creators 官方推出可选的"Made with AI"自我标注开关（以及付费合作标签）；2026-03-03，Bier 宣布不加 AI 披露就发武装冲突类 AI 视频的人，将被暂停分成资格 90 天，再犯永久取消。识别靠 Community Notes 和生成工具的元数据。Engadget 称这是 X 第一条强制 AI 披露的规则。
- 来源：[E-S25]（B）、[E-S26]（C）；OCR 页面（[E-S3]，A 经搜索摘录）沿用了这条规定 ｜ 交叉验证：多家媒体报道一致。
- 对创作者的含义：除冲突类视频外，AI 标注目前是自愿的。打标签会不会影响推荐，**未找到证据**。

[E-F16] OCR 明确把"aggregated content"（主要是编辑、拼合他人内容，没有加入实质性新观点）排除在分成之外。
- 来源：[E-S3]（A，经搜索摘录）、[E-S27]（B）｜ 对创作者的含义：用 AI 批量"洗稿、搬运、汇编"在 2026 年不但有封号风险，还直接拿不到分成。

[E-F17] Grok 在 X 内的创作相关功能：发帖框里的 Grok 按钮"Enhance your post"（校对、改写、精简，可选语气），网页端在 2025-01 就有，马斯克 2026-03 公开推荐用 Grok 校对；Grok Imagine 生图生视频（Premium 可用）；2026-04 在 iOS 上线 Grok 驱动的图片编辑（模糊敏感信息、自然语言改图）；2026-09 美国区开始邀请制的"Grok Bot Template Rewards"试点（按模板使用量发奖励，要求用付费合作标签）。
- 来源：[E-S31]（C）、[E-S8]（B，图片编辑）、[E-S4]（A，经搜索摘录）｜ 交叉验证：图片编辑和模板奖励有 B 级或官方来源；"Enhance your post"只有 C 级来源。
- 对创作者的含义：X 官方一边打击 AI 自动互动，一边推 AI 辅助创作。这说明平台的边界是"自动化互动"，不是"用 AI"本身。

[E-F18] 第三方工具 2026 年的格局：
- X API 在 2026-02 改为按量计费，发一条帖子 $0.015，**带 URL 的帖子 $0.200**，读一条帖子 $0.005。[E-S6] A（docs.x.com 直接精读）
- **Hypefury 官方定价页写着"Nope! Hypefury no longer supports 𝕏 :("**，现在支持 Bluesky、Threads、LinkedIn、Instagram、TikTok。[E-S28] A；[E-S29] C 说是 2026-08 前后的事。
- Typefully 定位是写作加排期（Creator 档含 AI 写作），Tweet Hunter 定位是 AI 写作、爆款库、自动转推、自动 plug、自动私信（$29/月起）。[E-S30] C
- 对创作者的含义：工具成本上升，并且通过 API 发带链接的帖子特别贵。Tweet Hunter 一类工具里的"自动私信、自动转推"功能，要拿 E-F12 的规则逐项核对后再开。

[E-F19] 读者对 AI 内容的反感有调研支持：
- Pew（2025-06-09 至 15，美国成人 5,023 人）：76% 认为能分辨内容是 AI 还是人做的"极其或非常重要"，53% 没信心自己分辨得出来；50% 对 AI 更多是担忧而不是兴奋。[E-S33] A
- Raptive 委托调研（美国成人 3,000 人，2025-07）：读者**以为**内容是 AI 写的时候，信任度下降近 50%，同页广告的购买考虑下降 14%。高管原话："regardless of whether it was really AI generated or not"。[E-S32] B-（商业方委托调研，有利益相关）
- 交叉验证：两份调研方向一致，但都是美国样本。**没有找到针对中文读者或 X 用户的 AI 反感调研**。X 回复区"踩"按钮专门设了"AI generated"理由（E-F14），可以侧面说明平台认定用户反感这类内容。
- 对创作者的含义：只要"看起来像 AI 写的"就会掉信任，不管实际是不是 AI 写的。AI 腔调本身就是风险。

---

## 中文 vs 英文 决策框架（基于证据）

**先说结论**：2026 年这个问题已经从"选哪种语言"变成"用哪种语言写得最好、最像本人"。原因是 Grok 自动翻译（E-F4、E-F5）加上跨语言推荐，正在把母语内容推给外语读者。不过跨语言推荐的实际效果、中文帖子的外溢比例，**目前都没有数据**，所以下面是带条件的建议，不是定论。

| 你的情况 | 建议 | 证据依据 |
|---|---|---|
| 内容的价值依赖中文语境（大陆时事解读、中文互联网文化、面向华人的出海、留学、移民服务，币圈中文社区） | **写中文**，把翻译外溢当额外收获 | 受众在中文区（E-F2、E-F3）；翻译容易丢失语境（E-F6） |
| 内容本身国际通用（AI 工具、独立开发、编程、设计、投资美股），英文写作能力能达到母语者的 80% | **主号写英文**，或者英文为主、中文为辅 | 英文区规模大一个量级（E-F1）；英文 build in public 社区成熟（E-F9，C 级） |
| 英文写作明显吃力，靠 AI 翻译整段发出 | **不推荐专门开英文号发机翻**，先写好中文、依靠平台翻译 | 平台已经会自动翻译（E-F5）；AI 腔会让信任下降近一半（E-F19）；不过 Grok 翻译质量本身也有人批评（E-F6） |
| 想做"中国视角向世界讲中国、亚洲" | 中文和英文都可以；Bier 明确鼓励用母语写本地文化和日常 | E-F6（Bier 原话，C 级转述） |
| 想靠 X 的平台分成赚钱 | 语言是次要的，关键是吸引 **Premium 用户**的有效曝光 | E-F8；各国 Premium 分布**无数据** |

**双语策略对比**（证据很弱，只能给逻辑分析，没有找到可靠的案例数据）：
- **同一条帖子写中英双语**：字数翻倍，在推荐流里读起来别扭；而且平台已经自动翻译，收益有限。不推荐。
- **双账号（中文号 + 英文号）**：可以按受众分开运营，代价是精力翻倍。注意 Authenticity 政策禁止多账号互相刷量（E-F13），两个账号之间不要做协调互动刷数据。
- **先写中文，再用 AI 改成英文发英文号**：可行的前提是由人改写成英文母语的表达，不能直接贴机翻。有人在环、没有 AI 腔，才不会掉信任。

---

## AI 使用红绿灯（绿=放心用 / 黄=谨慎 / 红=别做，每条附依据）

### 🟢 绿灯：放心用
| 用法 | 依据 |
|---|---|
| 用 AI 找选题、做研究、整理资料、列提纲 | 不涉及平台上的任何自动化行为；规则不管 |
| 用 AI（含 X 内置 Grok "Enhance your post"）校对、改写、精简自己的草稿，自己审定后手动发出 | 属于"human in the loop"（E-F14，Bier 原话）；X 官方自己在推这个功能（E-F17） |
| 用 AI 分析自己的数据（导出的 Analytics、爆帖复盘） | 只是只读分析，不涉及写操作 |
| 用排期工具定时发**自己写的**原创帖子 | 自动化规则允许 informational 类自动发帖（E-F12）；开发者政策允许合规的写操作（E-F12） |
| 用 AI 生图或配图并主动打"Made with AI"标签 | 标签是官方提供的自愿披露工具（E-F15） |

### 🟡 黄灯：谨慎
| 用法 | 风险与依据 |
|---|---|
| 把中文帖子用 AI 翻译成英文直接发 | 读者以为是 AI 写的，信任就会掉约 50%（E-F19，B- 级）；平台本身已有自动翻译（E-F5）。建议人工润色 |
| 让 AI 写全文，自己只改几个字 | 内容同质化，有 AI 腔；OCR 只奖励"meaningful original value"（E-F8、E-F16） |
| AI 生成的新闻、时事类图片或视频 | 武装冲突类不披露会被停分成 90 天（E-F15）；而且容易被打 Community Notes |
| Tweet Hunter 一类工具的"自动转推、自动 plug、自动私信" | 自动私信要求对方事先同意（E-F12，开发者政策原文）；开之前逐项核对规则 |
| 用 AI 帮你**起草**回复，但每条都自己看过再手动发 | 规则上属于人在环，但如果回复量很大、风格单一，容易被"踩"按钮标成"AI generated"并降权（E-F14） |

### 🔴 红灯：别做
| 用法 | 依据 |
|---|---|
| AI 回复机器人：自动生成并发出回复、评论 | 原文要求"prior written and explicit approval from X"（E-F11）；2026-07 清理了 4.2 万个账号（E-F14） |
| 按关键词自动回复、自动 @ 大号蹭流量 | "sending automated replies to posts based on keyword searches alone is not permitted"（E-F12） |
| 自动点赞、自动关注和取关 | "You may not like posts…in an automated manner"（E-F12） |
| 互赞、互转、互关群，多账号互刷 | Authenticity 政策禁止"coordinating to exchange engagement"（E-F13） |
| 用 AI 批量搬运、汇编、洗稿 | OCR 明确排除 aggregated content（E-F16），还有被判 spam 的风险 |
| 参与"发帖换代币或积分"的 InfoFi 项目，用 AI 批量发帖 | X 已于 2026-01 吊销这类应用的 API 权限（E-F14） |

---

## 💡 意外发现与洞见

1. **香港 X 广告受众是总人口的 168%**（E-F3）。这大概率是翻墙大陆用户被归到了香港，等于给"中文 X 受众主要是谁"提供了一个罕见的数据侧证。写作时可以用，但必须标明这是推断。
2. **Hypefury 已经放弃 X**（E-F18，官方定价页原话）。这是"X API 涨价、按量计费"之后工具生态收缩最直接的例子。另外，通过 API 发带链接的帖子要 $0.20 一条，是纯文本的 13 倍；这和 X 长期对外链限流的态度一致（后者是推断）。
3. **X 一边封 AI 回复，一边推 Grok 写作和 Grok 模板奖励**（E-F14 和 E-F17）。这不矛盾，平台的分界线是"有没有人在环、是不是自动化互动"，不是"用没用 AI"。这句话可以作为文章 AI 部分的核心论点。
4. **2026-07 那批被清理的 AI 回复号，目的是"涨粉后接 AI 公司的付费推广"**（E-F14，SEJ 转述 Bier）。教人"AI 回复涨粉"的课程，教的正是 X 打击的模式本身。
5. **"踩"按钮的反馈理由里专门有"AI generated"**（E-F14）。读者对 AI 回复的反感已经被产品化成排序信号，AI 腔的回复以后会被直接降权。
6. **中文自动翻译比日语晚了约两个月上线**（E-F5）。"中文帖子自动外溢给英文读者"在 2026 年 6 月以后才成立；在这之前的"中文号涨粉经验"，可能不适用于翻译开启后的环境。

---

## 小结（结论、证据强度、缺口）

**结论**
1. 规模上，英文区（美国为核心）和日语区远大于中文区。中文受众可以拆成台湾（约 600 万广告受众）、香港（数据异常，疑似包含大量大陆翻墙用户）和海外华人，但总量没有可靠数字。
2. 2026 年 3 月到 5 月，X 分批上线 Grok 自动翻译和跨语言推荐，中文约在 5 月底开通。"写中文就只有中文读者"不再成立，但跨语言推荐的实际效果**没有数据**。
3. 分成改按 Premium 用户的有效曝光计算（OCR，2026-09 起），原创是硬门槛。语言本身的变现差异**没有证据**。
4. AI 的边界：创作辅助是绿灯；所有"自动化互动"（AI 回复、自动点赞、按关键词回复、互刷）是红灯，规则原文和 2025-10 到 2026-07 的多轮清理都能支撑。

**证据强度**
- 强（A 或多个 B 来源）：自动翻译上线和官方表态、自动化规则核心条款、多轮封号数据（X 自报）、AI 冲突视频披露规则、OCR 门槛、API 定价、Hypefury 退出 X、Pew 调研。
- 中：DataReportal 国别受众（官方提示有异常）、Raptive 调研（商业方委托）、Grok 写作功能（只有 C 级来源）。
- 弱或缺：中文创作者做英文号的案例、双语策略效果、中英文商单报价差异、跨语言推荐的实际流量。

**缺口**
- help.x.com 规则页**没能直接打开**（Cloudflare 403），条款措辞来自搜索引擎摘录和多方转述，成稿前必须人工复核原文和"最后更新"日期。
- 没有 2026 年可靠的 X 国别 MAU（各家汇总彼此冲突），也没有大陆翻墙用户数（最新的官方估计是 2016 年的约 1000 万）。
- 各国 Premium 订阅分布未找到，所以"英文更赚钱"无法证实。
- 没有中文读者对 AI 内容反感的调研。
- 没有找到中文创作者通过双语或英文号取得成功、并且数据可查的 B 级以上案例。
- 大陆、台湾创作者能否提现 X 分成（支付通道），本轮没有查到官方依据。
