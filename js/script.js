
import { initMarsMap } from "./map.js";
import { initLayers } from "./layers.js";
import { initNavigation } from "./navigation.js";
import { initScience } from "./science.js";
import { initPlanner } from "./planner.js";
import { initEnvironment } from "./enviroment.js";\nimport { initMissionConsole } from "./mission-console.js";

function initializeVallesyn() {
    console.log("Initializing Vallesyn...");

    initEnvironment();

    const marsMap = initMarsMap();

    initLayers(marsMap);
    initNavigation(marsMap);
    initScience();
    initPlanner();\n    initMissionConsole();

    window.Vallesyn = {
        marsMap
    };

    console.log("Vallesyn initialized successfully.");
}

if (document.readyState === "loading") {
    document.addEventListener(
        "DOMContentLoaded",
        initializeVallesyn,
        { once: true }
    );
} else {
    initializeVallesyn();
}
