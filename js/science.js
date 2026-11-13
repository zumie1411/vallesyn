
export function initScience() {
    const pageHeading = document.querySelector(".page-heading");
    const marsWorkspace = document.querySelector(".mars-workspace");
    const bottomInformation = document.querySelector(".bottom-information");

    if (!pageHeading) return;

    const sciencePages = {
        terrain: {
            sections: [
                {
                    title: "Processed Elevation Model",
                    description: "Visual representation of processed East Melas terrain elevation.",
                    image: "assets/images/working_dem_visualization.png"
                },
                {
                    title: "Slope Classification",
                    description: "Categorized terrain slope data for regional analysis.",
                    image: "assets/images/east_melas_slope_classes.png"
                }
            ]
        },
        elevation: {
            sections: [
                {
                    title: "Digital Elevation Model",
                    description: "Processed elevation visualization of East Melas.",
                    image: "assets/images/working_dem_visualization.png"
                }
            ]
        },
        slope: {
            sections: [
                {
                    title: "Slope Visualization",
                    description: "Calculated terrain slope across East Melas.",
                    image: "assets/images/east_melas_slope_visualization.png"
                },
                {
                    title: "Slope Classification",
                    description: "Terrain classified into slope categories.",
                    image: "assets/images/east_melas_slope_classes.png"
                }
            ]
        },
        roughness: {
            sections: [
                {
                    title: "MOLA Roughness Reference",
                    description: "Rendered RGB reference image, not a numerical roughness measurement.",
                    image: "assets/images/east-melas-roughness-reference.png"
                }
            ]
        }
    };

    const style = document.createElement("style");
    style.textContent = `
        .science-dashboard {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 18px;
            width: 100%;
            margin-top: 22px;
        }

        .science-card {
            min-width: 0;
            padding: 18px;
            border: 1px solid rgba(130,160,190,.2);
            border-radius: 12px;
            background: rgba(15,25,40,.65);
        }

        .science-card h3 {
            margin: 0 0 9px;
            font-size: 14px;
        }

        .science-card p {
            font-size: 12px;
            line-height: 1.6;
            opacity: .75;
        }

        .science-card img {
            display: block;
            width: 100%;
            max-height: 390px;
            object-fit: contain;
            border-radius: 7px;
            background: #101722;
        }

        .science-label {
            display: inline-block;
            margin-bottom: 12px;
            font-size: 10px;
            letter-spacing: 1.5px;
            opacity: .65;
        }

        @media(max-width:800px) {
            .science-dashboard {
                grid-template-columns: 1fr;
            }
        }
    `;

    document.head.appendChild(style);

    const dashboard = document.createElement("section");
    dashboard.id = "science-dashboard";
    dashboard.className = "science-dashboard";
    dashboard.hidden = true;

    pageHeading.insertAdjacentElement("afterend", dashboard);

    function showSciencePage(page) {
        const data = sciencePages[page];

        if (!data) {
            dashboard.hidden = true;
            return;
        }

        dashboard.innerHTML = data.sections.map(section => `
            <article class="science-card">
                <span class="science-label">VALLESYN / SCIENTIFIC DATA</span>
                <h3>${section.title}</h3>
                <p>${section.description}</p>
                <img src="${section.image}" alt="${section.title}">
            </article>
        `).join("");

        dashboard.hidden = false;

        if (marsWorkspace) marsWorkspace.hidden = true;
        if (bottomInformation) bottomInformation.hidden = true;
    }

    document.addEventListener("vallesyn-science-page", event => {
        showSciencePage(event.detail.page);
    });

    window.VallesynScience = {
        show: showSciencePage
    };

    console.log("Vallesyn Science initialized.");
}

