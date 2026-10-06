# 点赞只值 0.5：2026 年 X 新规则下的账号运营全指南

> X 在 2026 年把推荐算法交给了 Grok 系模型，代码全部开源，变现也改成只奖励原创。这篇文章对照开源代码、官方条款和大样本数据，把新规则逐条讲清楚：哪些老攻略已经失效，新号怎么起，钱从哪里来，AI 能用到什么程度。

<!-- 图1：封面图 -->

中文圈流传最广的一条推特涨粉秘籍是：**作者回复你的评论，权重等于 75，相当于 150 个赞。** 所以要去大 V 帖子下面抢评论，争取被回复。

这个数字不是编的。它出自 Twitter 2023 年开源的排序模型配置，原文写的是 `reply_engaged_by_author: 75.0`[^tw2023]。问题在于，那份代码三年前就过时了。

2026 年 1 月 20 日，X 在 GitHub 上开源了新的推荐系统 `xai-org/x-algorithm`，8 月又公开了全部权重[^xalgo]。在新代码里，**"作者回复你"这一项根本不存在**。回复的权重是 5，转发是 1，点赞是 0.5。所有正向行为里，权重最高的是一个很少有人留意的动作："复制链接"，权重 20，是点赞的 40 倍[^param]。

这一年 X 改的远不止权重：

- **推荐交给模型**：推荐系统改由 Grok 系模型预测你的行为，人工规则几乎删光。
- **互关加权**：互相关注的人之间被加权。
- **回复区可以"踩"**：Premium 用户可以给回复点"踩"。
- **只奖励原创**：9 月起，变现只奖励原创内容。

你收藏的那些攻略，有多少还能用？

这篇文章想把 2026 年的新规则一次讲清楚。每一条结论都标注了出处，可能是开源代码的具体文件，可能是 X 官方的公告或条款，也可能是数据研究。确认过的写成确认，推断的会说明是推断。文章很长，建议先看下面的一页速查，再按需要跳到对应章节。

> **说明**：文中引用的代码数值，都是截至 2026 年 10 月 6 日 `xai-org/x-algorithm` 仓库里的"生产默认值"。X 会持续调整这些参数，仅 9 月就改过一次点击权重。所以不要把任何一个小数点当成永久规则，本文也不例外。

---

## 先看结论：一页速查

| # | 新规则 | 一句话解释 | 详见 |
|---|---|---|---|
| 1 | **让人想回复、分享、关注，比让人点赞重要得多** | 点赞的权重只有 0.5，回复和引用是 5，复制链接是 20，关注作者是 4 | §1 |
| 2 | **原创帖才能吃到新号扶持** | 粉丝不超过 5 万的作者，原创帖在发布 2 小时内、曝光不到 200 次时，有机会被直接提到推荐流第 15 位 | §3 |
| 3 | **别短时间连发** | 同一个人刷一次，你的第 2 条帖子只拿 0.625 倍分数，第 3 条 0.44 倍；代码里没有日更上限，连发的问题是自己跟自己抢位置 | §1、§2 |
| 4 | **外链没有被降权，但链接帖天然吃亏** | 官方否认降权，代码里也找不到惩罚；但读者点出去后很少回来互动，分数自然低 | §2 |
| 5 | **Premium 不是曝光开关** | 推荐排序代码里没有 Premium 乘数。它的作用在回复区优先、账号信誉和变现资格上 | §3 |
| 6 | **回复要少而精** | 大号帖子下的回复由 Grok 打分，"24 小时回了多少条""是不是粘贴的"都会被看到 | §3 |
| 7 | **互关圈有用，互粉群没用** | 互关作者原创帖的"回复"权重加 15，但群里发链接协调来的互动不计入排序 | §3 |
| 8 | **中文帖会被翻译后推给外国人** | 2026 年 5 月底起，中文帖由 Grok 自动翻译，并跨语言推荐 | §4 |
| 9 | **变现只认原创，回复不计入门槛** | 新的原创内容奖励计划只按原创内容计酬，回复区的曝光不算 | §5 |
| 10 | **AI 可以帮你写，不能替你互动** | X 一边推 Grok 写作，一边清理 AI 自动回复号；被判为 AI 水文的账号，30 天内拿不到站外推荐 | §6 |

**阅读路线**：

- **新号**：先读 §3，再读 §2。
- **想变现**：直接读 §5。
- **已经在做、数据却在下滑**：先读 §1 和 §6，看看是不是踩了新规则的雷。

---

## §1 规则变了什么：读懂 2026 年开源的推荐算法

### 1.1 先分清两份代码

讨论"推特算法"之前，先确认说的是哪一份代码。

**第一份是 2023 年 3 月 Twitter 开源的 `twitter/the-algorithm`。** 网上流传的大部分"权重秘籍"都出自这里：回复 13.5、作者回复 75、蓝 V 在站内 4 倍、站外 2 倍[^tw2023][^tw2023blue]。

**第二份是 2026 年 1 月 20 日 X 开源的 `xai-org/x-algorithm`。** 它是一套重写过的新系统[^xalgo1][^tc-open]。

即使是新代码，信息也是分批公开的：

- **1 月首版**：没有具体权重。代码引用了权重常量，但参数文件不在仓库里[^xalgo1]。
- **2026 年 8 月 13 日**：官方补上了参数文件，权重数值这才第一次公开[^xalgo]。

所以，1 月到 8 月之间那些号称"根据 2026 开源代码算出权重"的文章，数字不可能来自新代码，多半是把 2023 年的旧数字重新包装了一遍。

### 1.2 一条帖子是怎么被推到你面前的

"X 的算法交给 Grok 了"这句话常被理解成"Grok 会一条条读你的帖子，决定推不推"。这个理解只对了一部分。

按照开源仓库的说明，X 的 For You 推荐流水线大致分五步[^xalgo][^phoenix]：

1. **召回**：从两个池子里找候选。
   - 你关注的人最近发的帖子，由名为 Thunder 的组件提供。
   - 你没关注的人的帖子，由 Phoenix 双塔模型和 SimClusters 兴趣聚类找出来。
2. **预测**：排序模型 Phoenix 读取你最近的互动历史，预测你对每条候选帖子会做出约 20 种行为中每一种的概率：点赞、回复、转发、引用、分享、点开、停留、关注作者、点"不感兴趣"、屏蔽、举报……
3. **打分**：把这些概率乘以各自的权重，再加总，公式是 `最终分 = Σ 权重 × 预测概率`。
4. **调整**：同一作者多条帖子递减、陌生人的帖子打折、扶持新作者、去掉相似内容。
5. **过滤与混排**：去掉违规或不该给你看的内容，再和广告、推荐关注等内容混排。

<!-- 图2：X For You 推荐流水线示意图 -->

**"Grok 驱动"的准确含义有两层。**

- 第一层，Phoenix 用的是 Grok 系的 transformer 架构。2025 年 10 月 Musk 说要"删除所有启发式规则"[^smt-grok]，2026 年的 README 也说已经去掉了几乎所有人工设计的特征[^xalgo1]。
- 第二层，Grok 大模型（代码里叫 Grox）另外负责内容理解、打标签和回复区打分。后面会讲到它在回复区和 AI 水文识别上的作用。

**模型看的是你的读者，而不是你本人。**

Phoenix 对每条候选帖子的输入只有几样：帖子和作者的标识、帖子内容的语义编码，以及时区、当地时间、帖子发布了多久等上下文。代码里没有"作者是否认证"这个特征[^phoenix]。

所以，你的帖子能不能被推出去，取决于模型预测"看到它的这个人"会不会回复、分享、关注你，而不取决于你开没开会员、加没加标签。

### 1.3 权重表：哪些行为值钱

下表是截至 2026 年 10 月 6 日的生产默认权重，来自仓库里的 `home-mixer/params/param.rs`[^param]：

| 正向行为 | 权重 | 负向行为 | 权重 |
|---|---|---|---|
| 复制链接（分享到站外） | **20** | 举报 | **−234** |
| 回复互关作者的原创帖 | **20**（5 + 15） | 静音作者 | −58.8 |
| 回复 | 5 | 点"不感兴趣" | −47.52 |
| 引用转发 | 5 | 屏蔽作者 | −31.2 |
| 私信分享 | 5 | 划过不停留 | −0.02 |
| 关注作者 | 4 | | |
| 分享 | 2 | | |
| 转发 | 1 | | |
| 点赞 | **0.5** | | |
| 点开后的停留时长 | 0.4 | | |
| 点击帖子 | 0.3（9 月 29 日由 0.4 下调） | | |
| 打开链接 | 0.2 | | |
| 视频质量观看 | 0（8 月 25 日由 0.05 下调） | | |

<!-- 图3：2026 年 X 推荐权重条形图（正负向对比） -->

这张表有三种读法。

**第一，"让人想说话、想转出去、想关注你"的内容最值钱。**

点赞只有 0.5，转发只有 1。"求赞求转"式运营在新规则下收益很低。真正有分量的有三类：

- **回复和引用**：5
- **关注作者**：4
- **把链接复制出去、私信发给别人**：分别为 20 和 5

这意味着 X 想要的是**值得被转发到群聊和朋友圈的内容**，比如工具清单、数据图表、能直接拿去用的方法。它看重的不是你在帖子里放了多少外链，而是别人愿不愿意把你的帖子分享出去。

**第二，负反馈的代价远大于正反馈的收益。**

"不感兴趣"是 −47.52，静音是 −58.8，举报是 −234。标题党、引战、蹭不相干的热点，可能多拿到几个赞，但只要让一部分人点了"不感兴趣"或静音，就会被大幅扣分。

**第三，别拿权重做加减法。**

权重乘的是"这个人做出这个行为的预测概率"，而不是行为的次数。仓库 README 专门写了一段话：举报的权重是点赞的 468 倍，并不代表"1 次举报能抵掉 468 个赞"。举报本身极少发生，预测概率非常低，所以给了很大的权重[^xalgo]。

同一段注释还写了一句对中文圈很重要的话：

> "Directly navigating to a post (i.e., coordinating via groupchat) has no ranking impact."

意思是，只有发生在首页推荐里推给他的帖子上的互动，才计入推荐系统。**在群里发链接，让大家点进去点赞评论，对排序没有作用**[^param]。

### 1.4 打完分之后，还有几道关

**同一作者的帖子递减。**

同一位读者刷新一次时，系统会把你的几条帖子按分数排好，然后逐条打折，公式是 `0.75 × 0.5^k + 0.25`（k 从 0 开始）[^vmranker]：

- 第 1 条：拿全分
- 第 2 条：0.625 倍
- 第 3 条：0.44 倍
- 第 4 条：0.34 倍
- 最低：0.25 倍

<!-- 图4：同作者多帖衰减曲线 -->

这就是网上"单作者曝光上限"说法的真实来源。但它不是"一天发超过 N 条就限流"，代码里找不到任何每日条数上限。它的实际效果是：**短时间连发，你的几条帖子会在同一个读者面前互相抢位置。** 这组参数（0.5 和 0.25）和 2023 年版完全相同[^tw2023div]，所以"别连发"这条老经验恰好依然成立。

**陌生人看到你，分数打 0.75 折。**

帖子推给不关注你的人时，分数乘以 0.75。另外有一个过滤器，会把"你没关注的人发的回复和转发"从 For You 里去掉[^vmranker][^xalgo]。

这有一个直接的推论：**你在别人帖子下写的回复，不会作为独立内容推给陌生人。想被陌生人刷到，只能靠原创帖。** §3 会接着讲这一点。

**帖子只能活 48 小时。**

发布超过 48 小时的帖子，会被直接排除出推荐候选[^xalgo]。

**被判为"AI 水文"，30 天内拿不到站外推荐。**

这是这次研究里最值得警惕的一个发现。开源的执法规则里有一个 `llm_slop_user`（AI 水文用户）标签。账号一旦被打上这个标签，就会挂上一个为期 30 天的垃圾标签。在这 30 天里，这个账号的帖子在"推荐给不关注你的人"这一场景下会被直接丢弃，只有粉丝还能看到[^enforce][^xalgo]。

换句话说，**被判为 AI 批量产出的账号，增长会直接停止。** §6 会展开讲。

### 1.5 开源代码能告诉你什么，不能告诉你什么

开源不等于完全透明。1 月版发布后，康奈尔、格拉茨、卡内基梅隆三所大学的研究者都批评它"给人一种透明的假象"，因为没有权重、没有训练好的模型、也没有训练数据[^redacted]。8 月更新补上了权重和训练代码，但生产环境的模型参数和真实训练数据仍然不公开[^phoenix]。官方还说明，只有占流量 10% 以上的实验才会出现在仓库里[^xalgo]。

所以，开源代码能告诉你**机制**：

- 系统在预测什么
- 哪些行为加分、哪些扣分
- 有哪些硬性的门槛和窗口

开源代码不能告诉你**结果**：你某一条帖子具体会得多少分，外人无法复现。任何"精确到小数点的爆款公式"都不成立。

正确的用法是两条：

- **按机制调整行为。**
- **每个月去 GitHub 看一次仓库的提交记录。** X 改权重会直接体现在代码里，比读任何二手解读都快。

---

## §2 发什么、怎么发：内容与发帖策略

在新规则下，判断一条内容好不好，标准只有一个：**能不能让对的人停下来、回复、转出去、关注你。**

形式、时间、频率，都是为这件事服务的。先把过时的说法清理掉。

### 2.1 13 条流行说法，逐条核查

| 流行说法 | 结论 | 依据 |
|---|---|---|
| "作者回复你的评论 = 75 倍权重 / 150 个赞" | **已过时** | 来自 2023 年配置[^tw2023]；2026 年代码里没有这一项，回复权重为 5[^param] |
| "回复 13.5、转发 20" 之类的公式 | **已过时** | 混用了旧数字；2026 年转发权重为 1[^param] |
| "开蓝 V / Premium，曝光 ×2 到 ×4" | **在排序代码里找不到** | 来自 2023-03 的旧参数[^tw2023blue]；2026 年的排序代码没有 Premium 乘数（见 §3.4） |
| "外链会被降权，链接要放评论区" | **官方否认，代码里也没有惩罚；但链接帖实际表现确实弱** | 见 2.2 |
| "多加话题标签能获得推荐" | **无效** | 代码里没有标签加权；Musk 公开说"别再用了"[^hashtag] |
| "发布后前 30 分钟决定生死" | **不准确** | 代码里的新号扶持窗口是 2 小时或 200 次曝光（见 §3.1） |
| "一天发超过 N 条就会被限流" | **没有上限，但有同次递减** | 见 1.4[^vmranker] |
| "编辑帖子会被降权" | **没有证据** | 排序和过滤代码里都没有找到与编辑有关的惩罚 |
| "被举报 1 次等于少 468 个赞" | **错误，官方专门驳斥** | 权重乘的是概率，不是次数[^xalgo] |
| "进互赞群，在群里发链接互相点" | **对排序无效** | "Directly navigating to a post … has no ranking impact"[^param] |
| "发视频天然有加权" | **目前不成立** | 视频质量观看的权重 8 月下调为 0；视频靠停留和点开拿分[^param] |
| "存在一个固定的黄金发帖时间" | **没有写死的规则** | 模型会把"当地时间"当作特征，学的是你的受众的习惯[^phoenix] |
| "Grok 逐条读帖决定推不推" | **部分正确** | Grok 负责打标签和回复区打分，For You 的主排序靠 Phoenix 预测行为概率 |

### 2.2 链接到底能不能放

这是争议最大的一个问题，两边的证据都很硬。

**说没有降权的一方：**

- 开源代码里没有针对链接的惩罚，"打开链接"的权重反而是 +0.2[^param]。
- X 时任产品负责人 Nikita Bier 在 2025 年 10 月发帖说"Links are not deboosted"[^bier-links]。
- 2026 年 7 月 29 日，Musk 在回复 Paul Graham 时说："We haven't for over a year."[^musk-links]

**说链接帖表现差的一方：**

Buffer 分析了 7.1 万个账号的 1,880 万条帖子（2024 年 8 月至 2025 年 8 月），发现从 2025 年 3 月起：

| 账号与帖子类型 | 中位互动率 |
|---|---|
| 非 Premium 账号的链接帖 | **0%** |
| Premium 账号的链接帖 | 约 0.28% |
| Premium 账号的纯文本帖 | 约 0.90% |

[^buffer-links]

这两种说法可以同时成立。Bier 自己给过解释：读者点开链接、去看网页后，常常忘了回来点赞和回复，系统拿不到互动信号[^bier-links]。X 后来在 iOS 内置浏览器底部加了一排常驻的点赞和回复按钮，就是为了解决这个问题[^gigazine-links]。

所以准确的说法是：**没有硬性降权，但模型按"预测你会互动"打分，而链接帖天然拿不到互动。**

另外要注意，2026 年下半年还没有独立的对照数据。

**实操上：**

- **主帖必须能独立成立。** 读者不点链接，也能拿到核心信息：结论、数据、清单。
- **链接放正文还是评论区，影响不大。** 2026 年 7 月 Bier 明确说过"不需要再把链接放评论区了"[^musk-links]。
- **要导流的长内容，优先写成 X 的 Articles（长文）。** 内容留在站内，就不会让读者跳出去。

### 2.3 形式、时间、频率

**形式：纯文本仍然最强。**

Buffer 2026 年度报告统计了 5,200 万条以上的帖子（2024 年 1 月至 2025 年 12 月）。X 平台各形式的中位互动率如下[^buffer-2026]：

| 形式 | 中位互动率 |
|---|---|
| 纯文本 | 3.56% |
| 图片 | 3.40% |
| 视频 | 2.96% |
| 链接 | 2.25% |

文本和图片相差不大，链接垫底。视频方面，前面说过"视频质量观看"的权重已经下调为 0。代码里看不到视频天然加权的证据，视频要靠吸引人停留和点开拿分。

**时间：周中好、周六差，具体几点以自己的数据为准。**

几家大样本研究在"哪几天"上意见一致：周二到周四最好，周六最差。在"几点"上有分歧：

| 研究 | 样本 | 最佳时段 |
|---|---|---|
| Buffer | 870 万条帖子 | 工作日上午 9 到 11 点[^buffer-time] |
| Hootsuite | 100 万+ 条帖子 | 工作日上午 9 到 11 点[^hootsuite] |
| Sprout Social | 约 20 亿次互动 | 周二到周四中午 12 点到下午 6 点[^sprout] |

这些时间都按**受众所在地的当地时间**计算。

开源代码里没有写死的黄金时段，"当地时间"只是模型的一个输入特征[^phoenix]。所以最可靠的做法是看自己后台的粉丝活跃时间。

给中文创作者的换算：

- **面向大中华区读者**：以工作日上午和午休为主。
- **面向美国读者**：美东时间上午 9 到 11 点，大约是北京时间晚上 9 点到午夜（夏令时）。也就是说，你在晚上就能赶上英文读者的上午。

**频率：每天 1 到 3 条主帖，拉开间隔，长期坚持。**

需要说明一点：目前**没有**找到 2025 到 2026 年针对 X 的"发帖频率与单帖曝光"大样本研究。上面这个建议是根据机制推断出来的。

推断的依据有两条：

1. **同作者递减**：同一位读者一次刷新里，你的第 2 条只拿 0.625 倍分数[^vmranker]。所以把主帖间隔几个小时发，比集中连发划算。
2. **坚持带来的差距**：Buffer 跟踪了 10 万多名用户 26 周，坚持发帖的人单帖互动是零散发帖者的 5 倍以上。不过这项研究不分平台[^buffer-consistency]。

回复不进入陌生人的推荐流，所以不受同作者递减影响。但回复数量本身会被风控看到，这一点 §3 会讲。

### 2.4 写给中文创作者的四条约束

**第一，首屏只显示约 140 个汉字。**

X 的长帖在信息流里只显示前 280 个"加权字符"，中日韩文字每个字算 2 个字符[^charcount]。所以中文长帖的首屏大约只能放 **140 个汉字**，超出部分要读者点"显示更多"才能看到。英文写作指南不会提这件事，但它决定了中文帖的钩子要写多短。

**第二，主时间线不显示加粗，也别靠话题标签。**

2024 年 10 月起，加粗只在帖子详情页显示，主时间线上看不到[^bold]。Musk 在 2024 年 12 月发帖："Please stop using hashtags."[^hashtag]

信息流里的排版要靠**分行和空行**来完成。

**第三，你的中文帖可能被翻译给外国人看。**

2026 年 3 月底起，X 用 Grok 自动翻译外语帖子，并把它们推荐给其他语言的用户。中文大约在 5 月底开通[^bier-translate][^ithome-translate]。

所以写作时要少用只有中文语境才懂的谐音、缩写和梗，翻译过去以后外国读者看不懂，还可能引起误解。§4 会专门讨论这件事带来的机会。

**第四，争取的是"不后悔的停留"。**

Musk 在 2025 年 1 月说，推荐的目标是"unregretted user-seconds"，也就是用户不后悔花掉的时间[^unregretted]。代码里既有"停留"和"点开后停留时长"这样的正向项，也有"划过不停留"这样的负向项，再加上很重的负反馈权重。

靠情绪煽动换来的停留，往往伴随着"不感兴趣"和静音，最后得不偿失。

### 2.5 三个写法模板

下面三个模板是根据上面的机制和数据**归纳出来的结构**，没有人做过 A/B 测试，用的时候请结合自己的数据调整。

**模板一：140 字钩子长帖**

适合 Premium 用户，用来拿单帖曝光和停留时长。

```
第 1 段（≤140 字）：具体结论或反常识判断，带数字或具体对象
第 2 段：读者能从这条帖子里得到什么
——（以下需要点"显示更多"）——
3–6 个短段：每段一个论点 + 一个例子或证据，段与段之间空一行，不用加粗
结尾：一个能具体回答的问题（不要问"你怎么看？"）
```

为什么这样写：

- 首屏只有约 140 字，结论必须放在最前面。
- 点开"显示更多"后的停留时长有正向权重。
- 结尾提一个具体问题，是为了换回复（权重 5）。

**模板二：独家数据长文 + 摘要主帖**

用来拿原创分和变现。

```
Articles 长文：标题 = 具体发现；开头三句给结论；
  正文按"数据从哪来 → 发现 1/2/3 → 方法与局限"组织；图表自己做
主帖：3–5 条要点摘要，不点开也有价值，附长文卡片
发布后 1 小时内：认真回复前几条有内容的评论
```

依据有两条：

- **官方在扶持长文**：2026 年 1 月，Articles 开放给所有 Premium 用户[^articles]。X 随后拿出 100 万美元奖励"最佳文章"，冠军 @beaverd 写的是基于自建数据库的德勤政府合同调查，据报道曝光约 4,400 万次[^1m-article][^1m-winner]。他不是百万粉大号，赢在**独家数据和原创调查**。
- **新的变现规则只奖励原创**（见 §5）。

**模板三：Thread 步骤拆解**

用来拿深度互动和收藏。

```
1/ 钩子：一个具体问题或结果 + "下面拆成 N 步"
2/ 到 N-1/：每条讲一步或一个案例，每条单独拿出来也能看懂（方便被单独转发）
N/ 总结 + 一份可执行清单 + 一个问题
```

要注意，Thread 发出后不能编辑，发之前务必校对。

---

<!-- 第一批到此结束。§3–结尾在第二批。 -->

[^tw2023]: Twitter. *the-algorithm-ml: Heavy Ranker README*（2023 年 4 月权重）. GitHub. https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md
[^tw2023blue]: Twitter. *HomeGlobalParams.scala @ ef4c5eb*（2023-03-31，蓝 V 乘数 4.0/2.0）. GitHub. https://github.com/twitter/the-algorithm/blob/ef4c5eb/home-mixer/server/src/main/scala/com/twitter/home_mixer/param/HomeGlobalParams.scala
[^tw2023div]: Twitter. *ScoredTweetsParam.scala*（2023，作者多样性 0.5/0.25、站外 0.75）. GitHub. https://github.com/twitter/the-algorithm/blob/main/home-mixer/server/src/main/scala/com/twitter/home_mixer/product/scored_tweets/param/ScoredTweetsParam.scala
[^xalgo]: xAI / X. *X For You Feed Algorithm – README*. GitHub，2026-10-06 版本. https://github.com/xai-org/x-algorithm
[^xalgo1]: xAI / X. *x-algorithm 首个提交 aaa167b*. GitHub，2026-01-20. https://github.com/xai-org/x-algorithm/commit/aaa167b
[^param]: xAI / X. *home-mixer/params/param.rs*（排序权重与官方注释）. GitHub，2026-10-06 版本. https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs
[^vmranker]: xAI / X. *vm-ranker/params.rs 与 xai-value-model/scoring.rs*（作者多样性、站外折扣）. GitHub，2026-10-06 版本. https://github.com/xai-org/x-algorithm/blob/main/xai-value-model/scoring.rs
[^phoenix]: xAI / X. *phoenix/README.md*. GitHub，2026-10-06 版本. https://github.com/xai-org/x-algorithm/blob/main/phoenix/README.md
[^enforce]: xAI / X. *abuse-enforcement-service 与 visibility-filtering 规则*. GitHub，2026-08-26 同步. https://github.com/xai-org/x-algorithm/tree/main/abuse-enforcement-service
[^tc-open]: TechCrunch. *X open sources its algorithm while facing a transparency fine and Grok controversies*. 2026-01-20. https://techcrunch.com/2026/01/20/x-open-sources-its-algorithm-while-facing-a-transparency-fine-and-grok-controversies
[^redacted]: Dataconomy. *Researchers label recent X algorithm release as a redacted version*. 2026-02-05. https://dataconomy.com/2026/02/05/researchers-label-recent-x-algorithm-release-as-a-redacted-version/
[^smt-grok]: Social Media Today. *X switching to fully AI-powered Grok algorithm*. 2025-10-19. https://socialmediatoday.com/news/x-formerly-twitter-switching-to-fully-ai-powered-grok-algorithm/803174
[^hashtag]: FOX 5 DC. *Are hashtags dead? Elon Musk says 'please stop' using them*. 2024-12-17. https://www.fox5dc.com/news/hashtags-x-elon-musk-says-please-stop-using-them
[^bier-links]: Nikita Bier. "Links are not deboosted". X，2025-10-19. https://x.com/nikitabier/status/1980042761819828393
[^musk-links]: PPC Land. *X drops year-old link penalty, Musk tells Zuckerberg on platform*. 2026-07-30. https://ppc.land/x-drops-year-old-link-penalty-musk-tells-zuckerberg-on-platform/
[^buffer-links]: Buffer. *Do Posts with Links Affect Content Performance on X?* 2025-10-14. https://buffer.com/resources/links-on-x/
[^gigazine-links]: GIGAZINE. *X is testing a feature that makes it easier to get likes on posts with links*. 2025-11-05. https://gigazine.net/gsc_news/en/20251105-x-post-url-link
[^buffer-2026]: Buffer. *The State of Social Media Engagement in 2026*. 2026. https://buffer.com/resources/state-of-social-media-engagement-2026/
[^buffer-time]: Buffer. *The Best Time to Post on Twitter/X in 2026: 8.7 Million Posts Analyzed*. 2026-03-13. https://buffer.com/resources/best-time-to-tweet-research
[^hootsuite]: Hootsuite. *Best time to post on social media*. 2025-11-19. https://blog.hootsuite.com/best-time-to-tweet/
[^sprout]: Sprout Social. *Best times to post on X in 2026*. 2026-03-31. https://sproutsocial.com/insights/best-times-to-post-on-twitter/
[^buffer-consistency]: Buffer. *Consistent posting study*. 2025-01-29. https://buffer.com/resources/consistent-posting-study
[^charcount]: X Developer Platform. *Counting characters*. https://docs.x.com/fundamentals/counting-characters
[^bold]: Deccan Chronicle. *Elon Musk gets bold font removed from X's main timeline*. 2024-10-01. https://deccanchronicle.com/technology/elon-musk-gets-bold-font-removed-from-xs-main-timeline-1827302
[^bier-translate]: Nikita Bier. "We're rolling out auto-translate worldwide…". X，2026-04-07. https://x.com/nikitabier/status/2041335306331549699
[^ithome-translate]: IT之家.《X 平台面向全球推出 Grok 自动翻译》. 2026-05-29. https://www.ithome.com/0/956/853.htm
[^unregretted]: Business Today. *Elon Musk teases algorithm tweaks and customisable feeds*. 2025-01-04. https://www.businesstoday.in/technology/news/story/elon-musk-teases-algorithm-tweaks-and-customisable-feeds-see-all-details-459582-2025-01-04
[^articles]: PPC Land. *X opens Articles to all Premium users*. 2026-01-07. https://ppc.land/x-opens-articles-to-all-premium-users-ending-exclusive-pricing-tier/
[^1m-article]: X / @XCreators（Elon Musk 转发）. "We're giving $1 million to the Top Article of the next payout period". X，2026-01-16. https://x.com/elonmusk/status/2012350620045287714
[^1m-winner]: Social Media Today. *X Awards $1M To Top Article for January*. 2026-02-04. https://www.socialmediatoday.com/news/x-awards-1-million-to-top-article-for-january/811396/
