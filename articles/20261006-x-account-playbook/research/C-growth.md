# C 冷启动与涨粉

> 研究日期：2026-10-06 ｜ 视角：新号 0 → 1000 → 1 万粉
> 方法：约 28 次检索（中英文）、精读 15 篇网页；另把 X 官方开源仓库 `xai-org/x-algorithm` 克隆到本地（最新 commit 2026-10-06），直接读了源码。源码是本报告最硬的一手证据。
> 读源码的通用注意事项：`param.rs` 里的数值是**代码默认值**，线上可以被 feature switch / A/B 实验覆盖（仓库 README 明确有实验分桶）。所以下文凡写“代码默认值”的地方，都不等于“线上一定是这个数”。

## 来源

| 编号 | 标题 | 机构/作者 | 日期 | 等级 | URL |
|---|---|---|---|---|---|
| C-S1 | X For You Feed Algorithm（README，含 Notable Updates、Scoring、Under the Hood） | X / xAI 官方仓库 | 2026-10-06 版（README 内更新记到 2026-09-18） | A | https://github.com/xai-org/x-algorithm |
| C-S2 | docs/BIDIRECTIONAL_BOOST_CHANGE.md（互关加权变更说明 + diff） | X 官方仓库 | 描述 2026-07-10/13/24 变更 | A | https://github.com/xai-org/x-algorithm/blob/main/docs/BIDIRECTIONAL_BOOST_CHANGE.md |
| C-S3 | home-mixer/scorers/author_cold_start.rs + home-mixer/params/param.rs（新作者冷启动扶持、各动作权重） | X 官方仓库 | 2026-10 版 | A | https://github.com/xai-org/x-algorithm/tree/main/home-mixer |
| C-S4 | grox/flows/reply_spam/*、grox/core/lm/thread.py（回复区 LLM 打分与回复垃圾标签） | X 官方仓库 | 2026-10 版 | A | https://github.com/xai-org/x-algorithm/tree/main/grox |
| C-S5 | user-cred-v2/*（账号可信度 PageRank，属 platform_manipulation 包） | X 官方仓库 | 2026-10 版 | A | https://github.com/xai-org/x-algorithm/tree/main/user-cred-v2 |
| C-S6 | X Adds Comment Downvotes to Train Algorithm | Social Media Today | 2026-03-19 | B | https://socialmediatoday.com/news/x-formerly-twitter-adds-comment-downvotes-train-algorithm-tanking/815272/ |
| C-S7 | X algorithm update aims to make replies feel friendlier | Dataconomy | 2026-07-14 | B | https://dataconomy.com/2026/07/14/x-algorithm-update-aims-to-make-replies-feel-friendlier/ |
| C-S8 | X restricts programmatic bot replies（转述 X Developers 公告） | Tekedia | 2026-02-24 | B | https://www.tekedia.com/x-restricts-programmatic-bot-replies-to-boost-genuine-users-interaction/ |
| C-S9 | X bans access to InfoFi crypto projects / Kaito token plummets | Decrypt；The Block | 2026-01-15 | B | https://decrypt.co/354736/elon-musks-x-bans-access-infofi-crypto-projects-ai-slop-backlash ；https://www.theblock.co/post/385805/kaito-token-plummets-x-revises-api-policies-ban-infofi-crypto-projects |
| C-S10 | Platform manipulation and spam policy | X 帮助中心 | 未注明（2026-10 检索） | A（直连返回 403，文字取自搜索引擎摘录） | https://help.x.com/en/rules-and-policies/platform-manipulation |
| C-S11 | Automation rules | X 帮助中心 | 未注明 | A（同上，来自摘录） | https://help.x.com/en/rules-and-policies/x-automation |
| C-S12 | About X Premium | X 帮助中心 | 未注明 | A（同上，来自摘录） | https://help.x.com/en/using-x/x-premium |
| C-S13 | Creator Revenue Sharing | X 帮助中心 | 未注明 | A（同上，来自摘录） | https://help.x.com/en/using-x/creator-revenue-sharing |
| C-S14 | X Premium Users Get 10x More Reach（转述 Buffer 一年期研究） | Influencer Marketing Hub / Buffer | 2025-10-07 | B（二手转述） | https://influencermarketinghub.com/?p=222870 |
| C-S15 | How I went from 30 to 1,000 followers on X in 14 days | @JonBuildsHQ（Indie Hackers） | 2026-05-21 | A（自述） | https://www.indiehackers.com/post/how-i-went-from-30-to-1-000-followers-on-x-in-14-days-94fcd933e1 |
| C-S16 | 0 to 500 Twitter Followers in 30 Days | Dee Kargaev（个人博客） | 2025 年中（起点 2025-06-07） | A（自述） | https://blog.deeflect.com/05-twitter-growth/ |
| C-S17 | My Website's Growth Was Entirely Managed by AI（AI 托管增长复盘） | 鸭哥 Yan Wang（yage.ai） | 2026-06-01 | A（自述） | https://yage.ai/share/ai-managed-growth-en-20260601.html |
| C-S18 | 一条推文涨粉3000+，如何在X做一次成功的冷启动 | @AI_Jasonyu（X Article） | 约 2025-09 之后 | A（自述；X 返回 402 没读到全文，下面的数字来自搜索摘要） | https://x.com/AI_Jasonyu/article/2025943474156249308 |
| C-S19 | The X Growth Playbook We Ran Across 20 Accounts | Innmind（增长服务商） | 2026-06-09 | C | https://blog.innmind.com/x-growth-playbook-for-startup-founders-2026/ |
| C-S20 | 推特/个人品牌运营指南 2025 版 | Ruby Wang、starzq（Day1Global） | 2025-02-28 | C | https://www.web3brand.io/p/2025 |
| C-S21 | Reply guy（AI 回复工具） | Simon Willison | 2026-02-23 | B | https://simonwillison.net/2026/Feb/23/reply-guy/ |
| C-S22 | Who Is Nikita Bier? The Crypto Twitter Controversy | Backpack Learn | 2026-01-15（2026-07-16 更新） | C | https://learn.backpack.exchange/zh-cn/articles/nikita-bier-crypto-twitter |
| C-S23 | 2026 X 新手指南：如何打造高权重账号并获得收入 | 网易号“梗啾啾跨境说” | 2026-07-14 | C | https://www.163.com/dy/article/L1QDSG7T0556O6TC.html |
| C-S24 | How to Reach 1,000 Followers on X From Scratch: 2026 Roadmap | Farid Shukurov（Indie Hackers） | 2026-05-28 | C | https://www.indiehackers.com/post/how-to-reach-1-000-followers-on-x-twitter-from-scratch-a-complete-2026-roadmap-04c6c210f2 |
| C-S25 | Twitter Bio Optimization 2026 等主页优化文章 | TweetArchivist 等 | 2025–2026 | C | https://www.tweetarchivist.com/twitter-bio-optimization-guide-2025 |
| C-S26 | X Expands Transparency Tool / Under the Hood 报道 | Mezha、Roboin、Gigazine | 2026-08 至 2026-09 | B | https://roboin.io/article/en/2026/09/04/checking-xs-official-shadowban-checker-under-the-hood/ |
| C-S27 | Nikita Bier steps down as Head of Product at X | Shacknews | 2026-08 | B | https://www.shacknews.com/article/150270/nikita-bier-steps-down-as-x-head-of-product |
| C-S28 | X analytics guides（原生分析看板仅限 Premium 等） | Sociality.io、Neal Schaffer | 2026 | C | https://sociality.io/blog/twitter-analytics/ |
| C-S29 | Interview with Tony Dinh: 100 to 10k followers in 6 months | Indie Hackers | 2021（只作历史对照） | B | https://www.indiehackers.com/post/interview-with-tony-dinh-twitter-black-magic-100-to-10k-twitter-followers-in-6-months-8538468cfd |
| C-S30 | X new reply sorting options that don't rank blue checks higher | AlternativeTo | 2024-08 | C | https://alternativeto.net/news/2024/8/x-introduces-new-reply-sorting-options-that-don-t-rank-blue-check-users-higher |

## 事实卡片

### 一、算法机制（冷启动最相关的部分，主要依据开源源码）

[C-F1] X 的 For You 推荐里有一个**新作者冷启动扶持**（New-Author Boost）。被扶持的帖子要同时满足五个条件：①原创帖（不能是回复，也不能是转发）；②作者粉丝数 ≤ 50,000；③发布不超过 2 小时；④首页曝光 < 200；⑤本来的排名位置在候选列表前 97% 以内。系统每次刷新最多挑一条，把它提到第 15 位左右。挑哪一条用 Thompson 抽样，依据是这条帖子早期的“点赞数 / 首页曝光数”。
- 来源：[C-S3]（`author_cold_start.rs`；`param.rs` 默认值：`ColdStartFollowerCap=50000`、`ColdStartMaxPostAgeSecs=7200`、`ColdStartImpressionThreshold=200`、`ColdStartSlotMin/Max=15/16`、`LowImpressionsMaxPositionRatio=0.97`、`EnableViewerColdStart=true`） ｜ A ｜ 交叉验证：[C-S1] README 写明 “New-Author Boost: posts from authors whose impressions are below a threshold are lifted toward a target position”
- 原文关键句：`c.in_reply_to_tweet_id.is_none() && c.retweeted_tweet_id.is_none() && c.author_followers_count.is_some_and(|followers| (followers as i64) <= follower_cap)`
- 对创作者的含义：小号**原创帖**的头 2 小时是官方留出的“试镜窗口”。早期点赞率越高，越容易被抽中。回复和转发拿不到这个扶持，所以“只回复、不发原创”等于放弃了它。另外代码中有 control/treatment 分桶，说明这个扶持还处在实验状态，力度可能随时调整。

[C-F2] 2026 年 7 月上线的**互关加权**，按源码看是加在“互关作者的**原创帖**”上：把“预测你会回复”的权重从 5 加到 20（7-13 全量上线时的值），7-24 下调为 +15。作者自己的回复和转发不加权。
- 来源：[C-S2]、[C-S3]（`BidirectionalFollowReplyWeightBoost` 默认 15.0；`ReplyWeight` 5.0；`bidirectional_boost_eligible = !is_reply && !is_retweet && is_mutual_follow_author`） ｜ A ｜ 交叉验证：[C-S7] Dataconomy 2026-07-14 引用 Nikita Bier：“We noticed this data was missing from the algo and it made your friends appear less in your replies.”
- **冲突**：媒体报道（C-S7）把这次改动描述为作用在“回复区”；官方仓库文档（C-S2）写的是 “boosts original posts from people you mutually follow by increasing the weight on the predicted probability that you'll reply”，作用在 For You 的原创帖。回复区排序代码不在仓库里（见 C-F4），所以两者可能同时成立，目前无法确认。
- 原文关键句（C-S2）：“On July 13, 2026 … we rolled out a boost value of 20 to many users … on July 24, 2026 … we set the bidirectional follow reply boost value to 15 instead of 20.”
- 对创作者的含义：互关对象看到你原创帖的概率会被抬高。但加权乘在“对方可能回复你的预测概率”上。互关对象如果是不感兴趣的僵尸号或互粉群成员，这个预测概率本来就很低，加权后依然很低。互关有用的前提是对方真会和你对话。

[C-F3] 官方公开的默认权重（代码默认值）：点赞 0.5、回复 5、转发 1、引用 5、分享 2、**关注作者 4**、点开链接 0.2、停留 0.05、不感兴趣 −47.52、拉黑 −31.2、静音 −58.8、举报 −234。主页点击（profile click）的默认权重是 0。
- 来源：[C-S3] `param.rs` ｜ A ｜ 交叉验证：[C-S1] README 说明这些权重乘的是**你自己**做出该动作的预测概率，不是互动的原始计数：“it'd be incorrect … to conclude that ‘1 report cancels out 468 likes’”
- 对创作者的含义：“让人想回复、想关注”的内容权重最高。“让人想点不感兴趣或静音”的内容惩罚很重。蹭热点招来的错位流量，就容易触发这类负反馈。

[C-F4] 回复区排序有一条 Grok/Gemma 大模型打分管线：每条回复得到一个 score 和一段理由。score=0 的回复会被打上 `RiskyHighVizReply` 标签。用户可信度分（userCred）≥ 62 或带灰标的账号豁免这个标签。喂给模型的信号包括：该账号**过去 24 小时回复数**、粉丝数、过去 24 小时收到的“合理拉黑”数、**这条回复是否粘贴而来**、账号语言等。具体提示词没有公开。
- 来源：[C-S4]（`task_write.py`、`grox/core/lm/thread.py`、`constants.py: RISKY_HIGH_VIZ_REPLY_EXEMPT_MIN_PAGE_RANK_SCORE = 62`；`prompts.py` 注释 “prompts are excluded to reduce gameability”） ｜ A ｜ 交叉验证：[C-S6] Nikita Bier 2026-03 说回复算法是 “the worst product in the company”，随后开始整改
- 原文关键句：`lines.append(f"  - Num Replies Last 24 Hours: …")`、`lines.append(f"  - Reply Was Pasted: {post.is_pasted}")`
- 对创作者的含义：“一天 250 条回复”这种量本身就是模型能看到的输入信号。复制粘贴 AI 生成的回复也会被识别。新号可信度低、拿不到豁免，最容易被打上“高曝光风险回复”标签。

[C-F5] 账号可信度（UserCred v2）是一个 PageRank：在社交图上迭代计算，重启（teleport）权重一半均匀分给 **Premium/各类认证账号**，一半按过去 7 天的点赞和转发分配，并且以“互动者自身的可信度”加权。被调查认定为**关联账号（小号）之间的互动边会被剔除**，被封、受限、停用的账号不参与计算。
- 来源：[C-S5]（`UserCredV2App.scala`：`validUserInfoPipe.filter(u => !u.isNearZero && u.isPremium)`；`filterLinkedUserEdges` 读取 `AccountExpansionInvestigations`；`engagement_teleport_beta` 默认 0.5；`EngagementWindowDays = 7`） ｜ A ｜ 交叉验证：仅源码，单源。它在推荐打分里怎么用没有完全确认：Phoenix 嵌入里有 `user_credibility` 字段，回复垃圾标签的豁免阈值也引用了它
- 对创作者的含义：被 Premium 账号或高可信账号点赞、转发，能抬高你的可信度。拿自己的小号互刷不算数。买来的粉丝、粉丝被封以后，本来也算不进可信度。

[C-F6] 官方源码注释说，用群聊协调互动对排名**没有影响**：一次互动必须发生在首页时间线里推给他的那条帖子上，才计入推荐系统；“直接点进帖子”（比如从群聊链接进入）不计入。
- 来源：[C-S3] `param.rs` 注释 ｜ A ｜ 交叉验证：仅官方自述，单源
- 原文关键句：“For an account to count in the algorithms recommendation system, it must take place on a post served in Home Timeline. Directly navigating to a post (i.e., coordinating via groupchat) has no ranking impact.”
- 对创作者的含义：中文圈常见的“互赞群、互评群、发链接求互动”，按官方说法对推荐无效，还可能被 coordinated spam 分类器（C-S4 里有 `classifier_coordinated_spam.py`）识别出来。

[C-F7] For You 对“非关注作者”的帖子统一打一个小于 1 的折扣。别人关注的人发的回复和转发同样打折。有一个 `OONRetweetReplyFilter`，会把**你没关注的人发的回复**从 For You 过滤掉。
- 来源：[C-S1] README 的 Scoring 和 Filtering 表 ｜ A
- 对创作者的含义：“回复大号”涨粉，靠的不是让回复本身进入别人的 For You，而是在大号帖子的**回复区**被看到，然后有人点进主页。所以回复区排序（C-F4）和主页转化（C-F14）才是这条路的关键环节。

### 二、平台政策与执法（2025–2026）

[C-F8] 2026-03 起，X 在回复区加了“踩”，**只有 Premium 用户能用**，可选五种理由：不感兴趣 / 不准确或误导 / AI 生成 / 垃圾信息 / 举报。官方说法是：踩不直接降低可见度，主要作为个性化的偏好信号，同时简化举报路径。
- 来源：[C-S6] ｜ B ｜ 交叉验证：GlobalDatingInsights、Hongkiat 报道一致（搜索摘要）
- 原文关键句：Bier 称其 “designed as a user preference tool … while also providing a simplified reporting path”
- 对创作者的含义：低质的“沙发回复”会收到“AI generated/Spam”这类负反馈，再叠加 C-F3 的负权重和 C-F4 的 LLM 打分，“刷存在感”式回复的风险明显变大。

[C-F9] 2026-02-24，X 限制了用 API 发回复：只有原帖作者 @ 了你或引用了你，才能通过 API 回复。Free、Basic、Pro、按量付费各档都受限。目标就是遏制 AI 生成的垃圾回复。
- 来源：[C-S8]（转述 X Developers 公告） ｜ B ｜ 交叉验证：[C-S21] Simon Willison 2026-02-23 把这类工具称为 “reply guy tools … the latest scourge of Twitter”
- 对创作者的含义：“AI 自动回复大号”的工具链基本断了。剩下的绕过方式是网页脚本，而这违反自动化规则（C-F11），可能导致永久封号。

[C-F10] 2026-01-15，Nikita Bier 宣布不再允许“奖励用户发帖”的应用（InfoFi，比如 Kaito Yaps），并收回了它们的 API 权限。
- 来源：[C-S9] Decrypt + The Block ｜ B（双源） ｜ 原文关键句：“We will no longer allow apps that reward users for posting on X … This has led to a tremendous amount of AI slop [and] reply spam on the platform.”
- 对创作者的含义：加密 / Web3 中文圈过去常见的“刷 Yaps 涨粉”路径已经被官方关闭。

[C-F11] X 规则原文要点（摘自帮助中心，搜索摘录）：
  - 平台操纵政策禁止 “selling or purchasing followers or engagements (Reposts, Likes, mentions, X Poll votes)”、**follow churn**（大量关注后再取关来抬高自己的粉丝数），以及**协调交换互动**（coordinating to exchange engagement：Likes、Polls、Replies、Reposts、Lists、Views、Follows）。处罚是先临时锁号、限制功能，屡犯会被封号。
  - 自动化规则：自动点赞一律禁止；未经对方同意的自动回复或 @ 属于滥用；用非 API 的方式（比如脚本操作网页）做自动化，可能导致永久封号。
- 来源：[C-S10]、[C-S11] ｜ A（本次直连 help.x.com 被 Cloudflare 拦截，原文措辞取自多个搜索结果对官方页面的摘录，建议成稿前人工打开核对） ｜ 交叉验证：Postory、Watsspace 的转述一致
- 对创作者的含义：“互关圈 / 互粉群”如果是有组织地交换关注或互动，**按字面就落在“协调交换互动”的禁止范围内**，和平常自然地互相关注是两回事。

[C-F12] Nikita Bier 2026 年初公开说，加密圈触达下降不是算法压制，而是 “GM” 刷屏、模板回复、半自动互动把信息流淹没了（原帖已删）。另外，Bier 于 2026-08 宣布卸任产品负责人，转为顾问。
- 来源：[C-S22]（C，转述）、[C-S27]（B） ｜ 交叉验证：只有二手转述，原话找不到可靠存档
- 对创作者的含义：官方的态度一直是打击低质互动、刷量互动，这个方向不会因为人事变动而改变。

### 三、Premium/蓝标

[C-F13] 官方说法：Premium 各档都有“回复优先”（Basic “reply prioritization”、Premium “larger”、Premium+ “largest”）；进入创作者分成需要 Premium、近 3 个月 500 万次自然曝光、500 名认证粉丝。实测：Buffer 分析 7.1 万个账号的 1880 万条帖子，免费账号单帖曝光中位数不到 100，Premium 超过 600，Premium+ 超过 1,550；2025 年初免费账号互动率中位数为 0%。
- 来源：[C-S12]、[C-S13]（A，摘录）；[C-S14]（B，转述 Buffer） ｜ 交叉验证：免费账号拿不到 Premium 回复加权，这一点官方和实测一致
- **冲突 / 注意**：①Buffer 是相关性研究，愿意付费的账号本来就更活跃，存在选择偏差，原文没讨论这一点。②开源的 For You 主排序代码（home-mixer）里**没有找到显式的“Premium 乘数”**。Premium 在源码里能看到的作用，一是 UserCred 的重启种子（C-F5），二是回复区和搜索排序（官方帮助页说法，代码未开源）。所以“Premium 让 For You 曝光 ×4/×10”之类的说法，在源码层面找不到直接证据，只能视为观测结果。③2024-08 起回复区可以按“最相关 / 最新 / 最多赞”排序，非默认排序不再按蓝标优先（C-S30，C 级）。④中文营销文 C-S23 把分成门槛写成“300 万曝光”，与官方的 500 万不符，以官方为准。
- 对创作者的含义：对靠“回复大号”起号的人，Premium 的回复优先是实打实的杠杆；它还提供“踩”功能、完整的分析看板（C-F15）和变现资格。但不应该把 Premium 当作“For You 曝光开关”。

### 四、主页与指标

[C-F14] 主页优化对关注转化的影响**没有找到 A/B 级的可靠数据**。流传的说法都来自营销博客：“好 Bio 转化 25–40%，差的 < 5%”“真人头像多 47% 关注”“换掉置顶帖后，主页访问到关注的转化率从约 1.8% 升到约 4.1%”。这些都没有方法说明。
- 来源：[C-S25] ｜ C ｜ 交叉验证：无
- 机制侧旁证：源码里“主页点击”的默认权重为 0（C-F3），“关注作者”为 4。也就是说，主页本身不给推荐加分，访问者最终有没有关注才是信号。
- 对创作者的含义：建议写成“经验共识 + 自测”：用 X Analytics 里“主页访问 → 新增关注”的比例来对比改版前后，不要直接引用这些百分比。

[C-F15] X 原生分析：账号层面的总览包括曝光、互动率、**主页访问（Profile visits）**、**新增关注（Follows）**，单帖有曝光、互动、详情展开等。2026 年新增了视频活动面板（留存、完播）。**完整的账号分析看板仅限 Premium**，免费用户在手机端只能看单帖基础数据；原生看板默认显示 28 天，可导出最多 90 天。另有 2026-08 上线的官方工具 “Under the Hood”（试点）：可以下载 JSON，查看自己账号或帖子被打上的、会影响可见度的标签。门槛是近一个月发帖 ≥ 10 条，初期仅向注册满一年的账号开放。
- 来源：[C-S28]（C）；[C-S1] README（A，Under the Hood 链接 https://x.com/i/jf/under_the_hood）；[C-S26]（B） ｜ 交叉验证：“看板仅限 Premium”只有 C 级来源，没能读到官方帮助页确认
- 对创作者的含义：怀疑自己被限流的新号，可以先查 Under the Hood（满足门槛的话），不用靠第三方的“shadowban 检测”。

## 案例

> 说明：都是创作者自述，除特别注明外，第三方无法核实粉丝曲线。中文创作者案例没能拿到原文全文（X Article 需要登录或付费，知乎返回 403），已标出。

**案例 1｜@JonBuildsHQ（Solopreneur Dad）｜build in public / SaaS｜英文**
- 时间线：2026 年 5 月，14 天，约 30 → 1,000+
- 做法：以回复为主，高峰日回复 250+ 条、原创 18 条；写脚本分析 build-in-public 头部账号的爆款帖结构；把产品定位直接对准平台上已有的创作者人群。原文没有提到 Premium 或广告。
- 原话：“X growth is much more about replies than posting … replies are what actually put you in front of new audiences.”
- 来源：[C-S15] ｜ 可信度：A 级自述，不可核实。时间点在 3 月“踩”上线之后、7 月互关加权之前。日均 250 条回复在 C-F4 的信号下风险较高，作者没有讲后续。

**案例 2｜Dee Kargaev（@deeflect）｜AI 工具 / 开发 / 独立开发｜英文**
- 时间线：2025-06-07 起，30 天 0 → 500，写作时约 660
- 做法：前两周每天 15–20 条“有实质增量”的回复，专挑 5K–100K 粉的账号；发帖强调“基于真实使用的具体观点”；在美西科技圈活跃时段发帖。
- 无效做法（作者自述）：**AI 生成的回复**（建立不了真实关系）、**大量关注别人**（只换来礼貌性回关）、泛泛的技巧型长串（有曝光但没人关注）。
- 来源：[C-S16] ｜ 可信度：A 级自述，不可核实。适合作为“慢而稳”的样本。

**案例 3｜鸭哥 Yan Wang（yage.ai）｜AI / 技术博客｜中文作者，内容中英双语**
- 时间线：2026 年 2 月底至 5 月底，约 3 个月，X 粉丝 **171 → 4,813**；同期周活 2,500 → 7,000，邮件订阅 420 → 1,183
- 做法：作者自称“没有手动发过一条推”，全部交给 AI 系统做选题后的写作和分发；自己每天花 2 分钟挑选题。X 端的具体做法（频率、回复、语言）文中**没有披露**。
- 来源：[C-S17]（同一站点的另一页 yage.ai/llms.txt 的检索摘要里也是这组数字，但仍属同一作者自述，算不上独立双源） ｜ 可信度：A 级自述，不可核实。**风险提示**：这是“AI 托管发帖”，不是 AI 托管回复。是否触及自动化规则（C-F11）要看实现方式；2 月起 API 回复受限（C-F9），这类做法只适用于原创发帖。

**案例 4｜@AI_Jasonyu｜AI 赛道｜中文**
- 时间线（据搜索摘要）：2025 年 9 月起，半个月盘活一个注册 6 年、160 粉的“僵尸号”；单条推文曝光 24 万，8 小时涨粉 1,200+，72 小时 3,000+；后来涨到 25,300+。作者还说用同一套方法起号的朋友“不低于 20 个，几乎都是万粉以上”。
- 做法：本次**没有读到原文**（X 返回 402），具体方法未能核实。
- 来源：[C-S18] ｜ 可信度：自述，且只看到二手摘要，**成稿引用前必须人工打开原文核对**。

**案例 5｜Innmind 的 20 个创始人 / 公司账号（汇总样本）｜创业 / 科技｜英文**
- 数据：每个账号用 8 个月以上从 0 涨到约 2 万；0–3K 阶段日增 10–100，主要靠回复；3K–5K 是阶段切换点。
- 有效：每天持续发（作者称是“最强预测因子”）、在“pitch your startup / follow back”这类互相发现的帖子下回复、蹭现成的新闻热点、固定一种已验证的格式。无效：找捷径、天天换格式、三天打鱼两天晒网。
- 来源：[C-S19] ｜ 可信度：C（服务商自我宣传，没有公开账号名单，不可核实）。注意：在“follow back”帖下回复，本质是互关圈玩法，与 C-F11 的“协调交换关注”边界模糊。

**历史对照｜Tony Dinh（@tdinh_me）｜独立开发**：2021 年 6 个月内 100 → 1 万，靠“做一个推特工具（动态 Banner）+ 爆款演示帖”。属于 2021 年的老算法，只作为“产品即内容”打法的参考，**不能当作 2026 年的证据**。[C-S29]

**未找到可靠来源**：中文投资 / 理财博主在 X 上的公开增长复盘；有明确开通 Premium 前后对照数据的新号复盘。

## 打法评估表

| 打法 | 机制依据（2026 源码 / 官方） | 证据强度 | 风险 |
|---|---|---|---|
| 回复大号（reply guy） | 你没关注的人的回复会被 For You 过滤（C-F7），曝光来自回复区。回复区由 LLM 打分（C-F4），Premium 有回复优先（C-F13）。转化靠点进主页再关注 | 中：机制明确；案例 1、2、5 都是自述 | 高：24 小时回复数、是否粘贴都是模型输入；Premium 用户可以“踩”（C-F8）；低分回复会被打标签（C-F4）；AI 回复工具的 API 已被封（C-F9） |
| 原创帖抓冷启动窗口 | 粉丝 ≤ 5 万的原创帖，发布 2 小时内、曝光 < 200 时，有机会被提到第 15 位左右，按早期点赞率抽样（C-F1） | 强（源码），但扶持力度在实验中 | 低：唯一的“风险”是早期点赞率低，就抽不中 |
| 在垂直圈子形成真实互关 | 互关作者的原创帖“被回复”权重 +15（C-F2） | 强（源码 + 官方文档） | 中：互关对象不真互动就没用；成规模的组织化互关属于违规（C-F11） |
| 互关圈 / 互粉群 / 互赞群 | 官方称群聊协调互动对排名无效（C-F6）；小号之间的互动不计入可信度（C-F5） | 强（官方源码注释） | 高：违反平台操纵政策，可能锁号或封号；有协调垃圾分类器 |
| X Communities | 社群帖子可以出现在主信息流和推荐里（Social Media Today 报道，https://www.socialmediatoday.com/news/x-formerly-twitter-makes-communities-posts-visible/739116/ ，日期未核实，约 2024 年） | 弱：2025–26 年没有找到可靠的效果数据；营销文的“互动 +65%”无出处 | 低 |
| 蹭热点 / 趋势 | 回复和引用权重高（C-F3）；Innmind 称蹭现成热点有效（C-F 案例 5） | 弱到中 | 中：错位流量会带来“不感兴趣 / 静音”负权重（−47.52 / −58.8） |
| Spaces | 只有营销博客的说法（2026 年有发现 Tab、录音、字幕） | 弱：未找到可靠的增长数据 | 低：耗时间 |
| 合作互推 / 名人杠杆 | 被高可信账号转发能抬高 UserCred（C-F5）；Ruby Wang 和 starzq 举例：Ben Averbook 靠 Marc Andreessen 转发涨到 4 万（C-S20） | 中 | 低：付费互推不披露的话，可能涉及其他政策（本次未查） |
| 跨平台导流 | 外站来的用户直接点进帖子，按官方说法不计入排名（C-F6），但可以带来真实关注 | 弱：没有找到 X 端的量化数据 | 低 |
| 买粉 / 自动化刷量 | 明文禁止（C-F11）；买来的粉不会在“首页时间线里”产生有效互动 | 强（规则原文） | 极高：锁号、封号；分成门槛要求 500 名**认证**粉丝，买的粉丝不算 |
| 开 Premium | 官方：回复优先 + 分成资格；Buffer：曝光中位数约为免费账号的 6–15 倍（相关性） | 中（因果关系未确认） | 低：花钱；源码里找不到 For You 乘数 |

## 💡 意外发现与洞见

1. **“新号红利”是写进代码的，但只给原创帖。** 粉丝 ≤ 5 万的作者，原创帖在发布后 2 小时、曝光不到 200 时，有资格被插到第 15 位左右（C-F1）。这和“新号只能靠回复”的流行说法正好相反：回复负责拉人，原创帖负责吃到冷启动扶持，两者要配合，缺一不可。
2. **互关加权的作用对象是“原创帖”，媒体说是“回复区”。** 官方仓库的 diff 显示，+15 加在“预测你会回复互关作者原创帖”的权重上（C-F2）。加在“预测概率”上意味着：互粉群里那种彼此不感兴趣的互关，乘完还是接近 0。
3. **“你今天回了多少条”本身就是 X 回复打分模型的输入。** 还有“这条回复是不是粘贴的”（C-F4）。“日回 200 条”的老攻略，2026 年在算法层面直接对上了风控特征。
4. **官方在代码注释里说：群聊协调互动无效。** “Directly navigating to a post (i.e., coordinating via groupchat) has no ranking impact.”（C-F6）这句可以直接拿来回应中文圈的“互赞群”。
5. **Premium 的价值主要在“回复区 + 可信度 + 变现资格”，For You 主排序代码里没有 Premium 乘数。** UserCred 的 PageRank 把 Premium 和认证账号当作信任种子（C-F5），所以“被 Premium 用户点赞”比“自己开 Premium”更像一个干净的信号。这一点是从源码推断的，**不能说死**。
6. **2026 年 X 对“刷互动产业”连续动手：** 1 月封 InfoFi（C-F10），2 月限制 API 回复（C-F9），3 月上线回复踩（C-F8），8 月开源回复垃圾管线并上线 Under the Hood（C-F4、C-F15）。冷启动叙事应该从“怎么刷”转到“怎么不被判成刷”。
7. **源码里 `enable_author_diversity` 在 home-mixer 的 value_model 配置中为 false**（`home-mixer/scorers/value_model.rs`），但 README 描述有作者多样性衰减。“单作者曝光上限”的话题请负责算法的研究员核对，可能是别的服务（vm-ranker）在做这件事。

## 小结（结论、证据强度、缺口）

**结论**
- 2026 年冷启动的合理组合是：每天少量、高质量地回复同赛道 5K–100K 粉的账号（拉人进主页），加上每天 1–3 条原创帖（吃冷启动扶持，争取早期点赞率），再在小圈子里形成会真实对话的互关（吃 +15 回复加权）。
- 回复要“少而精”：回复数量、是否粘贴、收到的拉黑数都会进入官方回复打分模型。Premium 能放大回复的位置，但不是 For You 曝光的开关。
- 买粉、互粉群、自动化刷量：规则明文禁止，官方也明确说对排名无效，收益为负。
- 阶段指标建议（经验总结，无官方定义）：0–1K 看“主页访问 → 新增关注”的转化率和单条回复带来的主页访问；1K–1 万看原创帖曝光与互动率、互关对象的真实回复率；想变现的话，对照官方门槛（Premium + 3 个月 500 万自然曝光 + 500 名认证粉）。完整看板需要 Premium。

**证据强度**
- 强（A 级源码 / 官方）：冷启动扶持参数、互关加权的对象和数值、动作权重、回复 LLM 打分的输入、群聊互动无效、InfoFi 禁令、API 回复限制。
- 中：Premium 回复优先（官方帮助页摘录）+ Buffer 相关性数据；reply guy 有效性（多个自述案例，口径一致）。
- 弱：Communities、Spaces、蹭热点、跨平台导流的量化效果；主页优化的转化率数字（全是 C 级）。

**缺口**
1. 回复区排序的完整逻辑（Grox 提示词、Premium 回复加权的具体数值）没有开源，“踩”对排序的实际影响也只有官方的定性说法。
2. 中文创作者的增长复盘大多发在 X Article 或知乎，本次没能读到全文（402/403）。@AI_Jasonyu 的数据需要人工核对原文。中文投资类博主案例**未找到可靠来源**。
3. help.x.com 的规则页被 Cloudflare 拦截，规则原文来自搜索摘录，成稿前需要人工打开逐字核对。
4. 没有找到“开 Premium 前后”的单账号对照实验，也没有主页优化的可靠 A/B 数据。
5. 源码参数只是默认值，线上值可能被实验覆盖。冷启动扶持和互关加权都处在分桶实验中。
