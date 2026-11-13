
export function initEnvironment() {
    const root = document.documentElement;

    const settings = {
        theme: "dark",
        reducedMotion: window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches
    };

    function setTheme(theme) {
        settings.theme = theme;

        if (theme === "dark") {
            root.dataset.theme = "dark";
        }
    }

    function getSettings() {
        return { ...settings };
    }

    setTheme(settings.theme);

    window.VallesynEnvironment = {
        setTheme,
        getSettings
    };

    console.log("Vallesyn environment initialized.");
}
