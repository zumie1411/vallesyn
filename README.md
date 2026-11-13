# 🔴 VALLESYN
### Explore Mars. Understand the terrain. Imagine the next mission.

<p align="center">
  <a href="https://vallesyn.onrender.com"><strong>🚀 Open Live Website</strong></a>
  &nbsp;•&nbsp;
  <a href="https://github.com/zumie1411/vallesyn"><strong>💻 View Source Code</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Web%20Application-e45b35?style=for-the-badge" alt="Web application">
  <img src="https://img.shields.io/badge/Focus-Mars%20Terrain-252525?style=for-the-badge" alt="Mars terrain">
  <img src="https://img.shields.io/badge/Data-NASA%20Planetary%20Datasets-1d5b91?style=for-the-badge" alt="NASA planetary datasets">
</p>

**Vallesyn** is a web-based Mars exploration and terrain intelligence project. It brings planetary data and interactive 3D visualisation together to make the Martian surface easier to explore and understand.

## 🌐 Explore Vallesyn

<p align="center">
  <a href="https://vallesyn.onrender.com">
    <img src="https://img.shields.io/badge/LAUNCH%20VALLESYN-Open%20the%20live%20experience-e45b35?style=for-the-badge" alt="Launch Vallesyn">
  </a>
</p>

## 🪐 What you can explore

- **Global Mars Explorer** — Explore Mars through an interactive 3D globe.
- **Regional Terrain Explorer** — Investigate the East Melas region using terrain data.
- **Elevation & Slope** — Visualise elevation and project-defined slope classes.
- **Surface Visualisation** — Switch between available scientific data layers.
- **Mission Planner** — Select exploration areas and keep mission notes during a session.

## 🛰️ Data behind the experience

Vallesyn works with planetary datasets including:

- **MOLA** — Mars Orbiter Laser Altimeter elevation data.
- **CTX** — Context Camera terrain data from the Mars Reconnaissance Orbiter.

The datasets are processed and visualised to support exploration of Martian topography.

## ⚙️ Built with

| Area | Tools |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| 3D visualisation | Three.js |
| Data processing | Python, NumPy, Rasterio |
| Visualisation utilities | Matplotlib, Pillow |
| Deployment | Render |

## 🧭 Run locally

You will need Python installed.

```bash
git clone https://github.com/zumie1411/vallesyn.git
cd vallesyn
python -m http.server 8000
```

Then open **http://localhost:8000** in your browser.

## 📁 Project layout

```text
vallesyn/
├── assets/
├── css/
├── js/
├── data/
├── mission-portal/
│   ├── index.html
│   ├── css/
│   └── js/
├── index.html
└── README.md
```

## 🔬 Scientific context

Vallesyn is an exploration and visualisation project, not a substitute for peer-reviewed scientific analysis. Slope classes use project-defined thresholds, and the roughness layer is a rendered visual reference rather than a numerical roughness measurement. Interpret visualisations in the context of dataset resolution, coverage, projection, and processing assumptions.

## 🚧 Project status

Vallesyn is an evolving project. Features, datasets, and analysis workflows may change as development continues.

---

<p align="center">
  **VALLESYN** · A closer look at the Red Planet.
</p>
