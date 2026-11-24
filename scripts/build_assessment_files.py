"""Write the services and station-area data files published in data/services/ and data/station_area/.

Usage: python build_assessment_files.py <tod_output_dir> <data_dir>
  tod_output_dir holds the TOD report's outputs:
    station_services.xlsx              services near Hōʻaeʻae and Pouhala with walking distances
    station_services_google_maps.csv   the services list as checked against Google Maps and news reports
    station_area_acs.xlsx              ACS 2020-2024 profile of each station area
    station_area_zoning.xlsx           zoned acres within a half mile of the stations

Writes CSVs (UTF-8 with BOM so Excel keeps the Hawaiian diacritics) to data_dir/services and
data_dir/station_area.
"""
import os
import sys

import pandas as pd


def save(df, path):
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"{os.path.relpath(path)}: {len(df)} rows")


def main(src, data):
    services_dir, area_dir = f"{data}/services", f"{data}/station_area"
    os.makedirs(services_dir, exist_ok=True)
    os.makedirs(area_dir, exist_ok=True)

    s = pd.read_excel(f"{src}/station_services.xlsx", sheet_name=None)
    facilities = s["Facilities"].rename(columns={
        "category": "Category", "name": "Name", "address": "Address", "lon": "Longitude", "lat": "Latitude",
        "status": "Status", "source": "Source", "store_type": "Store type", "npi_enumerated": "NPI enumerated",
        "practices": "Practices", "license_type": "License type", "grades": "Grades", "school_type": "School type",
        "acres": "Acres"})
    save(facilities, f"{services_dir}/station_services.csv")
    save(s["Summary"].rename(columns={"category": "Category"}), f"{services_dir}/services_within_half_mile_walk.csv")
    save(s["SNAP changes"].rename(columns=str.capitalize), f"{services_dir}/snap_retailer_changes.csv")
    save(pd.read_csv(f"{src}/station_services_google_maps.csv"), f"{services_dir}/services_verification.csv")

    walk = s["Walkability"].rename(columns={"area": "Area", "walkability_index": "EPA walkability index (1-20)",
                                            "epa_category": "EPA category"})
    save(walk, f"{area_dir}/walkability.csv")
    reach = s["Street reach"].rename(columns={"station": "Station"})
    save(reach, f"{area_dir}/street_reach.csv")

    a = pd.read_excel(f"{src}/station_area_acs.xlsx", sheet_name=None)
    save(a["Long"].rename(columns={"area": "Area", "indicator": "Indicator", "value": "Value",
                                   "moe_90": "Margin of error (90%)", "unit": "Unit"}),
         f"{area_dir}/acs_profile_2020_2024.csv")
    save(a["Tracts"].rename(columns={"station_area": "Station area", "geoid": "GEOID", "tract": "Tract",
                                     "circle_share": "Share of the half-mile circle",
                                     "tract_share": "Share of the tract inside the circle",
                                     "included": "Included"}),
         f"{area_dir}/acs_tracts.csv")

    z = pd.read_excel(f"{src}/station_area_zoning.xlsx", sheet_name=None)
    save(z["Acres by district"], f"{area_dir}/zoning_acres_by_district.csv")
    save(z["Summary"].rename(columns={"Unnamed: 0": "Measure"}), f"{area_dir}/zoning_summary.csv")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
