# 配图方案：《点赞只值 0.5：2026 年 X 新规则下的账号运营全指南》

全文共 7 张图：

- 3 张数据图，已生成为 PNG
- 2 张流程图，已在正文中写成 Mermaid 代码
- 2 张插画，给出了生图提示词

## 统一风格前缀（插画用）

- **中文**：编辑插画风格，扁平几何构图，低饱和配色（深蓝 #1c5cab、雾白、珊瑚红 #e34948 点缀），大量留白，细线条，画面中无文字，无品牌标志，无真人肖像
- **English**：Editorial flat illustration, clean geometric composition, muted palette (deep blue #1c5cab, off-white, coral red #e34948 accents), generous negative space, fine line work, no text, no logos, no real people

数据图使用同一组蓝（#2a78d6）和红（#e34948），这组颜色已用色盲可读性脚本验证通过，与插画配色属于同一色系。

---

## 图 1：封面图（插画，待生成）

- **位置**：文章顶部，正文标记 `<!-- 图1 -->`
- **尺寸**：2.35:1（公众号封面）。另出一张 16:9 的通用版。
- **画面**：一台老式天平，左边托盘放着很多小小的"心形点赞"图标，右边托盘只放了一个"链接"图标，天平明显向右边倾斜。背景是淡淡的代码网格线。
- **隐喻**：在新规则下，一次"被分享出去"的分量，比很多个赞都重，对应权重 20 比 0.5。
- **提示词（中）**：{风格前缀}，一台简约的老式天平，左侧托盘堆满许多小巧的心形图标，右侧托盘只有一个链条形状的链接图标，天平明显向右下沉，背景是极淡的代码网格线，居中构图，柔和侧光，2.35:1
- **提示词（英）**：{style prefix}, a minimalist antique balance scale, the left pan piled with many tiny heart icons, the right pan holding a single chain-link icon, the scale clearly tipping toward the right, faint code-grid lines in the background, centered composition, soft side light, aspect ratio 2.35:1

## 图 2：推荐流水线（Mermaid 流程图，已嵌入正文）

- **位置**：§1.2
- **说明**：五个步骤：召回 → 预测 → 打分 → 调整 → 过滤与混排。GitHub 和大多数 Markdown 编辑器会直接渲染成流程图。
- **在公众号使用**：需要先导出成图片。可以在 mermaid.live 粘贴代码导出 PNG，或者交给设计师按下面的描述重画：五个横向排列的圆角方块，用箭头连接，每个方块里写一个步骤名和一行说明。

## 图 3：推荐权重条形图（数据图，已生成）

- **文件**：`images/chart-weights.png`
- **位置**：§1.3
- **图表**：左右两栏横向条形图。左栏是 11 个正向行为，用蓝色；右栏是 4 个负向行为，用红色，显示绝对值。两栏的刻度不同，图上已注明。
- **结论式标题**：复制链接和回复最值钱，点赞只值 0.5；负反馈的代价远大于正反馈
- **数据来源**：xai-org/x-algorithm `home-mixer/params/param.rs`，截至 2026-10-06

## 图 4：同作者多帖衰减（数据图，已生成）

- **文件**：`images/chart-decay.png`
- **位置**：§1.4
- **图表**：柱状图，第 1 到第 6 条帖子各自的分数乘数，依次为 1、0.625、0.438、0.344、0.297、0.273。虚线标出下限 0.25。
- **结论式标题**：连发等于自己抢自己：同一读者一次刷新里，第 2 条只拿 0.625 倍分数
- **数据来源**：`vm-ranker/params.rs` 和 `xai-value-model/scoring.rs`

## 图 5：新号冷启动扶持（Mermaid 流程图，已嵌入正文）

- **位置**：§3.1
- **说明**：一张判断流程图。依次判断 4 个条件，满足后进入候选池，按早期点赞率随机抽样，抽中的帖子会被插到推荐流第 15 到 16 位。
- **在公众号使用**：同图 2，先导出为图片。

## 图 6：X 广告受众规模（数据图，已生成）

- **文件**：`images/chart-audience.png`
- **位置**：§4.1
- **图表**：横向条形图，美国、日本、印尼、印度、英国、香港、台湾，单位为百万。香港旁边注明"约等于当地人口的 168%，数据异常"。
- **结论式标题**：X 是美日双核平台；中文受众的盘子小，而且算不清
- **数据来源**：DataReportal（2025-01）；Digital 2026 港、台报告（数据截至 2025-10）

## 图 7：30 天起号节奏（插画或信息图，待生成）

- **位置**：§7，正文标记 `<!-- 图7 -->`
- **画面**：一条横向的时间轴，分成 4 段，代表 4 周，每段配一个小图标：
  - 第 1 周：放大镜加名单，代表找到对标账号
  - 第 2 周：对话气泡，代表有质量的回复
  - 第 3 周：一篇长文，代表写 Article
  - 第 4 周：折线图，代表复盘
- **建议做法**：用 Canva、Figma 或者稿定设计做成信息图，把 §7 表格中的 4 段文字放上去。文字最好排版时手动添加，生图模型容易把中文写错。
- **纯图标版提示词（中）**：{风格前缀}，一条水平时间轴分为四段，依次是放大镜与名单、对话气泡、一篇长文稿纸、上升的折线图四个简洁图标，图标之间以细箭头相连，16:9
- **纯图标版提示词（英）**：{style prefix}, a horizontal timeline divided into four segments with four simple icons in sequence: a magnifying glass with a list, speech bubbles, a long-form document page, a rising line chart, connected by thin arrows, aspect ratio 16:9

---

## 插图使用提醒

- 两张插画都没有在画面里放文字。需要中文标题的话，请在后期排版时手动加上。
- 用 AI 生成的配图建议在 X 上打上 "Made with AI" 标签，这和正文 §6 的建议一致。
