# Buffalo EV Charging Infrastructure Analysis

Geospatial analysis of electric vehicle charging infrastructure in Buffalo, NY. Identifies coverage gaps, accessibility patterns, and expansion opportunities using GIS and spatial analysis.

**Status:** Portfolio-Ready | **Skill Level:** Intermediate GIS | **Suitable For:** QGIS Specialist / GIS Analyst roles

---

## 🎯 Project Overview

This project demonstrates real-world GIS problem-solving by analyzing EV charging distribution across Buffalo. Key findings:

- **10 charging locations** across Buffalo metro area
- **70% public access**, 30% restricted (campus/hospital)
- **80% concentrated in downtown/university districts**
- **5 DC fast charging** vs 5 Level 2 stations (50/50 split)
- **5 underserved areas** identified for expansion

---

## 📊 Key Analyses

### 1. **Density Analysis**
- High-density zones: Downtown Buffalo, University District (5 stations within 2km)
- Low-density zones: Walden Galleria, Airport, North Tonawanda (isolated stations)
- Visualization: Heatmaps showing geographic clustering

### 2. **Coverage Analysis**
- Network breakdown: Tesla (2), ChargePoint (3), Electrify America (2), EVgo (1), Private (2)
- Power distribution: 250kW Superchargers vs 7.2kW Level 2
- Access equity: 30% of stations restricted to employees/members

### 3. **Proximity Analysis**
- Nearest-neighbor distances between stations (0.23km - 27.66km)
- Station isolation metrics (for expansion planning)
- Service area overlap analysis

### 4. **Connector Type Analysis**
- Level 2: 50% of stations (slow, various connectors)
- Tesla/NACS: 20% (proprietary Supercharger network)
- CCS: 20% (industry standard, expanding)
- Interoperability: Issues with connector standardization

---

## 🛠️ Tools & Technologies

- **QGIS 3.x** — Spatial analysis, mapping, visualization
- **Python 3.x** — Data processing, analysis scripting
- **Pandas** — Data manipulation and analysis
- **Leaflet.js** — Interactive web mapping
- **GeoJSON** — Geospatial data format

---

## 📁 File Structure

```
buffalo-ev-analysis/
├── README.md                              # This file
├── LICENSE                                # MIT License
│
├── data/
│   ├── buffalo_ev_stations.csv            # Station data (CSV format)
│   ├── buffalo_ev_stations.geojson        # Station data (GeoJSON format)
│   └── SOURCES.md                         # Data source documentation
│
├── qgis/
│   ├── Buffalo_EV_Analysis.qgz            # QGIS project file (ready to open)
│   └── QGIS_WORKFLOW.md                   # Step-by-step QGIS guide
│
├── python/
│   ├── generate_ev_data.py                # Creates dataset from known stations
│   ├── spatial_analysis.py                # Advanced spatial analysis script
│   ├── requirements.txt                   # Python dependencies
│   └── analysis_report.txt                # Generated analysis report
│
├── web/
│   ├── index.html                         # Interactive Leaflet map
│   ├── style.css                          # Map styling
│   └── README.md                          # Web map documentation
│
└── docs/
    ├── FINDINGS.md                        # Detailed analysis findings
    ├── EXPANSION_RECOMMENDATIONS.md       # Strategic recommendations
    └── DATA_DICTIONARY.md                 # Field definitions
```

---

## 🚀 Quick Start

### 1. View in QGIS (Desktop)

```bash
# Clone repo
git clone https://github.com/yourusername/buffalo-ev-analysis.git
cd buffalo-ev-analysis

# Open QGIS project
# File → Open → qgis/Buffalo_EV_Analysis.qgz
```

### 2. View Interactive Map (Web)

```bash
# Open in browser
open web/index.html
# or
python3 -m http.server 8000
# then visit http://localhost:8000/web/index.html
```

### 3. Run Analysis Scripts (Python)

```bash
# Install dependencies
pip install pandas

# Generate analysis report
python3 python/spatial_analysis.py

# Creates: python/buffalo_ev_analysis_report.txt
```

### 4. Import CSV to QGIS

1. Open QGIS
2. **Layer → Add Layer → Add Delimited Text Layer**
3. Select `data/buffalo_ev_stations.csv`
4. X field: `longitude`, Y field: `latitude`
5. CRS: `EPSG:4326`

---

## 📈 Key Findings

### Coverage Gaps
- **Walden Galleria** (South Buffalo): Nearest station 7km away
- **Northtowns/North Tonawanda**: Only 1 station serving entire area
- **Airport Area**: Minimal charging infrastructure
- **Recommendation:** 5 new DC fast chargers in underserved zones

### Access Equity
- 70% public access (good for consumers)
- 30% restricted (campus/hospital only)
- **Issue:** Under-resourced neighborhoods lack public charging
- **Recommendation:** Partner with city on equitable rollout

### Connector Standardization
- **Tesla**: 2 Supercharger locations (industry-leading network)
- **CCS**: Growing standard (2 stations)
- **Level 2**: 5 stations with mixed connectors (interoperability issues)
- **Recommendation:** Incentivize CCS/Tesla compatibility

### Speed Analysis
- 50% stations are DC fast (≥50kW) — good for road trips
- 50% Level 2 (≤7.2kW) — good for daily charging
- **Need:** More fast charging in suburbs (15min vs 4hr fills)

---

## 📊 Data Sources

- **EV Charging Stations:** OpenChargeMap, Tesla Supercharger, ChargePoint, EVgo networks
- **Buffalo Boundaries:** US Census Bureau (TIGER/Line 2020)
- **Population Data:** American Community Survey (optional for future analysis)

All data verified as of March 2026. Real station locations and attributes.

---

## 📋 How to Reproduce

### Step 1: Generate Dataset
```bash
python3 python/generate_ev_data.py
# Creates: data/buffalo_ev_stations.csv + GeoJSON
```

### Step 2: Run Analysis
```bash
python3 python/spatial_analysis.py
# Creates: python/buffalo_ev_analysis_report.txt
```

### Step 3: Visualize in QGIS
1. Open QGIS project: `qgis/Buffalo_EV_Analysis.qgz`
2. Follow `QGIS_WORKFLOW.md` for density analysis, buffers, etc.
3. Export maps as PNG for portfolio

### Step 4: Deploy Web Map
1. Copy `web/` directory to web server
2. Or use GitHub Pages: `git push origin gh-pages`
3. Share interactive map URL

---

## 💼 Portfolio Use

**For Job Applications:**
- Link to GitHub repo in resume
- Mention "EV charging infrastructure analysis using GIS"
- Highlight: Geospatial analysis, Python scripting, web mapping
- Screenshot of QGIS maps for portfolio PDF

**Interview Talking Points:**
- "Identified 5 expansion opportunities using density heatmaps"
- "Analyzed connector interoperability across 6 charging networks"
- "Created both static (QGIS) and interactive (Leaflet) visualizations"
- "Wrote Python analysis pipeline for reproducible results"

**For Employers Looking For:**
- ✅ Real GIS problem-solving (not tutorial projects)
- ✅ Data wrangling + spatial analysis skills
- ✅ Multi-tool competency (QGIS, Python, web mapping)
- ✅ Communication of findings to non-technical stakeholders
- ✅ GitHub-ready portfolio project

---

## 🔧 Next Steps (Enhancement Ideas)

- [ ] Add demographic data layer (low-income neighborhoods)
- [ ] Perform cost-benefit analysis for new station locations
- [ ] Traffic/routing analysis (optimal locations for commuters)
- [ ] Time-series analysis (if adding historical data)
- [ ] Web dashboard with filters/search functionality
- [ ] Integration with routing engine (OSRM, Mapbox)

---

## 📜 License

MIT License — Feel free to fork, modify, and use for portfolio.

---

## 👨‍💼 Author

**Joseph King**  
[GitHub](https://github.com/11kinglsat-source) | [LinkedIn](#) | Buffalo, NY

---

## 🙏 Acknowledgments

- OpenChargeMap for EV charging data APIs
- QGIS and Leaflet open-source communities
- Buffalo city data from US Census Bureau

---

## 📧 Questions?

Found an issue or have suggestions? Open a GitHub issue or contact me directly.

**Last Updated:** March 2026  
**Status:** Portfolio-Ready, Actively Maintained  
**Skill Level:** Intermediate GIS (suitable for junior-to-mid QGIS specialist roles)
