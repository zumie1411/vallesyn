# VALLESYN
### Scientific 3D Mars Exploration & Terrain Intelligence Platform

Vallesyn is a web-based planetary exploration platform designed to visualize Martian topography and explore regional terrain characteristics using NASA planetary datasets.

## Overview

Vallesyn combines interactive 3D visualization with scientific terrain analysis to provide an accessible exploration environment for Mars.

## Features

- **Global Mars Explorer** — Interactive 3D Mars globe using MOLA elevation data.
- **Regional Explorer** — High-resolution East Melas terrain visualization using CTX DEM data.
- **Terrain Analysis** — Processed elevation and slope visualizations.
- **Elevation Analysis** — Regional digital elevation model exploration.
- **Slope Analysis** — Terrain slope calculation and five-class slope categorization.
- **Surface Roughness** — MOLA-derived rendered roughness reference visualization.
- **Data Layers** — Dataset exploration and visualization controls.
- **Mission Planner** — Select exploration regions and save mission notes during a session.

## Data Sources

- NASA Mars Orbiter Laser Altimeter (MOLA)
- Mars Reconnaissance Orbiter Context Camera (CTX) terrain data

## Technology Stack

- HTML5
- CSS3
- JavaScript (ES Modules)
- Three.js
- Python
- NumPy
- Rasterio
- Matplotlib
- Pillow

## Project Structure

```text
vallesyn/
├── assets/
│   └── images/
├── css/
│   ├── style.css
│   └── responsive.css
├── js/
│   ├── script.js
│   ├── map.js
│   ├── layers.js
│   ├── navigation.js
│   ├── science.js
│   ├── planner.js
│   └── enviroment.js
├── data/
│   └── (local scientific datasets)
├── index.html
└── README.md
```

## Running Locally

1. Clone the repository:

```bash
git clone https://github.com/zumie1411/vallesyn.git
```

2. Open the project folder:

```bash
cd vallesyn
```

3. Start a local server:

```bash
python -m http.server 8000
```

4. Open:

```text
http://localhost:8000
```

## Scientific Notes

Slope classifications use project-defined thresholds. The roughness reference is a rendered RGB visualization, not a numerical roughness measurement.

Scientific results should be interpreted with consideration of source resolution, projection, data coverage, and processing assumptions.

## Project Status

Development build. Features and scientific processing workflows may continue to evolve.

---

**Vallesyn — Exploring the Martian Surface Through Data and Visualization.**
