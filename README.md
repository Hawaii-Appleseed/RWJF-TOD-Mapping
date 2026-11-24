# RWJF TOD Mapping

Working maps for an overall assessment of the Waipahu TOD neighborhood around the Hōʻaeʻae (West Loch) and Pouhala (Waipahu Transit Center) rail stations on Oʻahu.

**Map:** https://hawaii-appleseed.github.io/RWJF-TOD-Mapping/

This repository started as a copy of [Waipahu-TOD-NOAH](https://github.com/Hawaii-Appleseed/Waipahu-TOD-NOAH). That map shows potential naturally occurring affordable housing (NOAH), older condo buildings, the TOD Special Districts, and ¼- and ½-mile station rings. Layers from the Waipahu TOD report will be added here.

## Current contents

- `index.html`: the map page. It uses [Leaflet](https://leafletjs.com/) 1.9.4 and draws its own base layers, without map tiles.
- `waipahu_tod.json`: the map data. It holds no owner names.
- `data/permits/`: City building permits within ½ mile of the two stations, January 2014 to June 30, 2025. Four CSVs cover new buildings since the October 2017 rezoning, homes added, homes demolished and all permits. [The folder's README](data/permits/README.md) gives the source, method and counts. The map's permit layers read these same files.
- `scripts/`: the Python scripts that rebuild the NOAH data from City & County of Honolulu, State of Hawaiʻi, HART and HUD sources. The [Waipahu-TOD-NOAH README](https://github.com/Hawaii-Appleseed/Waipahu-TOD-NOAH#rebuilding-the-data) gives the run order and the NOAH definition.

Owner names and mailing addresses from the tax roll stay out of this repository.
