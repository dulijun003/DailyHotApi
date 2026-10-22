"""DailyHotApi snapshot (data/<route>.json) → assets/lists.json for the page: per list its name and every entry (rank, title, hot)."""
import json, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROUTES = ['toutiao', 'tieba', 'bilibili', '36kr', 'ithome', 'sina-news', 'qq-news']
NAME = {'toutiao': '今日头条', 'tieba': '百度贴吧', 'bilibili': '哔哩哔哩', '36kr': '36氪', 'ithome': 'IT之家', 'sina-news': '新浪新闻', 'qq-news': '腾讯新闻'}
out = []
for r in ROUTES:
    d = json.load(open(os.path.join(D, 'data', r + '.json')))
    out.append({'id': r, 'name': NAME[r], 'type': d['type'], 'time': d['updateTime'],
                'items': [[i + 1, x['title'].replace('\n', ' ').strip(), x.get('hot') or 0] for i, x in enumerate(d['data'])]})
json.dump(out, open(os.path.join(D, 'assets', 'lists.json'), 'w'), ensure_ascii=False)
print('lists', len(out), 'entries', sum(len(l['items']) for l in out))
