# Everyday services near the Waipahu rail stations

Food stores, health care, schools, child care, parks and libraries near the Hōʻaeʻae (West Loch) and Pouhala (Waipahu Transit Center) rail stations, with walking distances from each station. They were prepared by Hawaiʻi Appleseed Center for Law and Economic Justice for *Missed Connections* (2026) and are shown on the [RWJF TOD Mapping](https://hawaii-appleseed.github.io/RWJF-TOD-Mapping/) map.

## Files

| File | Rows | What it lists |
|---|---:|---|
| `station_services.csv` | 125 | Every facility, with category, address, coordinates, status, source, and straight-line and walking miles to each station. |
| `services_within_half_mile_walk.csv` | 12 | For each category and station: how many are within a ½-mile walk (and how many of those are unconfirmed), how many are within a ½-mile straight line, and the nearest one with its walking distance. |
| `snap_retailer_changes.csv` | 13 | Stores near the stations that stopped or started accepting SNAP after June 30, 2023. |
| `services_verification.csv` | 79 | The facilities as checked against Google Maps and news reports, with links and notes on closures. |

## Sources

| Category | Source |
|---|---|
| Supermarkets, grocery and convenience stores | USDA SNAP-authorized retailer locations (October 2026). A supermarket is USDA store type Supermarket or Super Store. CVS, Longs and Walgreens are counted as pharmacies. |
| Pharmacies | CMS NPI Registry community and retail pharmacies in ZIP 96797. Long-term care, specialty, infusion and HMO pharmacies are left out. The registry keeps closed pharmacies, so closures were set by hand. |
| Clinics and doctor's offices | The federally qualified health center licensed by the Hawaiʻi Department of Health (Office of Health Care Assurance), plus street addresses where DOH lists a lab certificate for a doctor's office or clinic. One row per address; `Practices` counts the practices at that address. |
| Hospital emergency department and dialysis | DOH Office of Health Care Assurance and The Queen's Medical Center. |
| Child care and preschools | State of Hawaiʻi list of licensed centers and preschools (Statewide GIS, December 2021). Family child care homes are not included. |
| Public, charter and private schools | Statewide GIS (DOE, November 2024; HAIS, 2021). |
| Parks | City and County of Honolulu parks (Statewide GIS, October 2021). |
| Libraries | Hawaiʻi State Public Library System (Statewide GIS). |

## Method

- **Walking distance** follows City street centerlines (Statewide GIS, August 2024). It leaves out freeways, ramps and military roads, and street segments connect only at the same level. Off-street paths are not included.
- **Distances start** at the station point in HART's station layer, snapped to the nearest street.
- **Park distances** run to the nearest point on the park's edge within 60 m of a street.
- **`Status`** is `open`, `unconfirmed`, or the month a facility closed.
- **SNAP changes:** a store *stopped* if its last SNAP authorization ended after June 30, 2023, and *started* if its first authorization came after that date. The historical file runs through 2025.

## Rebuilding

`scripts/build_assessment_files.py` writes these files and those in `data/station_area/` from the report's outputs:

```bash
python scripts/build_assessment_files.py <report output folder> data
```
