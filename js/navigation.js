
const pages = {
    global: {
        title: "Global Mars Explorer",
        description: "Explore Martian topography through global MOLA elevation data."
    },
    regional: {
        title: "Regional Explorer",
        description: "Explore the East Melas region using higher-resolution CTX terrain data."
    },
    terrain: {
        title: "Terrain Analysis",
        description: "Investigate Martian terrain characteristics and surface morphology."
    },
    layers: {
        title: "Data Layers",
        description: "Manage planetary elevation and imagery datasets."
    },
    elevation: {
        title: "Elevation Analysis",
        description: "Explore elevation variations across the Martian surface."
    },
    slope: {
        title: "Slope Analysis",
        description: "Investigate terrain inclination using processed DEM data."
    },
    roughness: {
        title: "Surface Roughness",
        description: "Explore surface texture and roughness references."
    },
    planner: {
        title: "Mission Planner",
        description: "Prepare and evaluate potential Martian exploration regions."
    },
    crew: {
        title: "Crew Support",
        description: "Review terrain observations, EVA planning reminders and simulated Earth–Mars communications."
    }
};

export function initNavigation(marsMap) {
    const buttons = document.querySelectorAll(".nav-button");

    const workspace = document.querySelector(".mars-workspace");
    const bottom = document.querySelector(".bottom-information");

    function navigateTo(page) {
        const details = pages[page];

        if (!details) return;

        buttons.forEach(button => {
            button.classList.toggle("active", button.dataset.page === page);
        });

        const title = document.getElementById("page-title");
        const description = document.getElementById("page-description");
        const eyebrow = document.querySelector(".eyebrow");

        if (title) title.textContent = details.title;
        if (description) description.textContent = details.description;
        if (eyebrow) {
            eyebrow.textContent = "PLANETARY SYSTEM / " + page.toUpperCase();
        }

        const isGlobePage = page === "global" || page === "regional";
        const isSciencePage = ["terrain", "elevation", "slope", "roughness"].includes(page);

        const science = document.getElementById("science-dashboard");
        const layers = document.getElementById("layers-dashboard");
        const planner = document.getElementById("mission-planner");
        const crew = document.getElementById("crew-support");

        if (science) science.hidden = true;
        if (layers) layers.hidden = true;
        if (planner) planner.hidden = true;
        if (crew) crew.hidden = page !== "crew";

        if (workspace) workspace.hidden = !isGlobePage;
        if (bottom) bottom.hidden = !isGlobePage;

        if (isGlobePage) {
            marsMap.setView(page);
        }

        if (isSciencePage) {
            window.VallesynScience?.show(page);
        }

        if (page === "layers") {
            if (layers) {
                layers.hidden = false;
            } else {
                window.VallesynLayers?.show();
            }
        }

        if (page === "planner") {
            if (planner) {
                planner.hidden = false;
            } else {
                window.VallesynPlanner?.show?.();
            }
        }
    }

    buttons.forEach(button => {
        button.addEventListener("click", () => {
            navigateTo(button.dataset.page);
        });
    });

    console.log("Vallesyn navigation initialized.");
}
