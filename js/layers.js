
export function initLayers(marsMap) {
    const heading = document.querySelector(".page-heading");

    if (!heading) return;

    const panel = document.createElement("section");
    panel.id = "layers-dashboard";
    panel.hidden = true;

    panel.innerHTML = `
        <div class="layers-intro">
            <h2>Planetary Data Catalogue</h2>
            <p>Manage the scientific datasets powering Vallesyn's 3D environment.</p>
        </div>

        <div class="layers-grid">
            <article class="layer-card">
                <span class="layer-tag">GLOBAL DATASET</span>
                <h3>MOLA Global Elevation</h3>
                <p>NASA Mars Orbiter Laser Altimeter global digital elevation model.</p>
                <div class="layer-details">
                    <span>23041 × 46081</span>
                    <span>INT16</span>
                    <span>Global coverage</span>
                </div>
                <button data-action="global">View Global Dataset</button>
                <button data-action="elevation" class="secondary">Toggle Elevation</button>
            </article>

            <article class="layer-card">
                <span class="layer-tag">REGIONAL DATASET</span>
                <h3>East Melas CTX</h3>
                <p>High-resolution regional terrain data from the CTX digital elevation model.</p>
                <div class="layer-details">
                    <span>21833 × 8428</span>
                    <span>FLOAT32</span>
                    <span>24 m / pixel</span>
                </div>
                <button data-action="regional">View Regional Dataset</button>
            </article>

            <article class="layer-card">
                <span class="layer-tag">TERRAIN ANALYSIS</span>
                <h3>Slope Classification</h3>
                <p>Processed slope classes derived from the East Melas terrain model.</p>
                <div class="layer-details">
                    <span>Processed raster</span>
                    <span>East Melas</span>
                </div>
                <button data-action="slope">Open Slope Analysis</button>
            </article>

            <article class="layer-card">
                <span class="layer-tag">REFERENCE DATA</span>
                <h3>MOLA Roughness Reference</h3>
                <p>Regional crop of a rendered global roughness map. This is a visual reference, not a numerical roughness measurement.</p>
                <div class="layer-details">
                    <span>RGB image</span>
                    <span>Reference only</span>
                </div>
                <button data-action="roughness">Open Roughness Reference</button>
            </article>
        </div>
    `;

    heading.insertAdjacentElement("afterend", panel);

    const style = document.createElement("style");
    style.textContent = `
        #layers-dashboard {
            width: 100%;
            padding: 24px 0;
        }

        .layers-intro {
            margin-bottom: 24px;
        }

        .layers-intro h2 {
            margin-bottom: 8px;
        }

        .layers-intro p {
            color: #9aa8bd;
        }

        .layers-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 18px;
        }

        .layer-card {
            padding: 22px;
            border: 1px solid rgba(120, 160, 210, 0.2);
            border-radius: 12px;
            background: rgba(15, 28, 48, 0.8);
        }

        .layer-tag {
            color: #68baff;
            font-size: 11px;
            letter-spacing: 1.5px;
        }

        .layer-card h3 {
            margin: 14px 0 10px;
        }

        .layer-card p {
            color: #aab7ca;
            line-height: 1.6;
            min-height: 50px;
        }

        .layer-details {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 18px 0;
        }

        .layer-details span {
            padding: 6px 9px;
            border-radius: 5px;
            background: rgba(100, 150, 210, 0.12);
            color: #b9cce3;
            font-size: 11px;
        }

        .layer-card button {
            margin: 5px 5px 0 0;
            padding: 10px 13px;
            border: 0;
            border-radius: 6px;
            background: #287cc0;
            color: white;
            cursor: pointer;
        }

        .layer-card button.secondary {
            background: #34465e;
        }

        @media (max-width: 700px) {
            .layers-grid {
                grid-template-columns: 1fr;
            }
        }
    `;

    document.head.appendChild(style);

    panel.addEventListener("click", event => {
        const button = event.target.closest("button[data-action]");
        if (!button) return;

        const action = button.dataset.action;

        if (action === "global") marsMap.setView("global");
        if (action === "regional") marsMap.setView("regional");

        if (action === "elevation") {
            marsMap.setElevationVisible(true);
        }

        if (action === "slope") {
            document.querySelector('[data-page="slope"]')?.click();
        }

        if (action === "roughness") {
            document.querySelector('[data-page="roughness"]')?.click();
        }
    });

    function updateVisibility(page) {
        panel.hidden = page !== "layers";
    }

    document.querySelectorAll(".nav-button").forEach(button => {
        button.addEventListener("click", () => {
            updateVisibility(button.dataset.page);
        });
    });

    window.VallesynLayers = {
        show: () => updateVisibility("layers")
    };

    console.log("Vallesyn Data Layers initialized.");
}
