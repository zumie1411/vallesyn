export function initEnvironmentIntel() {
    const note = document.getElementById("environment-note");
    const save = document.getElementById("environment-save-note");
    const status = document.getElementById("environment-note-status");
    const list = document.getElementById("environment-saved-notes");
    if (note && save && status && list) initNotebook(note, save, status, list);
    initMedaAnalyzer();
}

function initNotebook(note, save, status, list) {
    const storageKey = "vallesyn-environment-observations";
    function readNotes() {
        try {
            const value = JSON.parse(localStorage.getItem(storageKey) || "[]");
            return Array.isArray(value) ? value : [];
        } catch { return []; }
    }
    function renderNotes() {
        const notes = readNotes();
        list.replaceChildren();
        if (!notes.length) { list.textContent = "No observations saved."; return; }
        notes.slice().reverse().forEach(item => {
            const entry = document.createElement("article");
            const time = document.createElement("small");
            const body = document.createElement("p");
            time.textContent = item.time;
            body.textContent = item.text;
            entry.append(time, body);
            list.append(entry);
        });
    }
    save.addEventListener("click", () => {
        const value = note.value.trim();
        if (!value) { status.textContent = "Enter an observation before saving."; return; }
        const notes = readNotes();
        notes.push({ time: new Date().toLocaleString(), text: value });
        try {
            localStorage.setItem(storageKey, JSON.stringify(notes.slice(-30)));
            note.value = "";
            status.textContent = "Observation saved in this browser.";
            renderNotes();
        } catch { status.textContent = "Could not save. Browser storage may be unavailable."; }
    });
    renderNotes();
}

function initMedaAnalyzer() {
    const fileInput = document.getElementById("meda-csv-file");
    const status = document.getElementById("meda-file-status");
    const xSelect = document.getElementById("meda-x-column");
    const ySelect = document.getElementById("meda-y-column");
    const plotButton = document.getElementById("meda-plot-button");
    const canvas = document.getElementById("meda-chart");
    const empty = document.getElementById("meda-chart-empty");
    const summary = document.getElementById("meda-summary");
    if (!fileInput || !status || !xSelect || !ySelect || !plotButton || !canvas) return;
    const ctx = canvas.getContext("2d");
    let headers = [];
    let rows = [];

    function parseCSV(text) {
        const lines = text.replace(/^\uFEFF/, "").split(/\r?\n/).filter(line => line.trim() && !line.trim().startsWith("#"));
        if (!lines.length) throw new Error("No tabular rows found.");
        function splitLine(line) {
            const out = []; let cell = ""; let quoted = false;
            for (let i = 0; i < line.length; i++) {
                const ch = line[i];
                if (ch === '"' && line[i + 1] === '"' && quoted) { cell += '"'; i++; }
                else if (ch === '"') quoted = !quoted;
                else if (ch === "," && !quoted) { out.push(cell.trim()); cell = ""; }
                else cell += ch;
            }
            out.push(cell.trim());
            return out;
        }
        const first = splitLine(lines[0]);
        const start = first.every(value => value === "" || !Number.isFinite(Number(value))) ? 0 : 1;
        const names = start === 0 ? first : first.map((_, i) => "Column " + (i + 1));
        const data = lines.slice(start + 1).map(splitLine).filter(row => row.length > 1);
        return { headers: names, rows: data };
    }

    function numericValues(index) {
        return rows.map(row => Number(String(row[index] ?? "").replace(/[<>]/g, ""))).filter(Number.isFinite);
    }

    function fillSelectors() {
        xSelect.replaceChildren(); ySelect.replaceChildren();
        headers.forEach((name, index) => {
            const x = document.createElement("option");
            x.value = String(index); x.textContent = name || "Column " + (index + 1);
            xSelect.append(x);
            const y = x.cloneNode(true); ySelect.append(y);
        });
        const numeric = headers.map((_, i) => i).filter(i => numericValues(i).length > 0);
        if (numeric.length) {
            ySelect.value = String(numeric.find(i => /temp|press|wind|speed|dust|radiation|flux|humid|value/i.test(headers[i])) ?? numeric[0]);
            xSelect.value = String(numeric.find(i => /sol|time|ltst|utc|lmst|sclk/i.test(headers[i])) ?? numeric[0]);
        }
        xSelect.disabled = ySelect.disabled = false;
        plotButton.disabled = false;
    }

    function drawPlot() {
        const xi = Number(xSelect.value), yi = Number(ySelect.value);
        const points = rows.map(row => ({ x: Number(String(row[xi] ?? "").replace(/[<>]/g, "")), y: Number(String(row[yi] ?? "").replace(/[<>]/g, "")) })).filter(p => Number.isFinite(p.x) && Number.isFinite(p.y));
        if (points.length < 2) {
            status.textContent = "Not enough numeric rows for these columns. Choose different fields.";
            summary.textContent = "No plot generated.";
            return;
        }
        const width = Math.max(320, canvas.clientWidth || 700);
        const height = 300;
        const ratio = window.devicePixelRatio || 1;
        canvas.width = width * ratio; canvas.height = height * ratio;
        canvas.style.height = height + "px";
        ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
        ctx.clearRect(0, 0, width, height);
        const pad = { left: 58, right: 18, top: 20, bottom: 42 };
        const xs = points.map(p => p.x), ys = points.map(p => p.y);
        const minX = Math.min(...xs), maxX = Math.max(...xs), minY = Math.min(...ys), maxY = Math.max(...ys);
        const spanX = maxX - minX || 1, spanY = maxY - minY || 1;
        const px = x => pad.left + (x - minX) / spanX * (width - pad.left - pad.right);
        const py = y => height - pad.bottom - (y - minY) / spanY * (height - pad.top - pad.bottom);
        ctx.strokeStyle = "#344359"; ctx.lineWidth = 1;
        for (let i = 0; i <= 4; i++) {
            const y = pad.top + i * (height - pad.top - pad.bottom) / 4;
            ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(width - pad.right, y); ctx.stroke();
        }
        ctx.fillStyle = "#91a1b6"; ctx.font = "10px monospace";
        ctx.fillText(String(maxY.toPrecision(5)), 5, pad.top + 4);
        ctx.fillText(String(minY.toPrecision(5)), 5, height - pad.bottom);
        ctx.fillText(String(minX.toPrecision(5)), pad.left, height - 14);
        ctx.fillText(String(maxX.toPrecision(5)), width - 70, height - 14);
        ctx.strokeStyle = "#e5a77c"; ctx.lineWidth = 1.8; ctx.beginPath();
        points.forEach((p, i) => { if (!i) ctx.moveTo(px(p.x), py(p.y)); else ctx.lineTo(px(p.x), py(p.y)); });
        ctx.stroke();
        ctx.fillStyle = "#f1c29b";
        points.forEach(p => { ctx.beginPath(); ctx.arc(px(p.x), py(p.y), 2, 0, Math.PI * 2); ctx.fill(); });
        empty.hidden = true;
        const mean = ys.reduce((a, b) => a + b, 0) / ys.length;
        summary.textContent = points.length + " plotted rows · " + headers[xi] + " vs " + headers[yi] + " · min " + minY.toPrecision(5) + " · max " + maxY.toPrecision(5) + " · mean " + mean.toPrecision(5);
    }

    fileInput.addEventListener("change", async () => {
        const file = fileInput.files?.[0];
        if (!file) return;
        if (file.size > 15 * 1024 * 1024) { status.textContent = "Please choose a CSV smaller than 15 MB."; return; }
        try {
            const parsed = parseCSV(await file.text());
            headers = parsed.headers; rows = parsed.rows;
            if (headers.length < 2 || !rows.length) throw new Error("Could not detect a usable CSV table.");
            fillSelectors();
            status.textContent = file.name + " · " + rows.length.toLocaleString() + " data rows · processed locally";
            empty.hidden = false;
            empty.textContent = "Choose columns and select PLOT DATA.";
            summary.textContent = "CSV loaded. Select the measurement and time/Sol columns.";
        } catch (error) {
            status.textContent = "CSV import failed: " + error.message;
            headers = []; rows = [];
            xSelect.disabled = ySelect.disabled = plotButton.disabled = true;
        }
    });
    plotButton.addEventListener("click", drawPlot);
    window.addEventListener("resize", () => { if (rows.length && !empty.hidden) drawPlot(); });
    console.log("Vallesyn MEDA CSV analyzer initialized.");
}
