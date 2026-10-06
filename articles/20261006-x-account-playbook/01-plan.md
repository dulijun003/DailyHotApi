# 研究计划：2026 年 X 账号运营实操指南

## 子问题拆解

| # | 子问题 | 对应核心问题 | 需要的证据类型 | 预期来源 |
|---|---|---|---|---|
| Q1 | 2026 年开源的推荐系统在哪个仓库？架构是什么（召回、Grok 排序、过滤）？ | 1 | 原始代码、官方公告 | GitHub、X Engineering 账号、@XEng 帖子、媒体报道 |
| Q2 | 代码或官方说明里，哪些信号被加权、哪些被降权？包括互动类型的权重、负反馈、外链、作者多样性、停留时长、视频观看 | 1, 2 | 原始代码、官方说明、独立的代码解读 | GitHub 源码、技术博客的逐行解读 |
| Q3 | 流行说法的真伪：外链降权、Premium 加权、日更上限、发帖时间、话题标签、回复踩的影响 | 1, 2 | 原始代码、官方表态、实验数据 | 代码、Musk/X 官方帖子、Buffer 等的数据研究 |
| Q4 | 2026 年规则变化的时间线：回复踩、互关加权、原创奖励、X Money、Articles 开放等 | 1, 4 | 官方公告 | X 帮助中心、官方博客、主流媒体 |
| Q5 | 各内容形式（短推、Thread、Articles、视频）的表现数据，以及停留时长友好的写法 | 2 | 数据研究、案例 | Buffer、Hootsuite、Sprout、创作者复盘 |
| Q6 | 冷启动打法（回复策略、社群、互关圈、热点、合作）的证据和案例 | 3 | 案例、实验、平台机制 | 创作者复盘、增长博客、代码中的社交图信号 |
| Q7 | Original Content Rewards 的规则、门槛、可领取地区、收益量级；订阅、X Money | 4 | 官方条款、创作者晒单 | X 帮助中心、媒体、创作者公开数据 |
| Q8 | 其他变现路径（私域/Newsletter、产品、商单）的量级 | 4 | 案例、行业数据 | 创作者经济报告、案例 |
| Q9 | X 上中文用户的规模与特点，英文区的竞争情况，自动翻译功能 | 5 | 平台数据、第三方统计 | X 官方、Similarweb、DataReportal、媒体 |
| Q10 | AI 内容与自动化政策，反垃圾机制，AI 回复被惩罚的证据 | 6 | 官方规则、报道 | X 自动化规则、开发者条款、媒体 |

## 研究视角（≥5）
1. **机制原理**：开源代码到底写了什么
2. **规则变化（历史演进）**：2025 → 2026 年的时间线
3. **实操方法**：发帖、冷启动的打法
4. **商业变现**：收益与路径
5. **反方与争议**：流行误读、算法的不透明之处、变现的天花板、平台风险
6. **国际与语言比较**：中文和英文

## 搜索查询清单（各研究员在此基础上扩展）
- **算法**：`xai-org x-algorithm github 2026`、`X open source algorithm January 2026 Grok phoenix`、`X algorithm source code analysis link penalty author diversity`、`X 算法 开源 2026 解读`
- **规则变化**：`X reply downvote March 2026`、`X mutuals ranking July 2026`、`X Original Content Rewards help center`、`X Money creator payouts`
- **发帖策略**：`X post frequency study 2026`、`best time to post on X 2026 data`、`X Articles reach 2026`、`X video reach 2026`
- **冷启动**：`grow X account from zero 2026 reply strategy`、`X communities growth 2026`、`推特 冷启动 涨粉 2026`
- **变现**：`Original Content Rewards eligibility countries payout`、`X creator earnings 2026 screenshot`、`推特 创作者 收益 2026`
- **语言**：`X Chinese language users 2026`、`X auto translate posts Grok 2026`、`中文推特 生态 2026`
- **AI 运营**：`X automation rules AI replies 2026`、`X spam AI-generated replies crackdown 2026`
- **反面**：`X algorithm myths debunked`、`X creator payouts decline criticism 2026`

## 执行方式
深度档，采用**并行子代理**：

- 5 个研究员并行工作：A 算法机制、B 发帖策略与写法、C 冷启动与涨粉、D 变现、E 语言选择与 AI 运营。
- 每人把事实卡片写到 `research/<视角>.md`。
- 主代理负责汇总：去重、统一编号 F#/S#，标记各视角之间的矛盾，写出 `02-notes.md` 和 `03-sources.md`。关键结论由主代理亲自抽查原始来源。
