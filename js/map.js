
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

export function initMarsMap() {
    const container = document.getElementById("mars-container");
    const loading = document.getElementById("loading-screen");
    const systemStatus = document.getElementById("system-status");

    const scene = new THREE.Scene();

    const camera = new THREE.PerspectiveCamera(
        45,
        container.clientWidth / container.clientHeight,
        0.1,
        100
    );

    camera.position.set(0, 0, 6);

    const renderer = new THREE.WebGLRenderer({
        antialias: true,
        alpha: true
    });

    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.outputColorSpace = THREE.SRGBColorSpace;

    container.appendChild(renderer.domElement);

    const controls = new OrbitControls(
        camera,
        renderer.domElement
    );

    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minDistance = 2.6;
    controls.maxDistance = 22;
    controls.autoRotate = true;
    controls.autoRotateSpeed = 0.35;

    scene.add(new THREE.AmbientLight(0xffffff, 1.5));

    const sunlight = new THREE.DirectionalLight(0xffffff, 2.5);
    sunlight.position.set(5, 3, 5);
    scene.add(sunlight);

    const globe = new THREE.Group();
    scene.add(globe);

    const textureLoader = new THREE.TextureLoader();

    let currentView = "global";
    let marsMaterial;
    let elevationTexture;
    let heightTexture;
    let regionalMesh;

    function loadTexture(path) {
        return new Promise((resolve, reject) => {
            textureLoader.load(
                path,
                resolve,
                undefined,
                reject
            );
        });
    }

    // GLOBAL MARS GLOBE

    const globeGeometry = new THREE.SphereGeometry(
        2,
        512,
        256
    );

    async function loadMars() {
        try {
            const [colorMap, heightMap] = await Promise.all([
                loadTexture("assets/images/mars-elevation.png"),
                loadTexture("assets/images/mars-height.png")
            ]);

            elevationTexture = colorMap;
            heightTexture = heightMap;

            elevationTexture.colorSpace = THREE.SRGBColorSpace;

            elevationTexture.anisotropy =
                renderer.capabilities.getMaxAnisotropy();

            marsMaterial = new THREE.MeshStandardMaterial({
                map: elevationTexture,
                displacementMap: heightTexture,
                displacementScale: 0.13,
                displacementBias: -0.065,
                roughness: 1,
                metalness: 0
            });

            const marsMesh = new THREE.Mesh(
                globeGeometry,
                marsMaterial
            );

            globe.add(marsMesh);

            const atmosphere = new THREE.Mesh(
                new THREE.SphereGeometry(2.055, 96, 96),
                new THREE.MeshBasicMaterial({
                    color: 0xd68c68,
                    transparent: true,
                    opacity: 0.09,
                    side: THREE.BackSide
                })
            );

            globe.add(atmosphere);

            if (currentView === "global") {
                loading.style.display = "none";
            }

            systemStatus.textContent = "MOLA DATA LOADED";

            console.log("MOLA global terrain loaded.");

        } catch (error) {
            console.error("MOLA loading failed:", error);

            loading.querySelector("p").textContent =
                "MOLA TEXTURES NOT FOUND";

            loading.querySelector("span").textContent =
                "CHECK ASSETS/IMAGES";

            systemStatus.textContent = "MOLA DATA ERROR";
        }
    }

    // EAST MELAS REGIONAL TERRAIN

    async function loadRegionalTerrain() {
        try {
            const [colorMap, heightMap] = await Promise.all([
                loadTexture("assets/images/east-melas-ctx.png"),
                loadTexture("assets/images/east-melas-height.png")
            ]);

            colorMap.colorSpace = THREE.SRGBColorSpace;

            colorMap.anisotropy =
                renderer.capabilities.getMaxAnisotropy();

            const terrainWidth = 3.6;
            const terrainHeight = terrainWidth * (2650 / 1024);

            const geometry = new THREE.PlaneGeometry(
                terrainWidth,
                terrainHeight,
                256,
                662
            );

            const material = new THREE.MeshStandardMaterial({
                map: colorMap,
                displacementMap: heightMap,
                displacementScale: 0.12,
                displacementBias: -0.06,
                roughness: 1,
                metalness: 0,
                side: THREE.DoubleSide,
                transparent: true,
                alphaTest: 0.01
            });

            regionalMesh = new THREE.Mesh(
                geometry,
                material
            );

            regionalMesh.visible = false;

            scene.add(regionalMesh);

            console.log("East Melas CTX terrain loaded.");

            if (currentView === "regional") {
                setView("regional");
            }

        } catch (error) {
            console.error("CTX terrain loading failed:", error);

            systemStatus.textContent = "CTX DATA ERROR";
        }
    }

    // STAR BACKGROUND

    const starGeometry = new THREE.BufferGeometry();
    const starPositions = [];

    for (let i = 0; i < 1800; i++) {
        starPositions.push(
            (Math.random() - 0.5) * 100,
            (Math.random() - 0.5) * 100,
            (Math.random() - 0.5) * 100
        );
    }

    starGeometry.setAttribute(
        "position",
        new THREE.Float32BufferAttribute(starPositions, 3)
    );

    const stars = new THREE.Points(
        starGeometry,
        new THREE.PointsMaterial({
            color: 0xffffff,
            size: 0.07,
            sizeAttenuation: true
        })
    );

    scene.add(stars);

    // VIEW MANAGEMENT

    function setView(view) {
        currentView = view;

        const isRegional = view === "regional";

        globe.visible = !isRegional;

        if (regionalMesh) {
            regionalMesh.visible = isRegional;
        }

        controls.target.set(0, 0, 0);

        if (isRegional) {
            camera.position.set(0, 0, 13.5);

            controls.minDistance = 5;
            controls.maxDistance = 22;
            controls.autoRotate = false;

            systemStatus.textContent = regionalMesh
                ? "CTX DATA LOADED"
                : "LOADING CTX DATA";

        } else {
            camera.position.set(0, 0, 6);

            controls.minDistance = 2.6;
            controls.maxDistance = 9;
            controls.autoRotate = true;

            systemStatus.textContent = "MOLA GLOBAL VIEW";
        }

        controls.update();

        const information = document.querySelector(
            ".planet-information"
        );

        if (information) {
            information.querySelector("span").textContent =
                isRegional ? "REGIONAL TERRAIN" : "PLANETARY BODY";

            information.querySelector("h3").textContent =
                isRegional ? "EAST MELAS" : "MARS";

            information.querySelector("small").textContent =
                isRegional
                    ? "CTX HIGH-RESOLUTION DEM"
                    : "GLOBAL TOPOGRAPHY";
        }

        const rotationButton = document.getElementById(
            "rotation-toggle"
        );

        rotationButton.textContent = isRegional
            ? "ROTATION DISABLED"
            : "PAUSE ROTATION";
    }

    // LAYER MANAGEMENT

    function setElevationVisible(visible) {
        if (!marsMaterial) return;

        marsMaterial.map = visible
            ? elevationTexture
            : null;

        marsMaterial.displacementMap = visible
            ? heightTexture
            : null;

        marsMaterial.needsUpdate = true;
    }

    // ROTATION

    function setRotation(enabled) {
        controls.autoRotate =
            enabled && currentView === "global";

        const rotationButton = document.getElementById(
            "rotation-toggle"
        );

        rotationButton.textContent = controls.autoRotate
            ? "PAUSE ROTATION"
            : "START ROTATION";
    }

    // RESET CAMERA

    function resetView() {
        setView(currentView);
    }

    document.getElementById("reset-view")
        .addEventListener("click", resetView);

    const rotationButton = document.getElementById(
        "rotation-toggle"
    );

    rotationButton.addEventListener("click", () => {
        if (currentView === "regional") return;

        setRotation(!controls.autoRotate);
    });

    // RESPONSIVE VIEWPORT

    const resizeObserver = new ResizeObserver(() => {
        const width = container.clientWidth;
        const height = container.clientHeight;

        if (!width || !height) return;

        camera.aspect = width / height;
        camera.updateProjectionMatrix();

        renderer.setSize(width, height);
    });

    resizeObserver.observe(container);

    // ANIMATION LOOP

    function animate() {
        requestAnimationFrame(animate);

        controls.update();
        renderer.render(scene, camera);
    }

    // INITIALIZE

    loadMars();
    loadRegionalTerrain();

    animate();

    return {
        setElevationVisible,
        setRotation,
        resetView,
        setView
    };
}
