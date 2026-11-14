# 🔴 VALLESYN
### The Next Frontier Is Red.

<p align="center">
  <a href="https://vallesyn.onrender.com"><strong>🚀 Visit the Mission Portal</strong></a>
  &nbsp;•&nbsp;
  <a href="https://vallesyn.onrender.com/explorer.html"><strong>🪐 Open the Mars Terrain Explorer</strong></a>
  &nbsp;•&nbsp;
  <a href="https://github.com/zumie1411/vallesyn"><strong>💻 Source Code</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Web%20Application-e45b35?style=for-the-badge" alt="Web application">
  <img src="https://img.shields.io/badge/Focus-Mars%20Terrain-252525?style=for-the-badge" alt="Mars terrain">
  <img src="https://img.shields.io/badge/Data-NASA%20Planetary%20Datasets-1d5b91?style=for-the-badge" alt="NASA planetary datasets">
</p>

**Vallesyn** is a web-based Mars exploration and terrain intelligence project. It combines planetary datasets with interactive 3D visualisation to make the Martian surface easier to explore and understand.

## 🌐 Start exploring

1. **Visit the [Mission Portal](https://vallesyn.onrender.com/)** for the project introduction, mission, data, technology, and impact.
2. Select **Launch Vallesyn** to open the interactive Mars terrain explorer.
3. You can also [open the explorer directly](https://vallesyn.onrender.com/explorer.html).

## 🪐 Inside the platform

- **Global Mars Explorer** — Explore Mars through an interactive 3D globe.
- **Regional Terrain Explorer** — Investigate the East Melas region using terrain data.
- **Elevation & Slope** — Visualise elevation and project-defined slope classes.
- **Scientific Data Layers** — Switch between available terrain visualisations.
- **Mission Planner** — Select exploration areas and keep mission notes during a session.

## 🛰️ Data behind the experience

Vallesyn works with planetary datasets including:

- **MOLA** — Mars Orbiter Laser Altimeter elevation data.
- **CTX** — Context Camera imagery from the Mars Reconnaissance Orbiter.

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

Open **http://localhost:8000** to view the mission portal. Use **http://localhost:8000/explorer.html** to open the terrain explorer directly.

## 📁 Project layout

```text
vallesyn/
├── assets/                 # Application assets and visualisations
├── css/                    # Explorer stylesheets
├── js/                     # Explorer JavaScript modules
├── data/                   # Planetary datasets and processed data
├── mission-portal/
│   ├── index.html          # Intro / mission portal
│   ├── css/
│   └── js/
├── index.html              # Redirects to the mission portal
├── explorer.html           # Interactive Mars terrain explorer
└── README.md
```

## 🔬 Scientific context

Vallesyn is an exploration and visualisation project, not a substitute for peer-reviewed scientific analysis. Slope classes use project-defined thresholds, and the roughness layer is a rendered visual reference rather than a numerical roughness measurement. Interpret visualisations in the context of dataset resolution, coverage, projection, and processing assumptions.

## 🤖 Use of Super Intelligence (SI) Tools

Generative AI tools, including **ChatGPT**, were used during Vallesyn's development for brainstorming, technical explanations, coding assistance, debugging support, and drafting project documentation.

AI assistance supported the development process. The developer reviewed and adapted suggestions during implementation and tested the project's features. AI-generated assistance is not presented as NASA-produced scientific data, and the planetary datasets are credited to their original sources above.

## 🚧 Project status

Vallesyn is an evolving project. Features, datasets, and analysis workflows may change as development continues.

---

<p align="center">
  **VALLESYN** · Built with curiosity. Inspired by exploration.
</p>
