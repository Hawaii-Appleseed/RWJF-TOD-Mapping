# Zoning in the Waipahu map area

The City and County of Honolulu zoning districts around the Hōʻaeʻae (West Loch) and Pouhala (Waipahu Transit Center) rail stations, and how many acres of each lie near the stations. The [RWJF TOD Mapping](https://hawaii-appleseed.github.io/RWJF-TOD-Mapping/) map shades the area by these districts when "Shade the map by: Zoning" is selected. GitHub also draws `zoning_districts.geojson` as a map when you open it.

## Files

- **`zoning_districts.geojson`**: one feature per zoning district, with all of that district's areas merged and clipped to the map area.
- **`zoning_acres.csv`**: for each district, the acres within ½ mile of each station, within ½ mile of either station, inside the TOD Special District, and in the whole map area. The last row totals them.

## Fields in `zoning_districts.geojson`

| Field | Meaning |
|---|---|
| `zone` | Zoning district code, such as `BMX-3`. |
| `name` | District name, such as `BMX-3 Community Business Mixed Use District`. |
| `group` | The use group that sets the map color (see below). |
| `acres_map` | Acres of the district in the map area. |
| `acres_half_mile` | Acres within ½ mile (straight line) of either station. |
| `acres_tod_special_district` | Acres inside the TOD Special District (Ordinance 17-54). |
| `labels` | Label points for the map, as `[longitude, latitude, acres]`, one for each separate area of 3 acres or more. |

## Use groups

The map gives each use group one color, and labels each area with its district code.

| Group | Districts in the map area |
|---|---|
| Residential | R-3.5, R-5, R-7.5 |
| Mixed use | AMX-2, BMX-3 |
| Apartment | A-1, A-2 |
| Business | B-1, B-2 |
| Industrial | I-1, I-2, IMX-1 |
| Agriculture and preservation | AG-1, AG-2, P-1, P-2, F-1 (Federal and Military Preservation) |

Federal land is in the preservation group so the map can use six colors, which stay distinguishable for people with color-blindness. None of it is within ½ mile of a station.

## Checks

- Within ½ mile of the stations, 956 acres are zoned, 310 of them residential (R-5 and R-7.5). The *Missed Connections* report's zoning summary (`data/station_area/zoning_summary.csv`) counts 954 and 309 acres from the same source.
- The TOD Special District holds 335 zoned acres here; the report counts 335.

## Sources

- **Zoning:** State of Hawaiʻi Office of Planning and Sustainable Development, Statewide GIS Program, the State's copy of the City and County of Honolulu zoning map, loaded September 2023. Layer: `geodata.hawaii.gov/arcgis/rest/services/ParcelsZoning/MapServer/3`. This copy reflects the October 2017 TOD rezoning. For a legal zoning determination, use the City's Department of Planning and Permitting.
- **TOD Special District boundary and station points:** City and County of Honolulu and HART.

Acres are measured on a flat projection centered on Waipahu, which is accurate to well under 1% over an area this size. Areas are clipped to the map area, so districts that extend beyond it, such as R-5 and P-2, are only partly counted in `acres_map`.

## Rebuilding

```bash
python scripts/build_zoning.py waipahu_tod.json data/zoning
```

The script needs [Shapely](https://shapely.readthedocs.io/) 2.
