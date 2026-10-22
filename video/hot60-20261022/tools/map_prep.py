"""Physical locator for the quake shot: Natural Earth 10m lakes and rivers (public domain), no borders.
Equirectangular with cos(32.4°) x-scaling, clipped to lon 84–104, lat 26–38, in a 1000-unit-wide box.
python3 tools/map_prep.py raw/ne_10m_lakes.geojson raw/ne_10m_rivers_lake_centerlines.geojson assets/map.json"""
import json, math, sys
L0, L1, B0, B1 = 84.0, 104.0, 26.0, 38.0
K = math.cos(math.radians(32.4))
W = 1000 / ((L1 - L0) * K)
def P(lon, lat): return [round((lon - L0) * K * W, 1), round((B1 - lat) * W, 1)]
def inside(pts): return any(L0 - 2 < x < L1 + 2 and B0 - 2 < y < B1 + 2 for x, y in pts)
def lines(g):
    t, c = g['type'], g['coordinates']
    if t == 'Polygon': return [c[0]]
    if t == 'MultiPolygon': return [p[0] for p in c]
    if t == 'LineString': return [c]
    if t == 'MultiLineString': return c
    return []
out = {'w': 1000, 'h': round((B1 - B0) * W, 1), 'lakes': [], 'rivers': []}
for key, src in (('lakes', sys.argv[1]), ('rivers', sys.argv[2])):
    for f in json.load(open(src))['features']:
        for ln in lines(f['geometry']):
            if inside(ln):
                out[key].append({'name': f['properties'].get('name_zh') or f['properties'].get('name'), 'pts': [P(*p[:2]) for p in ln]})
out['P'] = {'lon0': L0, 'lat1': B1, 'k': K * W, 'kl': W}
json.dump(out, open(sys.argv[3], 'w'), ensure_ascii=False)
print(sys.argv[3], len(out['lakes']), 'lakes', len(out['rivers']), 'rivers', 'h', out['h'])
