"""Write data/parcels/station_area_parcels.geojson: every land parcel in the Waipahu station areas.

Usage: python build_station_parcels.py <waipahu_tod.json> <out.geojson>
  waipahu_tod.json   the map data (for the extent, plan boundary, TOD Special District and stations)

A parcel is kept when its center is within 1/2 mile of the Hōʻaeʻae or Pouhala station, or inside the
TOD Special District or the Waipahu TOD Plan area. Road parcels are left out. Each parcel carries its
TMK, lot size in square feet (the recorded area, or the GIS area when none is recorded) and the zoning
district at its center, from the State's copy of the City zoning map (September 2023).
"""
import json
import math
import sys
import time
import urllib.parse
import urllib.request

PARCELS = "https://geodata.hawaii.gov/arcgis/rest/services/ParcelsZoning/MapServer/11/query"
ZONING = "https://geodata.hawaii.gov/arcgis/rest/services/ParcelsZoning/MapServer/3/query"
HALF_MILE = 0.5


def query_box(x0, y0, x1, y1, layer=PARCELS, fields="tmk8num,gisacres,rec_area_sf,street_parcel",
              offset="0.000003", depth=0):
    """Features intersecting a box, splitting the box when the server's record limit is hit."""
    params = {"where": "1=1", "geometry": f"{x0},{y0},{x1},{y1}", "geometryType": "esriGeometryEnvelope",
              "inSR": "4326", "spatialRel": "esriSpatialRelIntersects", "outSR": "4326",
              "outFields": fields, "returnGeometry": "true",
              "maxAllowableOffset": offset, "geometryPrecision": "6", "f": "json"}
    url = layer + "?" + urllib.parse.urlencode(params)
    for i in range(5):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                d = json.load(r)
            if "error" in d:
                raise RuntimeError(d["error"])
            break
        except Exception:
            if i == 4:
                raise
            time.sleep(2 * (i + 1))
    if d.get("exceededTransferLimit") and depth < 6:
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        out = []
        for box in [(x0, y0, mx, my), (mx, y0, x1, my), (x0, my, mx, y1), (mx, my, x1, y1)]:
            out += query_box(*box, layer=layer, fields=fields, offset=offset, depth=depth + 1)
        return out
    return d.get("features", [])


def area(ring):
    return sum(a * d - c * b for (a, b), (c, d) in zip(ring, ring[1:])) / 2


def centroid(rings):
    outer = max(rings, key=lambda r: abs(area(r)))
    a = area(outer)
    if a == 0:
        xs, ys = zip(*outer)
        return sum(xs) / len(xs), sum(ys) / len(ys)
    cx = sum((x0 + x1) * (x0 * y1 - x1 * y0) for (x0, y0), (x1, y1) in zip(outer, outer[1:])) / (6 * a)
    cy = sum((y0 + y1) * (x0 * y1 - x1 * y0) for (x0, y0), (x1, y1) in zip(outer, outer[1:])) / (6 * a)
    return cx, cy


def inside(lon, lat, multipolygon):
    hit = False
    for poly in multipolygon["coordinates"]:
        for ring in poly:
            for (x0, y0), (x1, y1) in zip(ring, ring[1:]):
                if (y0 > lat) != (y1 > lat) and lon < x0 + (lat - y0) * (x1 - x0) / (y1 - y0):
                    hit = not hit
    return hit


def miles(lat0, lon0, lat1, lon1):
    p0, p1 = math.radians(lat0), math.radians(lat1)
    h = math.sin((p1 - p0) / 2) ** 2 + math.cos(p0) * math.cos(p1) * math.sin(math.radians(lon1 - lon0) / 2) ** 2
    return 3958.8 * 2 * math.asin(math.sqrt(h))


def to_geojson(rings):
    polys = []
    for ring in rings:
        if area(ring) <= 0 or not polys:
            polys.append([ring])
        else:
            polys[-1].append(ring)
    return {"type": "MultiPolygon", "coordinates": polys}


def main(map_json, out_path):
    m = json.load(open(map_json, encoding="utf-8"))
    areas = [m["plan"]["geometry"]] + [f["geometry"] for f in m["districts"]["features"]]
    stations = [s for s in m["stations"] if s.get("tod")]

    x0, y0, x1, y1 = m["extent"]
    zoning = []
    for f in query_box(x0, y0, x1, y1, layer=ZONING, fields="zone_class,zoning_des", offset="0.000005"):
        rings = f.get("geometry", {}).get("rings")
        if rings:
            xs = [x for r in rings for x, _ in r]
            ys = [y for r in rings for _, y in r]
            zoning.append(((min(xs), min(ys), max(xs), max(ys)), to_geojson(rings), f["attributes"]))

    def zone_at(lon, lat):
        for (bx0, by0, bx1, by1), geom, a in zoning:
            if bx0 <= lon <= bx1 and by0 <= lat <= by1 and inside(lon, lat, geom):
                return a.get("zoning_des") or a.get("zone_class") or ""
        return ""

    geoms, attrs = {}, {}
    for f in query_box(x0, y0, x1, y1):
        a = f["attributes"]
        if a.get("street_parcel") == 1 or not f.get("geometry", {}).get("rings"):
            continue
        t = str(a["tmk8num"])
        geoms.setdefault(t, []).extend(f["geometry"]["rings"])
        attrs[t] = a

    features = []
    for t, rings in geoms.items():
        lon, lat = centroid(rings)
        near = min(miles(lat, lon, s["lat"], s["lon"]) for s in stations)
        if near > HALF_MILE and not any(inside(lon, lat, g) for g in areas):
            continue
        a = attrs[t]
        recorded = float(a.get("rec_area_sf") or 0)
        sqft = recorded if recorded > 0 else float(a.get("gisacres") or 0) * 43560
        features.append({"type": "Feature", "properties": {
            "tmk": t, "lot_sqft": int(round(sqft)), "area_basis": "recorded" if recorded > 0 else "GIS",
            "zoning": zone_at(lon, lat), "miles_to_station": round(near, 2),
            "tod_special_district": any(inside(lon, lat, f["geometry"]) for f in m["districts"]["features"])},
            "geometry": to_geojson(rings)})
    features.sort(key=lambda f: f["properties"]["tmk"])
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump({"type": "FeatureCollection", "features": features}, fh, ensure_ascii=False, separators=(",", ":"))
    sizes = sorted(f["properties"]["lot_sqft"] for f in features)
    print(f"{len(features)} parcels; median lot {sizes[len(sizes) // 2]:,} sq ft; "
          f"{sum(1 for f in features if f['properties']['area_basis'] == 'GIS')} use GIS area")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
