# FACTS — 热榜60秒 · 2026-10-22

Every claim in the film comes from one snapshot of the lists, pulled with a local DailyHotApi
(`dulijun003/dailyhotapi`, branch `ccr-65c7e4c3-onx1px`) on 2026-10-22 16:47 UTC = **2026-10-23 00:47 北京时间**.
Raw responses: `data/<route>.json`. The film reports what the lists show; it does not add facts of its own.

Lists used (7 of 15 tried; weibo 403, zhihu 401, douyin / thepaper / netease / kuaishou / baidu failed upstream):

| Route | List | Entries | "hot" field means |
|---|---|---|---|
| toutiao | 今日头条 热榜 | 50 | HotValue → 热度 |
| tieba | 百度贴吧 热议榜 | 30 | discuss_num → 讨论 |
| bilibili | 哔哩哔哩 热榜·全站 | 100 | stat.view → 播放 |
| 36kr | 36氪 人气榜 | 50 | – |
| ithome | IT之家 热榜 | 48 | – |
| sina-news | 新浪新闻 总排行 | 50 | – |
| qq-news | 腾讯新闻 热点榜 | 50 | hotScore |

Sum: 50 + 30 + 100 + 50 + 48 + 50 + 50 = **378 条**.

## Claims

| # | Claim in the film | Source entry (quoted) |
|---|---|---|
| 1 | 7 个热榜，一共 378 条 | counts above |
| 2 | 上榜最多的是一部手机：4 个平台 10 条说 iPhone Duo | titles containing "iPhone Duo" (see note) |
| 3 | B站第一：折 1 万次，会坏吗？播放 478 万 | bilibili #1 "折1万次，会坏吗？iPhone Duo深度评测", hot 4783248 (stat.view) |
| 4 | 国乒女团 2 比 3 不敌日本，摘银；头条第 8、腾讯第 10 | toutiao #8 "亚锦赛国乒女团决赛不敌日本"; qq-news #10 "乒乓亚锦赛：国乒女团2-3输日本摘银！…" |
| 5 | 星巴克全国施行消费入座；头条第 6、贴吧第 10 | toutiao #6 "人民日报评星巴克“消费入座”"; tieba #10 desc "今日起，星巴克将在全国开始施行消费入座" |
| 6 | 两个榜的第一是同一件事：西藏那曲巴青县 7.0 级地震 | toutiao #1 "西藏那曲巴青县发生7.0级地震"; tieba #1 "愿平安!西藏那曲发生7级地震" |
| 7 | 中国地震台网正式测定，22时33分，北纬32.40度 东经93.79度，震源深度10千米 | tieba #1 desc "中国地震台网正式测定：10月22日22时33分在西藏那曲市巴青县（北纬32.40度，东经93.79度）发生7.0级地震，震源深度10千米。" |
| 8 | 头条热度 1395 万；贴吧讨论 229 万（2,285,310，四舍五入） | toutiao #1 hot 13953302; tieba #1 hot 2285310 |

Note on #2: the matching entries are toutiao #21, bilibili #1 and #55, 36kr #1, #11, #22 and #35, ithome #4, #5 and #34:
1 + 2 + 4 + 3 = **10 条 on 4 platforms** (36kr #1 is a morning digest whose title names iPhone Duo; it counts once).
The film says **10 条**.

Not claimed: casualties, damage, rescue — the lists' entries don't state them. Rankings and numbers are as of the snapshot time and change by the minute.
