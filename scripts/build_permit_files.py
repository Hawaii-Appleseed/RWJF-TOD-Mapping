"""Write the Waipahu building-permit data files published in data/permits/.

Usage: python build_permit_files.py <tod_output_dir> <out_dir>
  tod_output_dir holds the TOD report's outputs:
    honolulu_tod_permits_2014_2025.csv     every permit near a Skyline station, placed at parcel centroids
    station_new_buildings_2017_2025.xlsx   the report's three permit lists for Hōʻaeʻae and Pouhala

Writes four CSVs (UTF-8 with BOM so Excel keeps the Hawaiian diacritics):
  waipahu_permits_2014_2025.csv     every permit within 1/2 mile of either Waipahu station
  new_buildings_2017_2025.csv       new-building permits since the October 2017 rezoning
  homes_added_2014_2025.csv         permits that recorded housing units added
  homes_demolished_2014_2025.csv    permits that recorded housing units removed
Contractor, applicant and plan-maker names in the City's file are left out.
"""
import sys

import pandas as pd

RECORD = "https://data.honolulu.gov/resource/4vab-c87q.json?buildingpermitno={}"
STATION_NAMES = {"Hōʻaeʻae": "Hōʻaeʻae (West Loch)", "Pouhala": "Pouhala (Waipahu Transit Center)"}
WORK_FLAGS = [("newbuilding", "New building"), ("addition", "Addition"), ("alteration", "Alteration"),
              ("repair", "Repair"), ("demolition", "Demolition"), ("solar", "Solar"),
              ("electricalwork", "Electrical"), ("plumbingwork", "Plumbing"), ("fence", "Fence"),
              ("retainingwall", "Retaining wall"), ("pool", "Pool")]


def is_yes(v):
    return str(v).strip().upper() in {"Y", "YES", "TRUE", "1", "1.0"}


def main(src, out):
    permits = pd.read_csv(f"{src}/honolulu_tod_permits_2014_2025.csv", low_memory=False)
    permits["permit"] = permits.buildingpermitno.astype(str).str.replace(r"\.0$", "", regex=True)
    where = permits.set_index("permit")[["loc_lat", "loc_lon"]]

    near = permits[permits.nearest_station.isin(STATION_NAMES) & permits.within_half_mile.map(is_yes)].copy()
    near["work"] = near.apply(lambda r: "; ".join(label for col, label in WORK_FLAGS if is_yes(r[col])) or "Other", axis=1)
    all_permits = pd.DataFrame({
        "Permit number": near.permit,
        "Issue date": pd.to_datetime(near.issuedate).dt.date.astype(str),
        "Address": near.address,
        "TMK": near.tmk,
        "Use (as recorded)": near.proposeduse,
        "Type of work": near.work,
        "Housing units added (as recorded)": near.numunitsadd.fillna(0).astype(int),
        "Housing units removed (as recorded)": near.numunitsdel.fillna(0).astype(int),
        "Estimated value of work ($)": near.estimatedvalueofwork.fillna(0).round().astype(int),
        "Permit status": near.statusdescription,
        "Nearest station": near.nearest_station.map(STATION_NAMES),
        "Distance to station (miles)": near.dist_to_station_mi.round(2),
        "Within a quarter mile": near.within_quarter_mile.map(lambda v: "Yes" if is_yes(v) else "No"),
        "Latitude": near.loc_lat.round(6),
        "Longitude": near.loc_lon.round(6),
        "City record": near.permit.map(RECORD.format),
    }).sort_values(["Issue date", "Permit number"])
    all_permits.to_csv(f"{out}/waipahu_permits_2014_2025.csv", index=False, encoding="utf-8-sig")
    counts = {"waipahu_permits_2014_2025.csv": len(all_permits)}

    lists = pd.read_excel(f"{src}/station_new_buildings_2017_2025.xlsx", sheet_name=None)
    for sheet, name in [("New buildings", "new_buildings_2017_2025.csv"), ("Homes", "homes_added_2014_2025.csv"),
                        ("Homes demolished", "homes_demolished_2014_2025.csv")]:
        df = lists[sheet].copy()
        df["Permit number"] = df["Permit number"].astype(str).str.replace(r"\.0$", "", regex=True)
        df["Issue date"] = pd.to_datetime(df["Issue date"]).dt.date.astype(str)
        df["Latitude"] = df["Permit number"].map(where.loc_lat).round(6)
        df["Longitude"] = df["Permit number"].map(where.loc_lon).round(6)
        df["City record"] = df["Permit number"].map(RECORD.format)
        missing = int(df.Latitude.isna().sum())
        if missing:
            raise SystemExit(f"{sheet}: {missing} permits have no location in the permit file")
        df.to_csv(f"{out}/{name}", index=False, encoding="utf-8-sig")
        counts[name] = len(df)

    for name, n in counts.items():
        print(f"{name}: {n} rows")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
