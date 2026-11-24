# Building permits near the Waipahu rail stations

Building permits within a ½-mile straight line of the Hōʻaeʻae (West Loch) and Pouhala (Waipahu Transit Center) rail stations, January 1, 2014 to June 30, 2025. They were prepared by Hawaiʻi Appleseed Center for Law and Economic Justice for *Missed Connections* (2026) and are shown on the [RWJF TOD Mapping](https://hawaii-appleseed.github.io/RWJF-TOD-Mapping/) map.

**Source:** City and County of Honolulu, Department of Planning and Permitting, Building Permits, https://data.honolulu.gov/d/4vab-c87q (file through June 30, 2025). Every row links to the City's own record in the `City record` column.

## Files

| File | Rows | What it lists |
|---|---:|---|
| `new_buildings_2017_2025.csv` | 28 | Every permit marked as a new building, issued from October 26, 2017 through June 30, 2025. October 26, 2017 is when Ordinances 17-54 and 17-56 rezoned the Waipahu station areas. Additions, alterations and repairs are not included. |
| `homes_added_2014_2025.csv` | 41 | Every permit that recorded housing units added, including additions and conversions such as accessory dwelling units. Four permits record units that are not homes; they are marked `No` in `Likely a home`, with the reason in `Note`. |
| `homes_demolished_2014_2025.csv` | 35 | Every permit that recorded housing units removed. Nine are not counted as homes demolished; they are marked `No` in `Counted as a home demolished`, with the reason in `Note`. Those nine are two revoked permits, three repeat demolition permits for one address, a driveway permit, and demolitions of a commercial building, an office and a church. |
| `waipahu_permits_2014_2025.csv` | 1,843 | Every permit of any kind within ½ mile of either station: new buildings, additions, alterations, solar, electrical, plumbing, demolitions and more. |

**Totals from these files:**
- **New buildings since the 2017 rezoning:** 28 permitted, 18 near Pouhala and 10 near Hōʻaeʻae. 5 are on Farrington Highway.
- **Homes added:** 40, from the 37 permits counted as homes; 27 were permitted after the rezoning.
- **Homes demolished:** 32, from 26 permits.

## Method

- Permits record a tax map key (TMK), not coordinates. Each permit is placed at the center of its tax parcel, or at the City address point for permits filed under a temporary TMK. `Latitude` and `Longitude` give that point.
- Distances are straight lines to the station point in HART's station layer.
- `On land rezoned in 2017` means the parcel lies in an area rezoned by Ordinance 17-56.
- Uses and housing units are copied as recorded on the permit. Two permits can share an address when a lot gets more than one building.
- In `waipahu_permits_2014_2025.csv`, `Type of work` combines the City's yes/no work flags: new building, addition, alteration, repair, demolition, solar, electrical, plumbing, fence, retaining wall and pool.
- The City's file also includes contractor, applicant and plan-maker names. They are left out here.

**Key to common uses as recorded:**
- SFD: single-family dwelling.
- ADU: accessory dwelling unit, a second, smaller home on a lot with a house.
- 2FD or two-family detached: two homes on one lot in separate buildings.
- PHOTOVOLTAIC: rooftop solar.

The City's standardized structure code was used to check which permits are homes: 51 is a single-family dwelling and 52 a two-family detached dwelling.

## Rebuilding

`scripts/build_permit_files.py` writes these four files from the report's permit outputs (`honolulu_tod_permits_2014_2025.csv` and `station_new_buildings_2017_2025.xlsx`):

```bash
python scripts/build_permit_files.py <report output folder> data/permits
```

The files are UTF-8 with a byte-order mark, so Excel shows the Hawaiian diacritics correctly.
