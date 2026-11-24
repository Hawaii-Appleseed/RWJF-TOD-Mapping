# Station-area profile: Hōʻaeʻae and Pouhala

Who lives around the Hōʻaeʻae (West Loch) and Pouhala (Waipahu Transit Center) rail stations, how walkable the areas are, and how the land is zoned. They were prepared by Hawaiʻi Appleseed Center for Law and Economic Justice for *Missed Connections* (2026) and are shown on the [RWJF TOD Mapping](https://hawaii-appleseed.github.io/RWJF-TOD-Mapping/) map.

## Files

| File | Rows | What it lists |
|---|---:|---|
| `acs_profile_2020_2024.csv` | 108 | 27 indicators for each station area, both together, and Honolulu County, with 90% margins of error. |
| `acs_tracts.csv` | 14 | The census tracts considered for each station area and whether each was included. |
| `walkability.csv` | 5 | EPA National Walkability Index for each station's half-mile circle and for Honolulu County. |
| `street_reach.csv` | 2 | Share of the streets inside each station's half-mile circle that can be reached in a half-mile walk. |
| `zoning_acres_by_district.csv` | 13 | Acres in each zoning district, for four areas: within a half mile of either station, the Waipahu TOD Plan area, the TOD Special District, and the half-mile area outside the special district. |
| `zoning_summary.csv` | 3 | Single-family-zoned acres, all zoned acres and the single-family share for the same four areas. |

## Census profile

- **Source:** U.S. Census Bureau, American Community Survey 5-year estimates, 2020–2024. Tables used: B01003, B25044, B25070, C17002, B08301, B08013, B08303, B08302, C24010, C16001, B01001 and C18108.
- **Station areas** are built from whole census tracts. A tract is included when it holds at least 5% of the station's half-mile circle and has at least 10% of its own area inside it. Included tracts are summed.
- **Shares** are of each table's universe: households, workers 16 and over, commuters (workers who do not work from home), employed civilians 16 and over, people 5 and over, people whose poverty status is determined, or the civilian noninstitutionalized population (for disability).
- **Margins of error** are at 90% and use the Census Bureau's approximation formulas for sums and proportions.
- **`Unit`** says whether a value is a `count`, a `share` (0–1) or `minutes`.
- **Ilocano** is not reported separately; it falls under "other Asian and Pacific Island languages."

## Walkability and street reach

- **Walkability:** U.S. EPA National Walkability Index, 2019 block groups, scored from 1 (least walkable) to 20 (most). Values are averaged over each half-mile circle, weighted by area and by population.
- **Street reach:** walking routes follow City street centerlines (Statewide GIS, August 2024), leaving out freeways, ramps and military roads.

## Zoning

- **Source:** City and County of Honolulu zoning (Statewide GIS).
- **Single-family** means the R-3.5 through R-20 residential districts.
- **The TOD Special District** is the one adopted by Ordinance 17-54. The Waipahu TOD Plan area is the City's 2014 neighborhood TOD plan boundary.

## Rebuilding

See `scripts/build_assessment_files.py`, which also writes `data/services/`.
