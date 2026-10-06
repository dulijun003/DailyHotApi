# B 发帖策略与写法

> 研究日期：2026-10-06 ｜ 研究员：B（发帖策略与内容写法）
> 说明：算法源码细节由另一位研究员负责，本文只在"怎么发、怎么写"需要时引用源码常量，且以本次直接读取到的文件为准。
> 等级：A=一手（官方帮助中心/文档/源码、X 高管或 Musk 原帖）；B=权威媒体或大样本研究报告；C=营销博客、自媒体、交易所快讯（只作线索）。
> 抓取限制：help.x.com、business.x.com 对抓取返回 403/402，相关条目取自搜索引擎摘要，已在表中注明“摘要”，引用前建议人工打开原页复核。

## 来源

| 编号 | 标题 | 机构/作者 | 日期 | 等级 | URL |
|---|---|---|---|---|---|
| B-S1 | Do Posts with Links Affect Content Performance on X? | Buffer / Tamilore Oladipo，数据 Julian Winternheimer | 2025-10-14 | B | https://buffer.com/resources/links-on-x/ |
| B-S2 | Does X Premium Really Boost Your Reach? An Analysis of 18M+ Posts | Buffer / Tamilore Oladipo | 2025-10-02 | B | https://buffer.com/resources/x-premium-review/ |
| B-S3 | The State of Social Media Engagement in 2026 | Buffer | 2026 年初发布（数据 2024-01～2025-12） | B | https://buffer.com/resources/state-of-social-media-engagement-2026/ |
| B-S4 | The Best Time to Post on Twitter/X in 2026: 8.7 Million Posts Analyzed | Buffer / Kirsti Lang | 2026-03-13 | B | https://buffer.com/resources/best-time-to-tweet-research |
| B-S5 | Best times to post on X in 2026 | Sprout Social | 2026-03-31 更新 | B | https://sproutsocial.com/insights/best-times-to-post-on-twitter/ |
| B-S6 | Best time to post on social media（X 部分） | Hootsuite × Critical Truth | 2025-11-19 | B | https://blog.hootsuite.com/best-time-to-tweet/ |
| B-S7 | 2024 X/Twitter Study: Data, Trends, and Best Practices to Grow on X in 2025 | Metricool | 2025 年初（数据 2024 全年） | B（厂商自有数据，相关性分析） | https://metricool.com/twitter-study/ |
| B-S8 | Twitter/X analytics（格式与字数数据） | Ordinal（原 Assembly） | 数据 2024-01～2026-05 | C（厂商客户数据，方法未公开） | https://www.tryordinal.com/blog/twitter-analytics |
| B-S9 | Consistent posting study | Buffer | 2025-01-29 | B | https://buffer.com/resources/consistent-posting-study |
| B-S10 | How to Grow on Social Media in 2026: A Data-Backed Strategy | Buffer | 2026（页面未标具体日） | C（建议性内容，X 频率无数据支撑） | https://buffer.com/resources/creator-growth-playbook |
| B-S11 | x-algorithm README | xAI / X（官方开源仓库） | 2026-01-20 首发，读取于 2026-10-06 | A | https://github.com/xai-org/x-algorithm |
| B-S12 | home-mixer/params/param.rs（权重常量） | xAI / X（官方开源仓库） | 读取于 2026-10-06（main 分支） | A | https://raw.githubusercontent.com/xai-org/x-algorithm/main/home-mixer/params/param.rs |
| B-S13 | Scoring and ranking（第三方文档站对开源代码的解读） | mintlify.wiki | 未标日期 | C | https://mintlify.wiki/xai-org/x-algorithm/pipeline/scoring-and-ranking |
| B-S14 | the-algorithm-ml / recap README（2023 旧版权重） | Twitter（官方开源仓库） | 2023-04-05 | A（历史版本） | https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md |
| B-S15 | X drops year-old link penalty, Musk tells Zuckerberg on platform | PPC Land | 2026-07-30 | B | https://ppc.land/x-drops-year-old-link-penalty-musk-tells-zuckerberg-on-platform/ |
| B-S16 | Even our tech overlords don't know how X works | Straight Arrow News (SAN) | 2026-07-29 | B | https://san.com/cc/even-our-tech-overlords-dont-know-how-x-works-is-there-hope-for-the-rest-of-us/ |
| B-S17 | X product chief denies rumor that link posts are deboosted（含 Bier 原帖链接） | roboin.io | 2025-10-20 | B（引用 A 级原帖） | https://roboin.io/article/en/2025/10/20/x-product-chief-denies-rumor-that-link-posts-are-deboosted/ |
| B-S17a | Nikita Bier 原帖 "Links are not deboosted"（ID 解码时间 2025-10-19 UTC） | Nikita Bier（时任 X 产品负责人） | 2025-10-19 | A | https://x.com/nikitabier/status/1980042761819828393 |
| B-S17b | Nikita Bier 原帖（链接帖体验改版说明，ID 解码时间 2025-10-12 UTC） | Nikita Bier | 2025-10-12 | A | https://x.com/nikitabier/status/1977422602328232415 |
| B-S18 | X is testing a feature that makes it easier to get likes on posts with links | GIGAZINE | 2025-11-05 | B | https://gigazine.net/gsc_news/en/20251105-x-post-url-link |
| B-S19 | X opens Articles to all Premium users | PPC Land | 2026-01-07 | B | https://ppc.land/x-opens-articles-to-all-premium-users-ending-exclusive-pricing-tier/ |
| B-S20 | X wants better writing and it's offering $1 million to prove it | Techloy | 2026-01-20 | B | https://www.techloy.com/x-wants-better-writing-and-its-offering-1-million-to-prove-it.md |
| B-S21 | X Puts $1.05M into Long-Form Content Contest, Winners Revealed | KuCoin 快讯 | 2026-02-04 前后 | C | https://www.kucoin.com/news/flash/x-puts-1-05m-into-long-form-content-contest-winners-revealed |
| B-S22 | Elon Musk's X ends creator revenue sharing: What happens to your payouts? | Gulf News | 2026-08-08 | B | https://gulfnews.com/technology/elon-musks-x-ends-creator-revenue-sharing-what-happens-to-your-payouts-1.500634678 |
| B-S23 | Original Content Rewards Program（帮助中心） | X Help Center | 2026-08（摘要，原页 403） | A（摘要） | https://help.x.com/en/using-x/original-content-rewards |
| B-S24 | X's head of product is leaving the company one year after joining | Engadget；Business Today 同日报道 | 2026-08-06 | B | https://engadget.com/2231302/x-head-of-product-nikita-bier-leaving-the-company-one-year-after-joining/ |
| B-S25 | Are hashtags dead? Elon Musk says 'please stop' using them on X | FOX 5 DC | 2024-12-17 | B | https://www.fox5dc.com/news/hashtags-x-elon-musk-says-please-stop-using-them |
| B-S26 | Elon Musk gets bold font removed from X's main timeline | Deccan Chronicle / Benzinga | 2024-10-01 | B | https://deccanchronicle.com/technology/elon-musk-gets-bold-font-removed-from-xs-main-timeline-1827302 |
| B-S27 | Musk warns Twitter accounts of engagement farming, threatens suspension | Business Today | 2024-04-19 | B | https://businesstoday.in/technology/news/story/musk-warns-twitter-accounts-of-engagement-farming-threatens-suspension-426097-2024-04-19 |
| B-S28 | About Edit post | X Help Center | 摘要（原页 403） | A（摘要） | https://help.x.com/en/using-x/edit-post |
| B-S29 | About different types of posts（longer posts） | X Help Center | 摘要（原页 403） | A（摘要） | https://help.x.com/en/using-x/types-of-posts |
| B-S30 | Counting characters | X Developer Docs | 摘要 | A（摘要） | https://docs.x.com/fundamentals/counting-characters |
| B-S31 | Elon Musk: Grok auto-translates & recommends foreign-language posts | PiunikaWeb | 2026-03-30 | C | https://piunikaweb.com/2026/03/30/elon-musk-grok-auto-translate-recommend-foreign-language-posts-x/ |
| B-S32 | X translation for Japanese users | GIGAZINE | 2026-03-31 | B | https://gigazine.net/gsc_news/en/20260331-x-translation-japanese |
| B-S33 | Elon Musk teases algorithm tweaks（"unregretted user-seconds"） | Business Today；Reclaim The Net | 2025-01-04 | B | https://www.businesstoday.in/technology/news/story/elon-musk-teases-algorithm-tweaks-and-customisable-feeds-see-all-details-459582-2025-01-04 |
| B-S34 | 2026-04 聚合号收益削减报道（"payouts cut to 60%"） | tesorb.com 等（仅搜索摘要） | 2026-04-13 | C（未精读到一手） | https://tesorb.com/command/x/ |
| B-S35 | Do hashtags actually work? data analysis 2026（"1–2 个话题标签多 21% 互动"） | hashtagtools.io | 2026 | C（无方法、无样本） | https://hashtagtools.io/blog/do-hashtags-actually-work-data-analysis-2026 |

---

## 事实卡片

### 一、发帖频率

[B-F1] 官方开源排序代码里有"同作者多帖衰减"：同一次推荐结果里，同一作者第 1 条之后的帖子会被乘上一个递减系数，但有下限（floor），不会降到 0。
- 来源：[B-S11] ｜ 等级 A ｜ 口径：README 原文描述 ｜ 交叉验证：[B-S13]（C，第三方文档站）给出公式 `(1-floor)×decay^position+floor`，示例 decay=0.6、floor=0.2 时第 2/3/4 条分别为 0.68/0.488/0.373。**本次读取的 param.rs [B-S12] 里没有 decay/floor 的具体常量**，示例值只能当作说明用，不能当成线上真实参数。
- 原文关键句："each post after an author's first is multiplied by a decaying factor, down to a floor."
- 对创作者的含义："单作者曝光上限"更准确的说法是**同一位读者的同一次刷新里，你的第 2、3 条会被打折**，而不是"一天超过 N 条就被限流"。短时间内连发多条，就是让自己的帖子在同一批推荐里互相抢位置。

[B-F2] 厂商横截面数据：大号发得多。Metricool 统计全球平均每周 12 条，粉丝最多的一档账号平均每周近 95 条。
- 来源：[B-S7] ｜ 等级 B ｜ 样本：23,561 个账号、2,144,853 条帖子、31,066 条 thread，2024 年数据 ｜ 交叉验证：[B-S3] Buffer 2026 报告也发现"互动前 10% 的账号发帖量显著高于中位数，在 X 这类以文字为主的平台差距尤其大"（未给出具体倍数）。
- 原文关键句："the higher the posting frequency, the larger the account size"
- 对创作者的含义：这是**相关性，不是因果**：大号有团队、有素材，所以发得多。它和 B-F1 并不矛盾：高频账号多出来的曝光主要来自**不同读者、不同时段**，不是同一批人看到更多条。

[B-F3] 未找到 2025–2026 年针对 X 的"发帖频率 → 单帖曝光"大样本研究。Buffer 有 LinkedIn、Instagram 的频率研究，X 没有；它的"坚持发帖"研究（10 万+ 用户、26 周，坚持型的单帖互动是零散型的 5 倍以上）不分平台，统计的是"有发帖的周数"，不是"每周发几条"。
- 来源：[B-S9]、[B-S10] ｜ 等级 B/C ｜ 交叉验证：Sprout [B-S5]、Hootsuite [B-S6] 也只说"时机比频率重要/保持一致"，都没有给出 X 的频率数据。
- 原文关键句：[B-S9] "The highly consistent posters saw more than 5 times the engagement per post compared to those who posted sporadically."
- 对创作者的含义：网上流传的"每天 3–5 条"（Buffer playbook [B-S10]、多家工具博客）属于**经验建议，没有 X 专项数据支撑**。

> **建议区间（推断，证据强度中等偏弱）**：每天 1–3 条主帖（原创帖/长帖/Article），相邻两条间隔几个小时，避免在同一批推荐里互相打折（B-F1）；**回复不限量**，因为回复不进入同作者多帖衰减的那一批主帖排序（这一点还需要算法研究员确认），而且现行变现规则在统计曝光门槛时排除回复（B-F16）。关键是长期稳定地发（B-F3 中"坚持"带来的 5 倍差距），不是单日冲量。

### 二、发帖时间

[B-F4] Buffer 2026（870 万条帖子，指标为互动率，按发帖人当地时间）：单个最佳时段是周二 9:00，其次是周三 10:00 和 9:00；最稳定的窗口是工作日 9–11 点；每天 18–23 点最差；周六最弱。
- 来源：[B-S4] ｜ 等级 B ｜ 样本 8.7M 条（统计区间未披露）｜ 交叉验证：Hootsuite [B-S6]（100 万+ 条帖子、118 国、按时区归一化）给出的 X 最佳时段是周三到周五 9–11 点；Buffer 2026 年度报告 [B-S3] 给出工作日 6–11 点，峰值在周二 9 点。
- 原文关键句："Mid-morning on weekdays, particularly between 9 a.m. and 11 a.m., is the most reliable window for reach."

[B-F5] **冲突**：Sprout Social 2026 认为下午更好，周二到周四 12–18 点最佳，周六最差。
- 来源：[B-S5] ｜ 等级 B ｜ 样本：约 30.7 万个社交账号上近 20 亿次互动，2025-11-27～2026-02-27，按当地时间 ｜ 交叉验证：Metricool [B-S7] 得出"全球 21 点在线用户最多"（衡量的是在线人数，不是互动率）；Ordinal [B-S8]（C）发现周四互动率最高（1.08%），并认为"周二发帖"这条建议在它的数据里不成立。
- 对创作者的含义：几份研究在**哪几天**上一致（周中最好、周六最差），在**几点**上不一致（上午还是下午）。这本来就是不同客户群体的平均值，最终还得看自己后台的粉丝活跃时段。

[B-F6] 跨时区：以上时段**都是受众所在地的当地时间**；面向中文读者的地区性分时数据，未找到可靠来源（只有 opentweet、radaar 一类工具页面给出"北京时间 10–11 点"，没有样本说明，C 级以下，不采用）。
- 来源：[B-S4][B-S5][B-S6] 对时区口径的说明 ｜ 等级 B
- 对创作者的含义（推断）：中文 X 的读者分布在大陆（翻墙用户）、港台、新马和北美华人，几个时区相距 12–16 小时。面向中文读者，可以把大中华区的工作日上午和午休作为主时段；面向英文读者，美东工作日上午 9–11 点相当于北京时间晚上 21–23 点（夏令时）或 22–24 点（冬令时），中文作者在晚间就能发到英文受众的黄金时段。另外，自 2026 年 3 月底起，Grok 会自动翻译外语帖并推荐给其他语言的用户（B-F17），**一条中文帖也可能被推给英文用户**，选时段时要考虑你想让哪一侧的读者先看到。

### 三、内容形式

[B-F7] Buffer 2026 年度报告（X 按格式的中位互动率）：纯文本 3.56% > 图片 3.40% > 视频 2.96% > 链接 2.25%；报告说文本和图片"接近到两者都好用"。
- 来源：[B-S3] ｜ 等级 B ｜ 样本：全平台 5,200 万+ 条帖子、20 万+ Buffer 账号，2024-01～2025-12 ｜ 交叉验证：Buffer Premium 研究 [B-S2]/[B-S1] 同样显示文本互动率最高（Premium 账号：文本约 0.90%、视频约 0.85%、图片约 0.42%、链接约 0.28%）。两份报告的互动率绝对值差一个量级，原因是分母口径不同，**只看排序，不要混用数字**。

[B-F8] Ordinal（87,528 条帖子，2024-01～2026-05）：thread 互动率最高（1.89%），平均曝光 27,508；纯文本平均曝光最高（46,731），但互动率只有 0.67%；视频平均曝光 30,684，互动率最低（0.53%）；图片/GIF 0.99%、13,053；投票 0.89%、3,634；多图 0.72%、12,335；链接 0.68%、9,573。100–200 字符的帖子互动率最高（1.09%），100 字符以下的曝光更高。
- 来源：[B-S8] ｜ 等级 C ｜ 样本 87,528 条（均值，容易被少数爆款拉高）｜ 交叉验证：在"文本曝光高、链接曝光低"这一点上，方向与 [B-S1][B-S3] 一致；"thread 互动率最高"未找到第二个 2025–2026 年的来源（网上流传的"Buffer：thread 比单条高 54% 互动"找不到原始报告，不采用）。
- 对创作者的含义：短文本负责拿曝光，thread、长内容负责拿深度互动，两者分工不同。

[B-F9] X Articles：2026-01-07 起开放给**所有 Premium**订阅者（此前仅限 Premium+、Business、Organizations）；支持标题、加粗、列表、内嵌图片/视频/帖子/链接。
- 来源：[B-S19] ｜ 等级 B（转述 Bier 原帖）｜ 交叉验证：PiunikaWeb、Storyboard18 同日报道。
- 原文关键句（Bier）："we're opening up X Articles to all Premium subscribers."

[B-F10] X 用 $1M 奖金推长文：2026-01 宣布奖励下一个结算周期的 Top Article，要求原创、≥1,000 词、美国用户、Premium，主要按"Verified Home Timeline impressions"评选；2026-02-04 公布结果，总奖金加到 $2.15M。冠军 @beaverd 写的是自建数据库的 Deloitte 政府合同调查，曝光约 4,440–4,500 万；Dan Koe 获 "Creator's Choice" 奖，曝光 1,104 万。
- 来源：[B-S20]（规则，B）、[B-S21]（结果，C）｜ 交叉验证：冠军粉丝数说法冲突（KuCoin 写约 9 万，另一处 HTX 转载写 9k），**曝光数和粉丝数仅 C 级来源，引用时要写"据报道"**。
- 对创作者的含义：**一个中等体量账号，靠独家数据和原创调查拿到了比百万粉大号高 4 倍的曝光**。这是 X 在 2026 年想奖励什么内容的最直接信号（参见 B-F16）。

[B-F11] 原生视频：X 推出了独立的视频 Tab（美国），开源模型的预测目标里有 video quality view、video continuation seconds 等观看信号；但本次读取的 param.rs 里 `VqvWeight = 0.0`，`VideoOpenWeight = 0.07`。
- 来源：[B-S11][B-S12] ｜ 等级 A ｜ 交叉验证：[B-S13]（C）说 VQV 只对超过最低时长的视频生效。
- 对创作者的含义：开源代码里**看不到"视频天然加权"的证据**；视频曝光高（B-F8）更可能来自视频 Tab 和单独的推荐通道，这部分交给算法研究员核实。长视频在 2025–2026 年的覆盖数据：**未找到可靠来源**。

[B-F12] 投票、Spaces：投票只有 Ordinal 的 C 级数据（互动率 0.89%，平均曝光 3,634，各格式中最低）；Spaces 在 2025–2026 年的覆盖或互动数据**未找到可靠来源**。

### 四、外链

[B-F13] Buffer（1,880 万条帖子、7.1 万个账号，2024-08～2025-08）：从 2025 年 3 月起，非 Premium 账号的链接帖中位互动率是 **0%**，Premium 约 0.28%（文本约 0.90%）。非 Premium 账号的中位单帖曝光不到 100，Premium 约 600，Premium+ 超过 1,550，即"约 10 倍"。
- 来源：[B-S1][B-S2] ｜ 等级 B ｜ 交叉验证：Ordinal [B-S8] 的链接帖平均曝光 9,573，约为纯文本 46,731 的 1/5；PPC Land [B-S15] 自测"链接帖少 94% 浏览"（方法未披露，C 级价值）。
- 原文关键句："On X, links are now the weakest format you can publish — especially without Premium."

[B-F14] **官方口径前后矛盾**：
 - 2024 年：Musk 本人承认链接帖覆盖更低（[B-S15] 转述）。
 - 2025-10-12/19：Bier 发帖称"Links are not deboosted"，并解释链接帖互动低是因为用户跳出去看网页后"忘了回来点赞或回复"，系统拿不到信号。之后 X 在 iOS 上改了链接打开体验，浏览网页时底部常驻原帖的点赞/回复/转发栏，2025-10-25 起推到全球 iOS 用户；Substack CEO Chris Best 称"去掉预加载的虚假浏览后，从 X 来的流量仍大幅上升"（GIGAZINE 换算约 4 倍）。
 - 2026-07-28/29：Bier 回复扎克伯格"Hello Mark, you do not need to put the links in replies anymore"；Paul Graham 追问后，Musk 回复"We haven't for over a year."
- 来源：[B-S17][B-S17a][B-S17b][B-S18][B-S15][B-S16] ｜ 等级 A（原帖）+ B ｜ 交叉验证：Musk 所说的"超过一年没降权"倒推是 2025 年年中，与 Buffer 截至 2025-08 链接帖仍是 0% 的数据**时间上重叠，存在冲突**；SAN [B-S16] 指出这一表态没有任何独立数据验证。另外，本次读取的 param.rs [B-S12] 里 `OpenLinkWeight = 0.2`（正值），**没有看到显式的"链接扣分"常量**（不排除存在于别处，交给算法研究员）。
- 对创作者的含义：最合理的解释是**"没有硬性降权"和"链接帖实际表现差"可以同时成立**：读者点出去以后不回来互动，排序模型又按预测互动打分，结果就是链接帖分数低。所以与其纠结链接放正文还是放回复，**更该保证正文本身能独立带来停留和互动**。

[B-F15] "链接放回复区"：Buffer 2025-10 的建议是"不保证有效，但有时能避开分发惩罚"；X 官方 2026-07 明确说"不需要再放回复了"。没有找到 A/B 级的对照实验数据。
- 来源：[B-S1]、[B-S15] ｜ 等级 B/A
- 原文关键句：[B-S1] "Put links in replies instead of the post. While not foolproof, this approach can sometimes avoid the distribution penalty."
- 对创作者的含义：主帖写完整的摘要或观点，**链接放正文、放回复都可以**；真正有用的是让读者不点链接也能拿到价值。需要导流的内容，优先写成 Article，或把要点直接写进长帖。

### 五、变现规则对写法的约束

[B-F16] 2026-08-07 起，X 停止接受"创作者收入分成"的新报名，2026-09-07 原计划停止计收，2026-09-08 起开放"Original Content Rewards"。奖励对象是原创内容（原创报道、分析、评论、本人拍摄的视频/照片、自制的梗图和图表等，帖子、Article、视频、图片都算）；未经实质改造的转发、搬运下载内容不算。收益按认证用户 Home 时间线曝光、内容格式、互动质量、有意义的对话等因素计算。
- 来源：[B-S22]（B）、[B-S23]（A 摘要）｜ **门槛数字冲突**：帮助中心摘要写"500 个认证粉丝 + 过去 90 天 50 万次认证用户 Home 时间线曝光（不含回复）"，Gulf News 写"3 个月 500 万次自然曝光"（旧版收入分成的门槛）。**以帮助中心为准，发布前请人工打开 help.x.com 复核**。
- 原文关键句（X 创作者负责人 Allegra Jacchia，Gulf News 转述）：激励"had become 'misaligned', with some creators reusing content from others to earn payouts rather than producing original material."
- 前情（C 级线索）：2026-04 Bier 宣布聚合号的收益被砍到正常水平的 60% [B-S34]，未读到一手原帖；Bier 已于 2026-08-06 卸任产品负责人，转为顾问 [B-S24]。
- 对创作者的含义：**回复不计入曝光门槛**，搬运和翻译别人的内容拿不到钱。中文圈常见的"搬运英文爆款 + 翻译"打法，在变现上已经失效。

[B-F17] Grok 自动翻译并跨语言推荐：2026-03-30 前后，Musk 宣布 Grok 会自动翻译外语帖并**推荐**给其他语言的用户，帖子顶部显示"Translated from …"，可以点开看原文，用户也可以关掉；4 月推向全球。日本账号的帖子明显被大量推给海外用户。
- 来源：[B-S32]（B）、[B-S31]（C）｜ 交叉验证：两篇报道互相印证；跨语言推荐给中文作者带来多少曝光，**没有量化数据**。
- 对创作者的含义：中文帖子可能被翻译后推给英文用户。写作时少用只有中文语境才懂的梗、谐音和缩写，否则翻译后读者看不懂。这对"中文创作者做英文受众"是一个新的低成本入口（推断）。

### 六、常见操作

[B-F18] 2026 开源权重（param.rs，A）里，与"引用 vs 转发"有关的常量：`QuoteWeight 5.0`、`ReplyWeight 5.0`、`RetweetWeight 1.0`、`FavoriteWeight 0.5`、`ShareViaCopyLinkWeight 20.0`、`ShareViaDmWeight 5.0`、`FollowAuthorWeight 4.0`、`BidirectionalFollowReplyWeightBoost 15.0`、`DwellWeight 0.05`、`ContClickDwellTimeWeight 0.4`；负向：`NotInterestedWeight -47.52`、`MuteAuthorWeight -58.8`、`BlockAuthorWeight -31.2`、`ReportWeight -234.0`。
- 来源：[B-S12] ｜ 等级 A ｜ 读取时间 2026-10-06 ｜ 注意：这些系数乘的是模型预测出的**概率**，各个动作的概率量级差很多，**不能直接说"一个引用 = 10 个赞"**；线上实际权重以 X 内部配置为准。
- 对创作者的含义：引用转发和回复的权重都是普通转发的 5 倍左右，被"复制链接分享"的权重最高。互相关注的人之间的回复有额外加成，所以**在圈子里真实对话**比群发互赞更有价值。负向信号的绝对值很大：被大量"不感兴趣/静音/拉黑"的代价远大于几个赞的收益。

[B-F19] 编辑帖子：Premium 功能，发布后 1 小时内最多改 5 次，帖子会显示已编辑标记和历史版本；thread、回复、投票、置顶帖等不能编辑；只能在发帖的设备上编辑。
- 来源：[B-S28] ｜ 等级 A（摘要）
- 编辑或"删了重发"对分发有什么影响：**未找到 A/B 级来源**。"小改不影响，大改或删帖重发会重置分发"只是营销博客的说法（C），无数据。开源 README 列出了 `PreviouslySeenPostsFilter`（已看过的帖子会被过滤）和 `DropDuplicatesFilter`（多个召回源返回的同一条帖子去重）[B-S11]。删帖重发会生成新 ID，理论上能重新进入推荐，但会丢掉原帖已有的互动，并可能被视为刷屏（推断）。

[B-F20] 话题标签（hashtag）：Musk 2024-12 发帖"Please stop using hashtags. The system doesn't need them anymore and they look ugly"；2025-06 广告中禁用 hashtag（媒体转述）；X 帮助中心建议每条不超过 2 个。
- 来源：[B-S25] ｜ 等级 B（转述 Musk 原帖）｜ 交叉验证：FOX 5 核实发现，Musk 引用的 Grok 截图是被改过的。"1–2 个标签多 21% 互动"[B-S35] **找不到原始研究，不采用**。
- 对创作者的含义：Grok 驱动的推荐靠语义理解内容，标签对分发的增益没有证据；用 0–1 个、只在参与已有话题时使用即可。

[B-F21] 加粗等格式：2024-10-01 Musk 宣布，因为加粗被滥用来"刷互动"，主时间线上不再显示加粗，要点开帖子详情才能看到。
- 来源：[B-S26] ｜ 等级 B ｜ 交叉验证：Twitchy、Benzinga 同日报道。
- 对创作者的含义：在信息流里，**排版靠分行和空行，不要靠加粗**；需要强格式的内容放进 Article。

[B-F22] 长帖展示规则：Premium 用户可以发最多 25,000 字符的长帖，信息流里只显示前 280 字符，后面要点"Show more"展开；字符按加权计数，**中日韩字符每个算 2**，emoji 也算 2，所以 280 的上限大约等于 **140 个汉字**。
- 来源：[B-S29][B-S30] ｜ 等级 A（摘要）｜ 交叉验证：Typefully 字符计数工具说明一致。
- 对创作者的含义：中文长帖的"首屏钩子"只有大约 140 个汉字。点"Show more"本身就是一次点击，展开后的阅读时长对应开源模型里的 click dwell time 信号 [B-S11][B-S12]。

[B-F23] 刷互动的打法有封号风险：Musk 2024-04 发帖"Any accounts doing engagement farming will be suspended and traced to source"；2025-01 Musk 把目标定为"maximize unregretted user-seconds"，并表示要压低负面内容。
- 来源：[B-S27][B-S33] ｜ 等级 B（转述原帖）
- 对创作者的含义："停留时长"指的是**读者不后悔花掉的时间**，靠煽动情绪换来的停留，不在 X 声称要奖励的范围内。

---

## 写法模板（每个注明依据）

> 这些模板是根据下列证据**归纳出来的结构**，没有任何来源对它们做过 A/B 测试，证据强度为"中"。

### 模板 1：140 字钩子长帖（适合 Premium，承担单帖曝光加停留）
```
第 1 行：具体结论或反常识判断（含数字/对象），≤ 140 汉字内说完核心
第 2 行：为什么值得看（读者能得到什么）
——（折叠线 / Show more）——
3–6 个短段：每段一个论点 + 一个证据/例子，段间空行，不用加粗
结尾：一个可回答的具体问题（不是"你怎么看？"式泛问）
```
依据：首屏只显示约 140 个汉字 [B-F22]；点开后的阅读时长有对应的预测信号 [B-F18][B-S11]；100–200 字符的帖子互动率最高、短文本曝光最高 [B-F8]；信息流不显示加粗 [B-F21]；回复权重高，互关用户的回复还有额外加成 [B-F18]，Buffer 数据显示作者在 X 上回复评论约带来 +8% 互动 [B-S3]。

### 模板 2：独家数据 Article + 摘要主帖（承担变现和"原创"信号）
```
Article：标题=具体发现；开头 3 句给结论；正文按"数据来源→发现 1/2/3→方法与局限"组织；图表自制
引流主帖：独立成立的 3–5 条要点摘要（不点开也有价值）+ Article 卡片
发布后 1 小时内：在评论区回应前几条实质性回复
```
依据：X 把 Articles 开放给全部 Premium 并重金奖励 [B-F9][B-F10]，冠军是自建数据的原创调查，账号体量远小于对手 [B-F10]；Original Content Rewards 明确奖励原创分析和自制图表，按认证用户 Home 时间线曝光计算 [B-F16]；链接帖表现差的原因是读者跳出后不回来互动 [B-F14]，所以主帖必须能独立成立。

### 模板 3：Thread 拆解（承担深度互动和收藏）
```
1/ 钩子：一个具体问题或结果 + "下面拆 N 步"
2/–N-1/ 每条一个步骤/案例，单条独立可读（适配单条被转发）
N/ 总结 + 一个可执行清单 + 提问
```
依据：Ordinal 数据中 thread 互动率最高（1.89%）但曝光低于纯文本 [B-F8]（C 级，单一来源）；Metricool 数据显示 thread 在大号中使用普遍 [B-F2]。**注意**：thread 不能编辑 [B-F19]，发前要校对。

---

## 已失效/被证伪的技巧

| 技巧 | 现状 | 依据 |
|---|---|---|
| "回复被作者回复 = 75 倍权重 / 相当于 150 个赞" | 来自 **2023 年旧版** Heavy Ranker 配置（reply_engaged_by_author 75.0）；2026 开源的 param.rs 里**没有这个常量**，回复为 5.0，互关回复加成为 15.0 | [B-S14] vs [B-S12]（A） |
| "转发 ×20、回复 ×13.5"之类简化公式 | 混用了 2023 年旧权重，与 2026 代码不符（2026 年转发 1.0） | [B-S12][B-S14] |
| 链接一律放回复区 | 官方 2026-07 明确说不需要了；实际表现差主要是读者跳出后不回来互动，不是硬性降权 | [B-F14][B-F15] |
| 多打 hashtag 蹭流量 | Musk 公开反对；没有增益证据；"21% 增益"查无出处 | [B-F20] |
| 用加粗/Unicode 粗体做视觉钩子 | 2024-10 起主时间线不显示加粗 | [B-F21] |
| 一天连发 5–10 条刷存在感 | 同一次推荐里同作者第 2 条起被打折；"每天 3–5 条"没有 X 专项数据 | [B-F1][B-F3] |
| 搬运/翻译英文爆款赚分成 | 2026-04 聚合号收益被削（C 级线索），2026-09 起只奖励原创 | [B-F16] |
| 引战、"你同意吗？"式刷回复 | Musk 威胁封号；强负反馈权重（不感兴趣 -47.5、静音 -58.8、举报 -234） | [B-F18][B-F23] |
| 免费账号单靠内容起号 | 非 Premium 中位曝光 <100、中位互动 0%（截至 2025-08） | [B-F13] |

---

## 💡 意外发现与洞见

1. **"外链被压"在官方口径上已经翻案，但数据还没跟上。** Bier（2025-10、2026-07）和 Musk（2026-07）都说没有降权，可 Buffer 截至 2025-08 的数据仍是非 Premium 链接帖 0% 互动。目前也**没有任何 2026 年下半年的独立数据**。文章写"外链被压"时最好改成"外链帖天然吃亏（读者跳出），官方称已不降权"，否则会被读者拿 Musk 原帖反驳。
2. **中文帖首屏只有大约 140 个汉字**（CJK 按 2 计）。这是中文创作者特有的约束，英文写作指南不会提，可以作为文章里一个独特的实操点。
3. **Grok 跨语言自动翻译和推荐（2026-03 起）** 意味着中文创作者的潜在受众不再只限于中文圈。时段选择、用梗和缩写都要考虑译文读者，这可能是 2026 年中文创作者最被低估的变化。
4. **开源权重里"复制链接分享"是 20.0**，在所有正向系数里最高（不过要考虑各动作概率量级不同）。这暗示 X 很看重"值得转发到站外的内容"，清单型、工具型、数据图表型内容可能因此受益（推断）。
5. **2026 年最高 $1M 奖金给了一个靠自建数据做调查的中等账号。** "原创 + 独家数据"打赢了"粉丝量"，这与原创奖励计划的方向完全一致。
6. **关键人员变动**：主导这些规则的产品负责人 Bier 已于 2026-08-06 卸任。他任内的口径（链接、聚合号）后续是否延续还不确定，文章引用时要写明发言人当时的身份和日期。

---

## 小结（结论、证据强度、缺口）

**结论**
1. 频率：没有 X 专项的频率研究；开源代码确认同一次推荐里同作者的多条帖子会递减打折。建议每天 1–3 条主帖、间隔发布、回复不限量，比单日冲量更重要的是长期稳定。（证据：机制 A，建议区间属推断）
2. 时间：周中好、周六差，这一点多源一致（B）；上午还是下午，Buffer/Hootsuite 和 Sprout 结论冲突；都按受众当地时间算。
3. 形式：文本互动率和曝光都领先，图片接近，链接最弱（B，多源）；thread 互动率最高只有单一 C 级来源；Articles 已对全部 Premium 开放，官方重金扶持（A/B），但没有公开的平均表现数据。
4. 外链：数据显示表现差（B），官方称不降权（A），两者有冲突；"放回复区"的效果没有对照数据。
5. 写作：中文首屏约 140 字；不用加粗；以真实对话为目标；原创才能变现。

**证据强度**：时间和形式排序为中高（多个大样本 B 级来源）；频率和外链机制为中（A 级代码或原帖，但缺少效果数据）；写法模板为中低（由机制和数据归纳，没有实验）。

**缺口**
- 2026 年下半年（Musk 表态之后）链接帖 vs 无链接帖的独立对照数据：**未找到**。
- X 专项的"发帖频率 → 单帖/总曝光"大样本研究：**未找到**；author diversity 的线上 decay/floor 参数：**未在 param.rs 中找到**。
- 原生长视频、Spaces、投票在 2025–2026 年的可靠覆盖数据：**未找到**（投票仅有 C 级）。
- Articles 的平均曝光和停留数据：**未找到**（只有奖金案例）。
- 编辑、删帖重发对分发的影响：**未找到** A/B 级来源。
- 中文受众的分时活跃数据：**未找到**可靠来源。
- Original Content Rewards 门槛（50 万 vs 500 万曝光）需人工打开 help.x.com 复核。
