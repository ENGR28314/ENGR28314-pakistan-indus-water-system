# Pakistan Rivers, Dams, Barrages & Link Canals Explorer

A Streamlit application for exploring Pakistan's major rivers and water-control infrastructure across:

- Gilgit-Baltistan
- Khyber Pakhtunkhwa (KPK)
- Punjab
- Sindh
- Balochistan
- Azad Jammu & Kashmir (AJK)
- Islamabad Capital Territory (ICT)

## Features

- Interactive OpenStreetMap-based map
- Province/region filter
- Asset-type filters
- Search across the dataset
- Major rivers and tributaries
- Dams and reservoirs/projects
- Barrages/headworks
- Major inter-river link canals
- Upstream/downstream descriptions
- Important river confluences
- Conceptual river-connectivity diagram
- CSV download
- CSV/XLSX upload for user datasets
- Separate data, map and network modules

## Install and run

Python 3.11+ is recommended.

```bash
python -m venv .venv
```

Windows:
```bash
.venv\\Scripts\\activate
```

Linux/macOS:
```bash
source .venv/bin/activate
```

Then:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## GitHub / Streamlit Community Cloud

Upload the project folder to GitHub and select `app.py` as the Streamlit entry point. No API key is required.

## Data and limitations

This package is a structured major-feature reference dataset, not a complete national GIS database. Coordinates are representative visualization coordinates. For engineering design, flood operations, irrigation operation, legal/regulatory reporting, or hydraulic modelling, replace them with verified official GIS and time-series datasets.

Project status can change, so verify current status against the responsible agency.

## Reference sources

- WAPDA: https://wapda.gov.pk/
- WAPDA Projects: https://wapda.gov.pk/wapda-projects/
- IRSA: https://pakirsa.gov.pk/
- Ministry of Water Resources: https://www.mowr.gov.pk/
- Ministry major rivers map: https://www.mowr.gov.pk/Detail/NTcwZGFlMTctOGNhYy00M2YyLTliMDAtMzU0OGU5YTlmZWZk
- Government Indus Water Treaty link-canal/barrage map: https://ncc.gov.pk/SiteImage/Misc/files/Indus%20Water%20Treaty%20Map%20English%282%29.pdf
- PCRWR Water Body Inventory: https://www.pcrwr.gov.pk/water-body-inventory/
