# A 算法机制

> 研究日期：2026-10-06。核心一手证据来自本地克隆的 `github.com/xai-org/x-algorithm`（HEAD = `e62790c`，提交日期 2026-10-06，共 43 个提交），所有代码引用均为当天 main 分支的实际内容。注意：仓库的默认参数会被 X 用定时脚本同步成"主要生产值"，但实验流量可能不同（见 A-F17）。

## 来源

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

---

## 事实卡片

### 一、仓库与时间线

[A-F1] 2026 版 X 推荐算法开源在 `github.com/xai-org/x-algorithm`（不是 2023 年的 `twitter/the-algorithm`），首个提交 2026-01-20，此后 2026-05-15、2026-08-13 为两次大更新，8 月中旬起几乎每个工作日都有同步提交（截至 10-06 共 43 个提交）。
- 来源：[A-S1][A-S10]（git log 实测）｜等级 A｜交叉验证：[A-S11] TechCrunch 报道 1 月 20 日发布，一致
- 原文关键句："This repository contains the core code that determines which posts a viewer sees in the **For You** feed on X."（A-S1）
- 规模：5-15 提交 "187 files changed, 18263 insertions"；8-13 提交 "2053 files changed, 363246 insertions"（git 实测，与 [A-S22] 报的 "added 363,246 lines" 一致）。
- 对创作者的含义：引用"开源算法"时必须分清版本。网上大量 "reply = 13.5、作者回复 = 75、蓝 V 4 倍" 等数字来自 2023 年旧仓库，不能当成 2026 年的规则。

[A-F2] 1 月版并没有公开权重数值：首个提交里 `weighted_scorer.rs` 引用了 `p::FAVORITE_WEIGHT` 等常量，但 `params` 模块不在仓库内。具体权重直到 2026-08-13 才随 `param.rs` 公开。
- 来源：[A-S10]（`git show aaa167b`，仓库中无任何 params 文件）、[A-S1]（"August 13th, 2026 … Adds key configuration parameters (including weights used to blend predicted action values into a score for a post)"）｜等级 A｜交叉验证：[A-S12] 学者 2 月批评 "omits key details such as interaction weightings"，一致
- 对创作者的含义：2026 年 1 月到 8 月之间自称"根据开源代码算出权重"的营销文章，数字都不可能来自 2026 版代码。

[A-F3] 1 月版 README 说排序模型是"Grok-based transformer"，代码移植自 Grok-1 开源实现，并称"We have eliminated every single hand-engineered feature and most heuristics"。8 月起 Phoenix 换成"生产实现本身"（JAX 训练 + Rust 服务），不再是 Grok-1 示例移植版。
- 来源：[A-S10][A-S9]｜等级 A｜交叉验证：[A-S20] Musk 2025-10 发帖称"aiming for deletion of all heuristics within 4 to 6 weeks. Grok will literally read every post and watch every video (100M+ per day)"，方向一致
- 原文（A-S9）："Earlier releases shipped a sample transformer ported from the Grok-1 open source release … This release ships the **production implementation itself**"
- 对创作者的含义："Grok 驱动"准确的说法是：排序模型用 Grok 系的 transformer 架构，读取用户历史互动序列来预测行为；另外 Grok 大模型（Grox）负责内容理解、打标签和回复排序（见 A-F12、A-F13）。"Grok 会逐条读你的帖子打分决定推不推"只对了一部分，不能照字面理解。

### 二、架构

[A-F4] 流水线顺序：查询补全（用户近期互动序列、关注、屏蔽/静音、已看过的帖子）→ 并行召回【站内 Thunder（关注的人的近期帖子）+ 站外 Phoenix 双塔召回 + SimClusters】→ 候选补全 → 打分前过滤 → Phoenix 打分 → 加权合成 + 作者多样性 + 站外折扣 + 新作者扶持 → VMRanker（DPP 多样性重排）→ Top-K → 可见性过滤（VF）→ 与广告、推荐关注等混排。
- 来源：[A-S1]｜等级 A｜交叉验证：[A-S9]（双塔召回 → transformer 排序）一致
- 原文："Both are ranked together by the same model. **Phoenix** reads the viewer's recent engagement history and predicts, for each post, how likely the viewer is to take each action on it."
- 对创作者的含义：关注你的人和陌生人看到你，走的是两条召回路，但用同一个模型排序。粉丝少的号主要靠站外召回，召回依据是帖子内容的语义 ID 和作者，与"标签"无关（见 A-F18）。

[A-F5] Phoenix 排序模型的候选输入是：帖子哈希、作者哈希、语义 ID（由帖子多模态 embedding 量化得到）和上下文特征（时区、当地小时、产品界面、帖龄）。用户侧输入包括历史互动序列、停留时长，以及画像特征（国家、语言、位置、性别、年龄段、已安装 App）。代码里没有"作者是否认证/Premium"这一类候选特征。排序时候选帖之间互相不可见（candidate isolation）。
- 来源：[A-S9]｜等级 A｜单源（官方代码文档）
- 原文："history and candidate positions carry semantic-ID embeddings and context features (timezone, local hour-of-day, product surface, post age)"
- 对创作者的含义：发帖时间和帖龄会作为模型特征起作用，但不存在写死的"黄金时间"规则。哪个时段好，取决于你的受众在那个时段的互动历史。

### 三、预测的互动与权重（2026-10-06 生产默认值）

[A-F6] Phoenix 预测的行为分五类：互动（点赞、回复、转发、引用、分享、私信分享、复制链接分享）、点击（帖子、主页、链接、展开图片、打开视频、被引用帖）、注意力（视频质量观看、停留、停留时长、点击后停留时长、视频续看秒数、主页停留秒数）、关注作者、负反馈（不感兴趣、静音作者、屏蔽作者、举报、未停留）。最终分 = Σ 权重 × 预测概率。
- 来源：[A-S1][A-S3]｜等级 A｜交叉验证：[A-S10] 1 月版公式相同
- 原文："Final Score = Σ (weight_i × P(action_i))"

[A-F7] 当前生产默认权重（`param.rs`，与 `vm-ranker/params.rs` 一致）：
| 行为 | 权重 | | 行为 | 权重 |
|---|---|---|---|---|
| 点赞 favorite | 0.5 | | 复制链接分享 share_via_copy_link | **20.0** |
| 回复 reply | 5.0 | | 私信分享 share_via_dm | 5.0 |
| 互关作者原创帖的回复（加成后） | 5.0 + **15.0** = 20.0 | | 分享 share | 2.0 |
| 转发 retweet | 1.0 | | 关注作者 follow_author | 4.0 |
| 引用 quote | 5.0 | | 点击后停留时长 cont_click_dwell_time | 0.4 |
| 点击 click | 0.3（9-29 由 0.4 下调） | | 停留 dwell | 0.05（8-25 由 0 上调） |
| 打开链接 open_link | 0.2 | | 停留时长 cont_dwell_time | 0.004 |
| 打开视频 video_open | 0.07 | | 展开图片 photo_expand | 0.05 |
| 视频质量观看 vqv | **0.0**（8-25 由 0.05 下调） | | 主页点击 profile_click | 0.0 |
| 不感兴趣 | −47.52 | | 静音作者 | −58.8 |
| 屏蔽作者 | −31.2 | | 举报 | −234.0 |
| 未停留 not_dwelled | −0.02 | | | |
- 来源：[A-S2][A-S3]；变更日期来自 `git log -p home-mixer/params/param.rs`｜等级 A｜交叉验证：[A-S22] 和多家媒体（8-14）报道的 0.5/5.0/1.0/20.0/4.0/−234 一致
- 对创作者的含义：按权重看，最值钱的是让人愿意复制链接转发出去、回复、引用和私信分享的内容（权重 5–20），点赞只有 0.5，转发只有 1.0。"求转发"式运营收益很低。负反馈的权重很大（−31 到 −234），引战、标题党一旦让人点"不感兴趣"或静音，代价远大于多拿几个赞。

[A-F8] 官方明确说权重乘的是"该用户做出该行为的预测概率"，不是原始计数。"1 次举报抵消 468 个赞"（234 ÷ 0.5）的读法是错的；举报的基础概率比点赞低 1000 倍以上，所以给了大权重。另外，只有在 Home 时间线里被推送到的帖子上发生的行为才计入；直接点链接进入帖子去互动（比如群聊组织刷量）对排序没有影响。
- 来源：[A-S2]（代码注释）、[A-S1]（8-14 Notable Updates）｜等级 A｜单源（官方自述，无法独立验证）
- 原文："it'd be incorrect to see that a report has 468 times higher weight than a like and conclude that e.g. '1 report cancels out 468 likes'"；"Directly navigating to a post (i.e., coordinating via groupchat) has no ranking impact."
- 对创作者的含义：社群互刷、群里发链接让大家去点赞，按官方说法对 For You 排序无效。权重也不能拿来做"多少个赞抵一次举报"的换算。

### 四、排序后调整

[A-F9] 作者多样性衰减：同一次推荐请求里，同一作者的帖子按分数排序后，第 k 条（k 从 0 开始）乘以 (1−0.25)×0.5^k + 0.25，即第 1 条 ×1.0、第 2 条 ×0.625、第 3 条 ×0.4375、第 4 条 ×0.344，最低降到 ×0.25。
- 来源：[A-S3]（`AuthorDiversityDecay=0.5`、`AuthorDiversityFloor=0.25`、`diversity_multiplier` 公式）｜等级 A｜交叉验证：[A-S23] 2023 版同样是 decay 0.5 / floor 0.25，机制延续
- 对创作者的含义：衰减只发生在同一个用户的同一次刷新里，不是"每天发超过 N 条就限流"。短时间连发多条，同一个粉丝一次刷新里只能看到你分数最高的那条，后面几条会被打折。代码里找不到日更上限。

[A-F10] 站外折扣：粉丝以外的人看到你的帖子时，分数 ×0.75（Topic 场景 ×0.5）。关注者看到的你的回复和转发同样 ×0.75。另外，`OONRetweetReplyFilter` 会把"非关注账号的转发和回复"直接从 For You 移除。
- 来源：[A-S3]（`OonWeightFactor=0.75`、`TopicOonWeightFactor=0.5`、`EnableOonRescoreForInNetworkRepliesRetweets=true`）、[A-S1]（过滤器表）｜等级 A｜交叉验证：[A-S23] 2023 版 `OutOfNetworkScaleFactorParam=0.75`，一致
- 对创作者的含义：要拿到站外推荐，必须发原创帖。你在别人帖子下的回复，不会作为独立内容推给不关注你的人。

[A-F11] 互关加成（"Bidirectional follow boost"）：当帖子作者与观看者互相关注，且帖子是原创（不是回复、不是转发）时，回复预测的权重从 5 提到 20（加 15）。时间线：2026-07-10 开始 A/B 测试（5/10/15/20）；07-13 对大量用户上线 20；07-24 因世界杯期间用户反馈看不到足够多的站外讨论，下调到 15。
- 来源：[A-S4][A-S2]｜等级 A｜交叉验证：[A-S13] Engadget 2026-07-14 报道 Nikita Bier 宣布，Bier 原帖 https://x.com/nikitabier/status/2076747704248758617 （A-S4 中给出）
- 冲突说明：媒体（Engadget、Gigazine）把这次改动描述成"回复区优先显示互关的人"，但开源代码里的实现是 For You 排序中加大互关作者原创帖的回复权重。回复区排序可能另有改动，不在本仓库。写作时建议写成"互关好友的原创帖在 For You 里更靠前"，回复区部分标注为"官方口径"。
- 原文（A-S4）："the bidirectional follow boost boosts original posts from people you mutually follow by increasing the weight on the predicted probability that you'll reply to a post from one of those authors who you mutually follow."
- 对创作者的含义：和同领域创作者真实互关、形成会互相回复的圈子，现在有代码层面的收益（回复项是原来的 4 倍）。但只对原创帖生效，而且需要对方确实可能回复。

[A-F12] 新作者冷启动扶持：每次请求最多扶持 1 条帖子。条件是原创（非回复、非转发）、作者粉丝 ≤ 50,000、发布 ≤ 2 小时、在 Home 的曝光 < 200、不在本次排序的最后 3%。从合格的帖子里用 Thompson 采样（Beta 先验 α=0.75、β=49.25，约等于假设 1.5% 点赞率，再用实际"点赞数/首页曝光"更新）选出一条，抬到第 15–16 位。
- 来源：[A-S5][A-S2]（`ColdStartFollowerCap=50000`、`ColdStartMaxPostAgeSecs=7200`、`ColdStartImpressionThreshold=200`、`ColdStartSlotMin/Max=15/16`）｜等级 A｜交叉验证：[A-S1] "New-Author Boost: posts from authors whose impressions are below a threshold are lifted toward a target position"，一致
- 注意：代码里有作者/观看者分组（Treatment/Control/Holdout），说明这个功能还处于实验或分组状态，不一定对所有人生效。
- 对创作者的含义：粉丝不到 5 万的号，每条原创帖在发布后 2 小时、首页曝光前 200 次内有一次被"试推"的机会，前 200 次曝光的点赞率决定它会不会被选中。这是"发帖初期表现很关键"在代码里唯一明确的依据，窗口是 2 小时和 200 次曝光，不是 30 分钟。

[A-F13] 时效：所有候选帖超过 48 小时就被 `AgeFilter` 过滤掉（`MAX_POST_AGE = 48*60*60`），SimClusters 来源同样是 48 小时上限。没有显式的时间衰减公式，帖龄作为模型特征参与预测。
- 来源：[A-S1][A-S2]（`home-mixer/params/config.rs`）｜等级 A｜单源
- 对创作者的含义：在 For You 里，一条帖子最长只有 48 小时的推荐寿命。

### 五、Grok 大模型在哪里起作用（Grox / 标签 / 回复排序）

[A-F14] 回复排序：Grox 用 Grok 4 mini（备用 Grok 4.1 fast）给回复打 0–3 分，结果写入存储，用于回复排序。只有当被回复的帖子或楼主的粉丝数 > 250,000 时才启用（`GROK_GEMMA_FOLLOWER_SPLIT = 250_000`，否则记为 "low_blast_radius" 跳过）。模型能看到的信号包括：回复者粉丝数、过去 24 小时回复数、过去 24 小时收到的有效屏蔽数、是否有风险安全标签、是否缺少客户端事件，以及"回复是否为粘贴"（`Reply Was Pasted`）。打分 prompt 未公开。
- 来源：[A-S6]｜等级 A｜单源（代码可证，但 prompt 和阈值是否为真实生产值无法核实；同仓库 yaml 里部分阈值明确写了"mock value"）
- 原文（prompts.py）："As stated in README for the open source repo, prompts are excluded to reduce gameability of the system."
- 对创作者的含义：在大 V（25 万粉以上）帖子下"抢热评"时，复制粘贴的回复、24 小时内刷大量回复、经常被人屏蔽，都是 Grok 判分时能看到的信号。AI 批量生成再粘贴的评论最容易被压到下面。

[A-F15] "AI 水文"（LLM slop）惩罚：执法规则中，账号被打上 `llm_slop_user` 分数标签后，会被加上 `SpamHighRecall` 用户标签，TTL 2,592,000,000 ms = 30 天；帖子被打上 `llm_slop_post` 后加上 `RiskyHighVizReply` 标签。可见性过滤规则里，`SpamHighRecall` 只在"推荐给非关注者"的场景下直接 DROP，关注者照常能看到。
- 来源：[A-S7]（`enforcement_user.yaml`、`enforcement_post.yaml`、`visibility-filtering/rules/author_rules.rs`、`registry.rs`）、[A-S1]（"Some rules drop a post only when it is a recommendation from an account the viewer does not follow — spam caught at high recall, for instance. The same post is allowed to a follower."）｜等级 A｜单源
- 局限：yaml 里粉丝数豁免阈值写的是 "Prod uses a different follower count floor; this is a mock value"，所以多少粉丝以上可以豁免并不知道。
- 对创作者的含义：靠 AI 批量产出的账号，一旦被打标签，30 天内基本拿不到站外推荐，只剩粉丝能看到。这与 9 月起变现只奖励原创的方向一致。可以用官方 "Under the Hood" 工具（https://x.com/i/jf/under_the_hood ，试点中）自查账号有没有被打可见性标签。

[A-F16] 账号信誉 user-cred-v2：在关注图和互动边上跑 PageRank，得分 0–100（165.2 + 7.07×ln(mass)）。PageRank 的均匀先验种子只发给 Premium/认证账号（`isPremium` = 蓝/灰/金标、认证组织及其关联账号）。这个信誉分在执法服务里用于豁免（`cred.is_high || cred.score >= 50.0` 时跳过部分自动处罚），不是 For You 的排序乘数。
- 来源：[A-S8][A-S7]｜等级 A｜单源
- 对创作者的含义：Premium 在 2026 代码里没有直接的曝光乘数，但会间接提高账号信誉，减少被自动反垃圾规则误伤的概率。这是"Premium 有用"在代码里能找到的唯一依据。

### 六、透明度与局限

[A-F17] 官方承认三类"不在仓库里"的内容：Grox 的 LLM prompt、部分 botmaker 规则、部署相关代码。生产默认值由定时脚本同步进代码，但实验参数可能不同；官方只承诺"占 10% 以上流量"的实验会在仓库中可见。
- 来源：[A-S1]｜等级 A｜交叉验证：[A-S22] 一致
- 原文："we run cron scripts that set the defaults in this repository's code to be the primary production values"；"Our aim is for experiments running at a notable share of traffic — e.g. 10% or more — to be visible in this repository."
- 对创作者的含义：代码给出的是机制和默认值，任何"精确到小数点的爆款公式"都不成立。Phoenix 预测的概率由模型决定，外人无法复现生产权重下的具体分数。

[A-F18] 学界批评（针对 1 月版）：Cornell 的 John Thickstun 认为发布代码只是给人一种透明的假象，大量决策发生在黑箱神经网络里；Graz 大学的 Ruggero Lazzaroni 指出缺少运行算法所需的训练好的模型；CMU 的 Mohsen Foroughifar 要求公开训练数据。
- 来源：[A-S12]｜等级 B｜交叉验证：[A-S11] TechCrunch 提到 2023 版也被批"transparency theater"
- 原文："What troubles me about these releases is that they give you a pretense that they're being transparent for releasing code…"（Thickstun）
- 说明：8 月更新后补上了权重、训练代码和合成数据，但生产模型参数（checkpoint）和真实训练数据仍未公开（[A-S9]："there is no checkpoint or corpus bundle to fetch"）。5 月版曾经通过 Git LFS 发过一个约 3 GB 的 mini 演示模型，8 月被训练代码取代。

### 七、2026 年规则变化（官方口径）

[A-F19] 回复"踩"（thumbs-down）：约 2026-03-18 开始灰度，只针对回复，不公开计数，作者不会收到通知。最早向认证/Premium 用户和移动端推出。起因是 Nikita Bier 回复用户建议说 "Give me 60 seconds"。
- 来源：[A-S16]（Hongkiat、Siasat，都是 2026-03-18）｜等级 C（追溯到 @grok 帖，未能直接打开）｜交叉验证：开源代码里有 `ReplyDownVote`（`visibility-filtering/params/limited_actions_policy.rs`）和 Thunder schema 的 `downvoted` 字段，功能确实存在。但 For You 的 Phoenix 行为列表里没有"downvote"这一项，它具体如何影响回复排序，代码层面看不到。
- 冲突说明：Siasat 写"No official statement from X has been released"，说它影响排序只是"unconfirmed"。
- 对创作者的含义：在热帖下发低质、引战或 AI 味很重的回复，可能被私下踩而沉底。它对回复区的影响强度未经证实，写作时应写"据报道"。

[A-F20] 互关加权（2026-07）：见 A-F11。日期以 A-S4 为准（07-10 测试、07-13 上线 20、07-24 改为 15），Engadget 报道日期为 07-14。
- 等级 A + B 双源一致。

---

## 流行说法核查表

| 说法 | 结论 | 依据 |
|---|---|---|
| "回复权重 13.5、作者回复你的回复 = 75（= 150 个赞）" | **错误（张冠李戴）** | 这是 2023-04-05 旧版 Heavy Ranker 的权重 [A-S17]。2026 版回复权重是 5.0，互关原创帖加成后 20.0，没有"作者回复"这一项 [A-S2]。部分营销博客把它说成"2026 年 1 月开源代码确认"，而 1 月版根本没公开权重 [A-F2] |
| "Premium/蓝 V 曝光加权 2–4 倍" | **错误（对 2026 版而言）** | 来源是 2023-03-31 旧代码 `BlueVerifiedAuthorInNetworkMultiplierParam=4.0` / `OutOfNetwork=2.0` [A-S18]。2026 版 home-mixer、vm-ranker、xai-value-model 里都没有按 Premium 或认证加权的代码，Phoenix 的候选特征里也没有认证字段 [A-F5]。Premium 唯一的代码影响是 user-cred 种子带来的执法豁免 [A-F16]。Buffer 统计到 Premium 号人均曝光约 10 倍 [A-S19]，但这是 2024-08 到 2025-08 的相关性数据，无法区分因果，也早于 2026 新算法。回复区可能仍有 Premium 优先，但未找到 2026 年官方帮助中心的可靠原文（help.x.com 返回 403） |
| "TweepCred：认证号上限 100、未认证 55" | **错误（旧版说法）** | 来自 2023 版 TweepCred 的解读。2026 版是 user-cred-v2（PageRank 0–100），用于执法豁免，不是排序乘数 [A-S8] |
| "外链会被降权" | **代码层面无证据；官方否认；实际效果仍偏弱** | 2026 版没有针对 URL 的惩罚，`open_link` 权重是 +0.2 [A-S2]。Bier 2026-04-13 说 "Fake news… Just post the link in the body of the post"[A-S15]；Musk 2026-07-29 说 "We haven't for over a year"[A-S14]。Bier 承认带链接的帖子触达偏低，原因是用户点出去后忘了回来点赞和回复。冲突：Buffer 的数据显示 2025-03 以后非 Premium 号的链接帖中位互动率为 0%[A-S19]，时间早于官方说的"取消惩罚" |
| "hashtag 有助于推荐" | **无证据；官方劝不要用** | 召回和排序靠语义 ID 和 embedding，代码里没有 hashtag 加权 [A-S9]。Grox 的违规分类里有 `SpamHashTagAbuse`（滥用标签算垃圾）[A-S7 grox/flows/ptos/state.py]。Musk 2024-12-17："Please stop using hashtags. The system doesn't need them anymore and they look ugly"[A-S21] |
| "存在固定的最佳发帖时间" | **部分证实（机制存在，固定时间无证据）** | Phoenix 输入里有当地小时和帖龄 [A-S9]，模型会学习受众的时段习惯，但代码里没有写死的时段加权 |
| "日更上限 / 发多了限流" | **部分证实（机制不同）** | 没有每日条数上限。有作者多样性衰减，同一用户的单次刷新里，你的第 2 条 ×0.625，最低 ×0.25 [A-F9]；另有 DPP 相似度重排（`DppTheta=0.65`）[A-S3]。连发相似内容会互相挤占 |
| "前 30 分钟决定生死" | **部分证实（窗口是 2 小时 / 200 曝光，不是 30 分钟）** | 冷启动扶持只对发布 ≤ 2 小时、首页曝光 < 200、作者粉丝 ≤ 5 万的原创帖生效，用早期点赞率做 Thompson 采样 [A-F12]。帖子 48 小时后就离开推荐池 [A-F13]。"30 分钟"在代码里没有依据 |
| "编辑帖子会降权" | **无证据** | 2026 版排序和过滤代码里没有与编辑相关的惩罚（检索 edit 相关字段无结果）。未找到官方说法 |
| "一次举报抵 468 个赞 / 被恶意举报就会被压" | **错误（官方明确驳斥）** | 权重乘的是预测概率；推荐是个性化的；只计算 Home 时间线里推送到的帖子上的行为 [A-F8] |
| "多刷别人帖子下的评论就能涨粉" | **基本错误** | 非关注账号的回复和转发不进 For You [A-F10]；大 V 帖下的回复会被 Grok 打分，粘贴、刷量都是负面信号 [A-F14]。Bier 也曾称每天回复几百条对增长没帮助（媒体转述，原帖未能核实） |
| "视频观看直接加分" | **部分错误（当前）** | `vqv` 权重 2026-08-25 起为 0.0，`video_open` 为 0.07。视频主要靠停留和点击后停留时长等注意力项拿分 [A-F7] |
| "Grok 逐条读帖决定推荐" | **部分证实** | Grox 用 Grok 大模型做内容分类、打标签、给回复打分，"banger" 初筛里有 `slop_score`，但 For You 排序主体是 Phoenix transformer 对行为概率的预测 [A-F3][A-F14][A-F15] |

---

## 💡 意外发现与洞见

1. **"复制链接分享"权重 20，是所有正向行为里最高的**（与互关原创帖的回复并列），是点赞的 40 倍，私信分享也有 5。让人想存下来、转发到站外或微信群的内容（工具清单、干货长图、可引用的数据），在代码层面最值钱。这和"外链降权"的焦虑正好相反：X 想要的是别人把你的帖子链接分享出去，而不是你在帖子里放外链。
2. **算法在主动惩罚 AI 水文**：`llm_slop_user` 标签导致 30 天内拿不到站外推荐，回复排序会看"是否粘贴"。对用 AI 批量写中文推文的创作者来说，这是 2026 年最实际的风险。
3. **转发几乎不值钱（1.0），点赞只有 0.5**：传统的"互赞互转"运营在 2026 版基本无效，有效的是回复、引用、分享和关注。
4. **冷启动扶持面向小号（粉丝 ≤ 5 万）**：小号每条原创帖都有一次被试推的机会，依据是首页早期的"点赞/曝光"比率。所以前 200 次曝光里的点赞率比绝对点赞数更重要。
5. **权重会随时间变**：9-29 点击权重从 0.4 降到 0.3，8-25 视频质量观看从 0.05 降到 0、停留从 0 升到 0.05。文章应写"截至 2026-10-06 的仓库默认值"，并提醒读者到 GitHub 看 diff。官方自己在 `BIDIRECTIONAL_BOOST_CHANGE.md` 里也是这么建议的。
6. **作者多样性和站外折扣的数值（0.5 / 0.25 / 0.75）与 2023 版完全相同**，所以有些"老结论"恰好仍然成立。但回复、蓝 V 等关键数字已经变了，老文章要逐项核对，不能整体照搬。
7. **合规过滤也写进了代码**：例如巴西 2026 大选过滤器（8-14 起），被巴西选举法院列入名单的账号对非关注者不可见。说明 For You 的可见性还受各国法律影响，9-18 起 Under the Hood 报告会显示因法律原因被限制的情况。

## 小结（结论、证据强度、缺口）

**结论**
- 2026 版 X 推荐算法在 `xai-org/x-algorithm`（2026-01-20 首发，05-15、08-13 大更新，此后高频同步）。结构是 Thunder（站内）+ Phoenix 双塔 / SimClusters（站外）召回，Phoenix transformer 预测约 20 种行为概率，再加权求和，经作者多样性（0.5 衰减、0.25 下限）、站外 ×0.75、新作者冷启动和 DPP 重排，最后过可见性过滤。
- 权重（截至 10-06）：点赞 0.5、转发 1、回复 5（互关原创帖 20）、引用 5、复制链接分享 20、关注 4；负反馈 −31 到 −234。
- 2026 版代码里没有 Premium 曝光乘数，也没有外链惩罚、hashtag 加权、编辑降权、日更上限。确实存在的是 48 小时寿命、2 小时 / 200 曝光的冷启动窗口、AI 水文 30 天站外屏蔽，以及大 V 帖下由 Grok 给回复打分。

**证据强度**
- 强（A 级代码直接可证）：架构、权重、多样性和站外参数、冷启动条件、48 小时过滤、互关加成及日期、LLM slop 标签规则。
- 中（官方口头说法 + 媒体）：外链"未降权"（Bier / Musk）、互关改动的产品描述、hashtag 态度。
- 弱（C 级媒体，单源）：回复"踩"的上线日期和排序影响。

**缺口**
1. **Premium 在回复区排序中是否仍有优先**：未拿到 2026 年 help.x.com 原文（403），Grox 回复打分的 prompt 未公开，无法确认。
2. **回复"踩"**：没有 X 官方帖原文可核实，代码中看不到它在排序里的权重。
3. **实验流量与生产值的偏差**：10% 以下的实验不公开；冷启动有分组逻辑，覆盖范围未知；部分阈值（执法粉丝豁免线）明确是 mock 值。
4. **模型本身**：生产 checkpoint 和训练数据未公开，任何具体帖子的分数都无法复现。
5. 未找到"编辑帖子影响推荐"的任何官方或代码证据，正反两面都没有。
