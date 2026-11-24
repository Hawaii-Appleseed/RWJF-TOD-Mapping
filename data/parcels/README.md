# Parcels in the Waipahu station areas

Every land parcel in the station areas around the Hōʻaeʻae (West Loch) and Pouhala (Waipahu Transit Center) rail stations, with lot size and zoning. It is shown on the [RWJF TOD Mapping](https://hawaii-appleseed.github.io/RWJF-TOD-Mapping/) map, shaded by lot size. GitHub also draws `station_area_parcels.geojson` as a map when you open it.

## What's included

- **Parcels.** A parcel is included when its center is within ½ mile (straight line) of either station, or inside the TOD Special District (Ordinance 17-54) or the 2014 Waipahu TOD Plan area. Road parcels are left out.
- **Condominiums** appear once, as the land parcel under the building.

## Fields

| Field | Meaning |
|---|---|
| `tmk` | Eight-digit tax map key: zone, section, plat, parcel. |
| `lot_sqft` | Lot size in square feet. |
| `area_basis` | `recorded` when `lot_sqft` is the area on record. `GIS` when no area is recorded and it is computed from the parcel's shape. |
| `zoning` | The zoning district at the parcel's center. Parcels split between districts show only that one. |
| `miles_to_station` | Straight-line miles from the parcel's center to the nearer station. |
| `tod_special_district` | `true` when the parcel's center is inside the TOD Special District. |

## Sources

- **Parcels:** State of Hawaiʻi Office of Planning and Sustainable Development, Statewide GIS Program, *Parcels – Honolulu County*, from the City and County of Honolulu. Layer: `geodata.hawaii.gov/arcgis/rest/services/ParcelsZoning/MapServer/11`.
- **Zoning:** the State's copy of the City and County of Honolulu zoning map, as of September 2023. Layer: `.../ParcelsZoning/MapServer/3`.
- **TOD Special District and TOD Plan boundaries, and station points:** City and County of Honolulu and HART.

Parcel shapes are simplified to about 0.3 m, which does not visibly change their outlines.

## Rebuilding

```bash
python scripts/build_station_parcels.py waipahu_tod.json data/parcels/station_area_parcels.geojson
```
