"""Write data/zoning/: the City zoning map for the Waipahu map area, and zoned acres near the stations.

Usage: python build_zoning.py <waipahu_tod.json> <out_dir>
  waipahu_tod.json   the map data (for the map extent, the TOD Special District and the stations)

Outputs
  zoning_districts.geojson  one feature per zoning district (all its areas merged), clipped to the map
                            area, with the use group, acres and label points ([lon, lat, acres] for
                            each area of 3 acres or more)
  zoning_acres.csv          acres of each zoning district within 1/2 mile of each station, inside the
                            TOD Special District and in the whole map area

Source: State of Hawaiʻi Statewide GIS Program, ParcelsZoning MapServer layer 3, a copy of the City and
County of Honolulu zoning map loaded September 2023. Acres are measured on a local flat projection
centered on Waipahu, which is accurate to well under 1% at this size.
"""
import csv
import json
import math
import os
import sys

from shapely.geometry import box, mapping, Point, shape
from shapely.ops import transform, unary_union

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_station_parcels import ZONING, query_box, to_geojson  # noqa: E402

HALF_MILE_M = 804.672
SQM_PER_ACRE = 4046.8564224
LABEL_MIN_ACRES = 3

# Use groups for the map colors. Each zoning district goes to the first group whose prefix it matches.
GROUPS = [
    ("residential", "Residential", ("R-",)),
    ("mixed", "Mixed use", ("AMX", "BMX")),
    ("apartment", "Apartment", ("A-",)),
    ("business", "Business", ("B-",)),
    ("industrial", "Industrial", ("I-", "IMX")),
    # F-1 is the Federal and Military Preservation District
    ("open", "Agriculture and preservation", ("AG", "P-", "C", "F-")),
]


def group_of(zone):
    for key, _, prefixes in GROUPS:
        if zone.startswith(prefixes):
            return key
    return "other"


def projector(lat0, lon0):
    """Local equirectangular projection in meters, and its inverse."""
    phi = math.radians(lat0)
    my = 111132.92 - 559.82 * math.cos(2 * phi) + 1.175 * math.cos(4 * phi)
    mx = 111412.84 * math.cos(phi) - 93.5 * math.cos(3 * phi)
    fwd = lambda x, y, z=None: ((x - lon0) * mx, (y - lat0) * my)  # noqa: E731
    inv = lambda x, y, z=None: (x / mx + lon0, y / my + lat0)  # noqa: E731
    return fwd, inv


def main(map_json, out_dir):
    m = json.load(open(map_json, encoding="utf-8"))
    x0, y0, x1, y1 = m["extent"]
    fwd, inv = projector((y0 + y1) / 2, (x0 + x1) / 2)
    to_m = lambda g: transform(fwd, g)  # noqa: E731
    to_ll = lambda g: transform(inv, g)  # noqa: E731

    clip = to_m(box(x0, y0, x1, y1))
    stations = [s for s in m["stations"] if s.get("tod")]
    rings = {s["name"]: to_m(Point(s["lon"], s["lat"])).buffer(HALF_MILE_M, 128) for s in stations}
    either = unary_union(list(rings.values()))
    district = unary_union([to_m(shape(f["geometry"]).buffer(0)) for f in m["districts"]["features"]])

    parts, names = {}, {}
    for f in query_box(x0, y0, x1, y1, layer=ZONING, fields="zone_class,zoning_des", offset="0.000005"):
        geom_rings = f.get("geometry", {}).get("rings")
        a = f["attributes"]
        zone = (a.get("zone_class") or "").strip()
        if not geom_rings or not zone:
            continue
        g = to_m(shape(to_geojson(geom_rings)).buffer(0)).intersection(clip)
        if not g.is_empty:
            parts.setdefault(zone, []).append(g)
            names[zone] = (a.get("zoning_des") or zone).strip()

    acres = lambda g: g.area / SQM_PER_ACRE  # noqa: E731
    features, rows = [], []
    for zone, gs in parts.items():
        g = unary_union(gs)
        polys = list(getattr(g, "geoms", [g]))
        labels = []
        for p in sorted(polys, key=lambda p: -p.area):
            if acres(p) >= LABEL_MIN_ACRES:  # [lon, lat, acres]: the map shows smaller areas' labels only when zoomed in
                pt = to_ll(p.representative_point())
                labels.append([round(pt.x, 6), round(pt.y, 6), round(acres(p), 1)])
        by_station = {name: acres(g.intersection(r)) for name, r in rings.items()}
        props = {
            "zone": zone, "name": names[zone], "group": group_of(zone),
            "acres_map": round(acres(g), 1),
            "acres_half_mile": round(acres(g.intersection(either)), 1),
            "acres_tod_special_district": round(acres(g.intersection(district)), 1),
            "labels": labels,
        }
        features.append({"type": "Feature", "properties": props,
                         "geometry": json.loads(json.dumps(mapping(to_ll(g))))})
        rows.append([zone, names[zone], dict((k, n) for k, n, _ in GROUPS).get(props["group"], "Other"),
                     *(round(by_station[s["name"]], 1) for s in stations),
                     props["acres_half_mile"], props["acres_tod_special_district"], props["acres_map"]])

    def rounded(coords):
        if isinstance(coords[0], (int, float)):
            return [round(coords[0], 6), round(coords[1], 6)]
        return [rounded(c) for c in coords]

    for f in features:
        f["geometry"]["coordinates"] = rounded(f["geometry"]["coordinates"])
    order = {k: i for i, (k, _, _) in enumerate(GROUPS)}
    features.sort(key=lambda f: (order.get(f["properties"]["group"], 99), f["properties"]["zone"]))
    rows.sort(key=lambda r: -r[-3])

    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "zoning_districts.geojson"), "w", encoding="utf-8") as fh:
        json.dump({"type": "FeatureCollection", "features": features}, fh, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(out_dir, "zoning_acres.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Zoning district", "District name", "Use group",
                    *(f"Acres within 1/2 mile of {s['name']}" for s in stations),
                    "Acres within 1/2 mile of either station", "Acres in the TOD Special District",
                    "Acres in the map area"])
        w.writerows(rows)
        total = [sum(r[i] for r in rows) for i in range(3, 3 + len(stations) + 3)]
        w.writerow(["All districts", "", "", *(round(t, 1) for t in total)])

    half = sum(r[-3] for r in rows)
    print(f"{len(features)} zoning districts; {half:,.0f} zoned acres within 1/2 mile "
          f"(two full circles are {2 * math.pi * HALF_MILE_M ** 2 / SQM_PER_ACRE:,.0f} acres)")
    for r in rows:
        print(f"  {r[0]:7s} {r[2]:30s} half-mile {r[-3]:7.1f}  SD {r[-2]:6.1f}  map {r[-1]:7.1f}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
