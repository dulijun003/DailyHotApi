# 来源清单：2026 年 X 账号运营实操指南

> 汇总自 research/A–E 五份研究笔记。编号保留各视角前缀（A-S1、B-S1…），全局唯一。等级：A=一手（代码/官方条款/官方帖），B=权威媒体或大样本研究，C=营销博客/自媒体/自述（只作线索）。
> 主编复核：2026-10-06 本地克隆 xai-org/x-algorithm（HEAD e62790c）亲自核对了权重、作者多样性、冷启动参数；OCR 门槛经 TechCrunch/TNW/帮助中心摘要三方一致。help.x.com 全站 403，相关条目为搜索摘要。
> 合计 158 条（含少量跨视角重复）：A 级 58，B 级 58，C 级 42。

## A 算法机制（23 条）

| 编号 | 标题 | 机构/作者 | 日期 | 等级 | URL |
|---|---|---|---|---|---|
| A-S1 | X For You Feed Algorithm – README（当前版） | xAI / X（xai-org） | 2026-10-06 HEAD；Notable Updates 写到 2026-09-18 | A | https://github.com/xai-org/x-algorithm |
| A-S2 | `home-mixer/params/param.rs`（排序权重与参数，含官方注释） | xai-org | 2026-10-06 HEAD（权重首次公开于 2026-08-13） | A | https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs |
| A-S3 | `vm-ranker/params.rs` + `xai-value-model/scoring.rs`（作者多样性、站外折扣、加权公式） | xai-org | 2026-10-06 HEAD | A | https://github.com/xai-org/x-algorithm/tree/main/vm-ranker ；https://github.com/xai-org/x-algorithm/blob/main/xai-value-model/scoring.rs |
| A-S4 | `docs/BIDIRECTIONAL_BOOST_CHANGE.md`（互关加权变更示例 diff） | xai-org | 描述 2026-07-10 / 07-13 / 07-24 的变更 | A | https://github.com/xai-org/x-algorithm/blob/main/docs/BIDIRECTIONAL_BOOST_CHANGE.md |
| A-S5 | `home-mixer/scorers/author_cold_start.rs`（新作者冷启动扶持） | xai-org | 2026-10-06 HEAD（Thompson 采样参数加入于 2026-08-14） | A | https://github.com/xai-org/x-algorithm/blob/main/home-mixer/scorers/author_cold_start.rs |
| A-S6 | `grox/flows/reply_spam/*`（Grok 回复排序打分器，prompt 未公开） | xai-org | 2026-10-06 HEAD | A | https://github.com/xai-org/x-algorithm/tree/main/grox/flows/reply_spam |
| A-S7 | `abuse-enforcement-service/service-lib/rules/*.yaml` + `visibility-filtering/rules/*` | xai-org | yaml 注明 "last sync 2026-08-26" | A | https://github.com/xai-org/x-algorithm/tree/main/abuse-enforcement-service ；https://github.com/xai-org/x-algorithm/tree/main/visibility-filtering |
| A-S8 | `user-cred-v2/`（账号信誉 PageRank） | xai-org | 2026-10-06 HEAD | A | https://github.com/xai-org/x-algorithm/tree/main/user-cred-v2 |
| A-S9 | `phoenix/README.md`（Phoenix 召回/排序模型说明） | xai-org | 2026-10-06 HEAD | A | https://github.com/xai-org/x-algorithm/blob/main/phoenix/README.md |
| A-S10 | 首个提交 `aaa167b` 的 README（2026-01-20 原始版） | xai-org | 2026-01-20 | A | https://github.com/xai-org/x-algorithm/commit/aaa167b |
| A-S11 | X open sources its algorithm while facing a transparency fine and Grok controversies | TechCrunch | 2026-01-20 | B | https://techcrunch.com/2026/01/20/x-open-sources-its-algorithm-while-facing-a-transparency-fine-and-grok-controversies |
| A-S12 | Researchers label recent X algorithm release as a redacted version | Dataconomy（引 Cornell / Graz / CMU 学者） | 2026-02-05 | B | https://dataconomy.com/2026/02/05/researchers-label-recent-x-algorithm-release-as-a-redacted-version/ |
| A-S13 | X will prioritize replies from people you follow | Engadget | 2026-07-14 | B | https://engadget.com/2214455/x-will-prioritize-replies-from-people-you-follow |
| A-S14 | X drops year-old link penalty, Musk tells Zuckerberg on platform | PPC Land | 2026-07-30 | B/C | https://ppc.land/x-drops-year-old-link-penalty-musk-tells-zuckerberg-on-platform/ |
| A-S15 | X says link deboosting is a myth（含 Nikita Bier 原帖链接） | Roboin | 2026-04-13 | C（追溯到 A：x.com/nikitabier/status/2043428612108644848） | https://roboin.io/article/en/2026/04/13/x-denies-link-deboost-recommends-in-post-links/ |
| A-S16 | X Just Added a Thumbs Down Button for Replies / X to roll out dislike button | Hongkiat；Siasat | 2026-03-18 | C（Hongkiat 引用 x.com/grok/status/2034370218911211616，未能直接打开核实） | https://www.hongkiat.com/blog/x-thumbs-down-replies/ ；https://www.siasat.com/x-to-roll-out-dislike-button-following-hint-from-product-head-3437268/ |
| A-S17 | the-algorithm-ml：Heavy Ranker README（2023 年旧版权重） | Twitter | 2023-04-05 权重 | A（旧版） | https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md |
| A-S18 | the-algorithm：`HomeGlobalParams.scala` @ `ef4c5eb`（2023 年蓝 V 乘数） | Twitter | 2023-03-31 | A（旧版） | https://github.com/twitter/the-algorithm/blob/ef4c5eb/home-mixer/server/src/main/scala/com/twitter/home_mixer/param/HomeGlobalParams.scala |
| A-S19 | Does X Premium Really Boost Your Reach? An Analysis of 18M+ Posts | Buffer | 2025-10-02 | B/C（数据研究，相关性） | https://buffer.com/resources/x-premium-review/ |
| A-S20 | X switching to fully AI-powered Grok algorithm | Social Media Today（引 Musk 帖） | 2025-10-19 | B | https://socialmediatoday.com/news/x-formerly-twitter-switching-to-fully-ai-powered-grok-algorithm/803174 |
| A-S21 | Are hashtags dead? Elon Musk says 'please stop' using them | FOX 5 DC | 2024-12-17 | B | https://www.fox5dc.com/news/hashtags-x-elon-musk-says-please-stop-using-them |
| A-S22 | X algorithm "Under the Hood" transparency（8 月更新解读） | XenoSpectrum | 2026-08-13 | C | https://xenospectrum.com/en/x-algorithm-under-the-hood-transparency/ |
| A-S23 | 2023 版 `ScoredTweetsParam.scala`（作者多样性 0.5/0.25、站外 0.75） | Twitter | 2023（main 分支） | A（旧版） | https://github.com/twitter/the-algorithm/blob/main/home-mixer/server/src/main/scala/com/twitter/home_mixer/product/scored_tweets/param/ScoredTweetsParam.scala |

## B 发帖策略与写法（37 条）

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

## C 冷启动与涨粉（30 条）

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

## D 变现路径（32 条）

| 编号 | 标题 | 机构/作者 | 日期 | 等级 | URL |
|---|---|---|---|---|---|
| D-S1 | Original Content Rewards Program（官方长文，全文已读） | X / @XCreators | 2026-08-07 21:06 UTC | A | https://x.com/XCreators/status/2085835082166653393 |
| D-S2 | Original Content Rewards Program Terms（Effective: August 7, 2026，全文已读） | X Corp（legal.x.com） | 2026-08-07 | A | https://legal.x.com/en/original-content-rewards-terms.html |
| D-S3 | Original Content Rewards（帮助中心，直连 403，仅搜索索引摘要） | X 帮助中心 | 2026-08 后（页面无可见日期） | A（间接获取） | https://help.x.com/en/using-x/original-content-rewards |
| D-S4 | Creator Revenue Sharing（帮助中心，直连 403，仅搜索索引摘要） | X 帮助中心 | 未知 | A（间接获取） | https://help.x.com/en/using-x/creator-revenue-sharing |
| D-S5 | About Creator Subscriptions / About Subscriptions（直连 403，仅搜索索引摘要） | X 帮助中心 | 未知 | A（间接获取） | https://help.x.com/en/using-x/subscriptions-creator |
| D-S6 | "Starting today, U.S. payouts for Original Content Rewards and Subscriptions will be paid through @XMoney" | X / @XCreators | 2026-09-02 01:25 UTC | A | https://x.com/XCreators/status/2094959821782983076 |
| D-S7 | "2026 is the year of the creator on 𝕏…highest payouts since our monetization program launched" | X / @XCreators | 2026-01-16 | A | https://x.com/XCreators/status/2012253925202919521 |
| D-S8 | "We're giving $1 million to the Top Article of the next payout period"（被 Musk 引用） | X / @XCreators；@elonmusk | 2026-01-16 / 01-17 | A | https://x.com/elonmusk/status/2012350620045287714 |
| D-S9 | 本地区曝光加权公告 | Nikita Bier（X 产品负责人） | 2026-03-25 00:36 UTC | A | https://x.com/nikitabier/status/2036603028619534564 |
| D-S10 | "We will pause moving forward with this until further consideration" | Elon Musk | 2026-03-25 06:03 UTC | A | https://x.com/elonmusk/status/2036685311179477401 |
| D-S11 | X replaces 'misaligned' revenue sharing program with Original Content Rewards | TechCrunch | 2026-08-08 | B | https://techcrunch.com/2026/08/08/x-replaces-misaligned-revenue-sharing-program-with-original-content-rewards/ |
| D-S12 | X says it's reducing payments to clickbait accounts | TechCrunch | 2026-04-12 | B | https://techcrunch.com/2026/04/12/x-says-its-reducing-payments-to-clickbait-accounts/ |
| D-S13 | X shifts US creator payouts from Stripe to X Money | TechCrunch | 2026-09-02 | B | https://techcrunch.com/2026/09/02/x-shifts-us-creator-payouts-from-stripe-to-x-money/ |
| D-S14 | X awards $1 million prize to creator with history of racist posts | NBC News | 2026-02-07（据抓取摘要） | B | https://www.nbcnews.com/tech/internet/x-pays-1-million-prize-creator-history-racist-posts-rcna257768 |
| D-S15 | X Awards $1M To Top Article for January | Social Media Today | 2026-02-04 | B- | https://www.socialmediatoday.com/news/x-awards-1-million-to-top-article-for-january/811396/ |
| D-S16 | X doubles creator revenue pool and offers $1M for top Article | PPC Land | 2026-01 | C | https://ppc.land/x-doubles-creator-revenue-pool-and-offers-1m-for-top-article-but-why/ |
| D-S17 | X 将美国创作者收益结算从 Stripe 迁移至 X Money | 腾讯新闻（至顶科技） | 2026-09-03 | B-（中文转述） | https://news.qq.com/rain/a/20260903A09VL600 |
| D-S18 | "𝕏 will no longer take a 10% cut of a creator's subscription revenue once a creator has earned over $100,000" | Sawyer Merritt（非官方大V） | 2026-05-03 | C | https://x.com/SawyerMerritt/status/2050794317849964931 |
| D-S19 | X's revenue shake-up: Localizing creator earnings… | tech-ish | 2026-03-25 | C | https://tech-ish.com/2026/03/25/x-revenue-shake-up-localizing-creator-earnings-or-killing-the-global-town-square/ |
| D-S20 | 推特工资与 X 创作者收益排行榜（收录公开帖子自报收益） | @imfycc | 抓取于 2026-10-06（周期 2025-12 至 2026-08） | C（自报汇总） | https://payouts.solox.dev/ |
| D-S21 | "11月9日推特发放了最新一期创作者收益，中文区好惨……" | @0xNathanWalk | 2024-11-11 | C（自述/转述） | https://x.com/0xNathanWalk/status/1855796409896927233 |
| D-S22 | 玩推特有多少种赚钱的途径（长文） | @MYohei707 | 2026-05-01 | C | https://x.com/MYohei707/article/2050099966044160069 |
| D-S23 | X 创作者变现：大陆身份开通 Stripe 全攻略（2026 实操版） | @makai1201 | 2026-01-09 | C | https://x.com/makai1201/status/2009469469664661619 |
| D-S24 | 2026 X Creator Revenue Complete Guide（转载 @AI_Jasonyu 长文） | YouMind / @AI_Jasonyu | 2026-02-15 | C | https://youmind.com/landing/x-viral-articles/x-creator-revenue-guide-2026 |
| D-S25 | The State of Paid Newsletters 2026 | beehiiv（平台一手数据，但属利益相关方） | 2026-06-22 | B-/C | https://www.beehiiv.com/blog/the-state-of-paid-newsletters-2026 |
| D-S26 | 2025 年 Twitter/X KOL 营销完整指南 | Foresight News / ChainPeak 品牌营销 | 2025-06-11 | C | https://foresightnews.pro/article/detail/86096 |
| D-S27 | Everything you need to know about X's original content rewards program | @AIFutureVine | 2026-08-10 | C | https://x.com/AIFutureVine/article/2086769091667193879 |
| D-S28 | X Money is becoming mandatory: what changes for US creators | ValueYourNetwork | 2026-09 | C | https://www.valueyournetwork.com/en/x-money-creators-us/ |
| D-S29 | Pat-Mario Chinweike: 最低提现 $30 / 每两周经 Stripe | @Mario_Sneh | 2026-01-16 | C | https://x.com/Mario_Sneh/status/2012304226265776544 |
| D-S30 | Cross-border payouts（Stripe 文档） | Stripe | 抓取于 2026-10-06 | A（Stripe 一手） | https://docs.stripe.com/connect/cross-border-payouts |
| D-S31 | Twitter/X 影响者报价（汇总类搜索结果：influencerfee / infloq / hootsuite 等） | 多家营销博客 | 2026 | C | https://influencerfee.com/blog/twitter-x-influencer-pricing/ |
| D-S32 | Links no longer deboosted / 外链降权已取消（Bier、Musk 表态的媒体转述） | Social Media Today / freepressjournal 等 | 2026-07-28 前后 | C（未读到原帖） | https://www.socialmediatoday.com/news/x-formerly-twitter-testing-links-in-app-link-post-penalties/803176/ |

## E 语言选择与 AI 运营（36 条）

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

