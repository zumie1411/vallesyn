export function initCrewSupport() {
    const root = document.getElementById("crew-support");
    if (!root) return;

    const terrain = document.getElementById("crew-terrain-condition");
    const dust = document.getElementById("crew-dust-condition");
    const radiation = document.getElementById("crew-radiation-status");
    const advisory = document.getElementById("crew-advisory-output");
    const checks = [...root.querySelectorAll("[data-eva-check]")];
    const checkCount = document.getElementById("eva-check-count");
    const checkFill = document.getElementById("eva-check-fill");
    const message = document.getElementById("crew-message");
    const delay = document.getElementById("crew-delay");
    const send = document.getElementById("crew-send");
    const receive = document.getElementById("crew-receive");
    const commsStatus = document.getElementById("crew-comms-status");
    const commsLog = document.getElementById("crew-comms-log");
    let pendingMessage = "";

    function updateAdvisory() {
        const items = [];
        if (terrain.value === "steep") items.push("Steep terrain selected: review the local slope product, route geometry and alternate path before any simulated traverse.");
        if (terrain.value === "loose") items.push("Loose or rocky surface selected: request higher-resolution imagery and mobility review; orbital data alone cannot confirm footing.");
        if (terrain.value === "unknown") items.push("Terrain condition unknown: treat this as an information gap and obtain additional imagery or measurements.");
        if (dust.value === "observed") items.push("Dust observed: review suit dust-control procedures, equipment seals and visibility impacts using mission-approved procedures.");
        if (dust.value === "unknown") items.push("Dust conditions unavailable: no local dust sensor feed is connected to Vallesyn.");
        if (radiation.value === "unavailable") items.push("Radiation forecast unavailable: Vallesyn has no radiation sensor or forecast feed. Consult validated mission radiation data.");
        if (radiation.value === "review") items.push("Radiation data marked for review: confirm current exposure forecasts and mission limits with qualified flight operations.");
        advisory.innerHTML = items.map(item => "<li>" + escapeHTML(item) + "</li>").join("");
        if (!items.length) advisory.innerHTML = "<li>No concerns selected. This does not mean the area is safe; verify all conditions with validated mission data.</li>";
    }

    function escapeHTML(value) {
        return String(value).replace(/[&<>"']/g, char => ({
            "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;"
        })[char]);
    }

    function updateChecks() {
        const complete = checks.filter(item => item.checked).length;
        checkCount.textContent = complete + " / " + checks.length + " reviewed";
        checkFill.style.width = (complete / checks.length * 100) + "%";
    }

    [terrain, dust, radiation].forEach(control => control.addEventListener("change", updateAdvisory));
    checks.forEach(control => control.addEventListener("change", updateChecks));

    send.addEventListener("click", () => {
        const text = message.value.trim();
        if (!text) {
            commsStatus.textContent = "Enter a mission message first.";
            return;
        }
        pendingMessage = text;
        const oneWay = Number(delay.value);
        commsStatus.textContent = "SIMULATION: message queued for a " + oneWay + "-minute one-way transit. No real transmission occurred.";
        commsLog.textContent = "OUTBOUND · " + new Date().toLocaleTimeString() + " · " + text;
        receive.hidden = false;
        send.disabled = true;
    });

    receive.addEventListener("click", () => {
        if (!pendingMessage) return;
        const oneWay = Number(delay.value);
        commsStatus.textContent = "SIMULATION COMPLETE: arrival acknowledged after the simulated " + oneWay + "-minute one-way delay. Estimated round trip: " + (oneWay * 2) + " minutes.";
        commsLog.textContent = "SIMULATED ARRIVAL · " + pendingMessage;
        pendingMessage = "";
        receive.hidden = true;
        send.disabled = false;
    });

    document.getElementById("crew-open-slope").addEventListener("click", () => {
        document.querySelector('[data-page="slope"]')?.click();
    });

    updateAdvisory();
    updateChecks();
    console.log("Vallesyn Crew Support initialized.");
}
