export function initMissionClock() {
    const root = document.getElementById("mission-clock");
    if (!root) return;

    const toggle = document.getElementById("mission-clock-toggle");
    const panel = document.getElementById("mission-clock-panel");
    const display = document.getElementById("mission-clock-display");
    const largeDisplay = document.getElementById("mission-clock-large");
    const startButton = document.getElementById("mission-clock-start");
    const resetButton = document.getElementById("mission-clock-reset");
    const stampButton = document.getElementById("mission-clock-stamp");
    const status = document.getElementById("mission-clock-status");
    const observations = document.getElementById("brief-observations");

    let elapsedBeforeStart = 0;
    let startedAt = null;
    let intervalId = null;

    function elapsedSeconds() {
        if (startedAt === null) return elapsedBeforeStart;
        return elapsedBeforeStart + Math.floor((Date.now() - startedAt) / 1000);
    }

    function formatTime(totalSeconds) {
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;
        return [hours, minutes, seconds].map(value => String(value).padStart(2, "0")).join(":");
    }

    function render() {
        const value = "T+" + formatTime(elapsedSeconds());
        display.textContent = value;
        largeDisplay.textContent = value;
        startButton.textContent = startedAt === null ? "START" : "PAUSE";
        status.textContent = startedAt === null ? "Clock paused" : "Session in progress";
    }

    function tick() {
        render();
    }

    toggle.addEventListener("click", () => {
        const isOpen = !panel.hidden;
        panel.hidden = isOpen;
        toggle.setAttribute("aria-expanded", String(!isOpen));
        toggle.querySelector(".clock-chevron").textContent = isOpen ? "＋" : "−";
    });

    startButton.addEventListener("click", () => {
        if (startedAt === null) {
            startedAt = Date.now();
            intervalId = window.setInterval(tick, 250);
        } else {
            elapsedBeforeStart = elapsedSeconds();
            startedAt = null;
            window.clearInterval(intervalId);
            intervalId = null;
        }
        render();
    });

    resetButton.addEventListener("click", () => {
        elapsedBeforeStart = 0;
        startedAt = null;
        if (intervalId !== null) window.clearInterval(intervalId);
        intervalId = null;
        render();
    });

    stampButton.addEventListener("click", () => {
        if (!observations) {
            status.textContent = "Open Mission Brief Studio to add a field note.";
            return;
        }
        const stamp = "[MET " + "T+" + formatTime(elapsedSeconds()) + "] ";
        const current = observations.value;
        observations.value = current ? current.replace(/\s*$/, "\n") + stamp : stamp;
        observations.focus();
        status.textContent = "Mission time added to observations.";
    });

    render();
    console.log("Vallesyn Mission Clock initialized.");
}
