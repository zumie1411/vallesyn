
export function initMissionConsole() {
    const form = document.getElementById("brief-form");
    if (!form) return;

    const ids = ["check-elevation", "check-slope", "check-ctx", "check-limitations"];
    const readinessNumber = document.getElementById("readiness-number");
    const readinessFill = document.getElementById("readiness-fill");
    const readinessCopy = document.getElementById("readiness-copy");
    const feedback = document.getElementById("brief-feedback");
    const notesBox = document.getElementById("field-notes");
    const storageKey = "vallesyn-field-notes-v1";

    function getNotes() {
        try { return JSON.parse(localStorage.getItem(storageKey) || "[]"); }
        catch { return []; }
    }

    function renderNotes() {
        const notes = getNotes();
        notesBox.innerHTML = notes.length
            ? notes.map(note => `<article class="field-note"><strong>${escapeHTML(note.title)}</strong><small>${escapeHTML(note.date)} · ${escapeHTML(note.region)}</small><p>${escapeHTML(note.text)}</p></article>`).join("")
            : '<p class="empty-notes">No field notes saved yet.</p>';
    }

    function escapeHTML(value) {
        return String(value).replace(/[&<>"']/g, char => ({
            "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;"
        })[char]);
    }

    function updateReadiness() {
        const complete = ids.filter(id => document.getElementById(id).checked).length;
        readinessNumber.innerHTML = complete + '<span>/4</span>';
        readinessFill.style.width = (complete / 4 * 100) + "%";
        readinessCopy.textContent = complete === 4
            ? "Review checklist complete. Your investigation is ready to document."
            : complete + " of 4 review steps completed. This is a workflow checklist, not a safety rating.";
    }

    ids.forEach(id => document.getElementById(id).addEventListener("change", updateReadiness));

    function collectBrief() {
        return {
            title: document.getElementById("brief-title").value.trim(),
            region: document.getElementById("brief-region").value.trim(),
            objective: document.getElementById("brief-objective").value,
            coordinates: document.getElementById("brief-coordinates").value.trim(),
            observations: document.getElementById("brief-observations").value.trim(),
            checklist: ids.map(id => ({
                label: document.querySelector('label[for="' + id + '"]')?.textContent || ({
                    "check-elevation":"Elevation layer reviewed",
                    "check-slope":"Slope layer reviewed",
                    "check-ctx":"CTX imagery reviewed",
                    "check-limitations":"Data limitations considered"
                })[id],
                complete: document.getElementById(id).checked
            })),
            generated: new Date().toLocaleString()
        };
    }

    form.addEventListener("submit", event => {
        event.preventDefault();
        const brief = collectBrief();
        if (!brief.title || !brief.region) {
            feedback.textContent = "Add an investigation title and region first.";
            return;
        }
        const report = [
            "VALLESYN | SCIENTIFIC MISSION BRIEF",
            "====================================",
            "Title: " + brief.title,
            "Region: " + brief.region,
            "Objective: " + brief.objective,
            "Reference coordinates: " + (brief.coordinates || "Not supplied"),
            "Generated: " + brief.generated,
            "",
            "SCIENTIFIC OBSERVATIONS",
            brief.observations || "No observations entered.",
            "",
            "REVIEW CHECKLIST",
            ...brief.checklist.map(item => (item.complete ? "[x] " : "[ ] ") + item.label),
            "",
            "DATA CONTEXT",
            "Project layers include NASA MOLA elevation data and CTX imagery where available.",
            "Interpretations must account for source resolution, coverage, projection and NoData limitations.",
            "",
            "DISCLAIMER",
            "This is a user-generated research note, not a validated scientific assessment or landing-site safety certification."
        ].join("\n");
        const blob = new Blob([report], {type:"text/plain;charset=utf-8"});
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = "Vallesyn-Mission-Brief.txt";
        link.click();
        URL.revokeObjectURL(url);
        feedback.textContent = "Mission brief generated. Your text report has been downloaded.";
    });

    document.getElementById("save-observation").addEventListener("click", () => {
        const brief = collectBrief();
        const notes = getNotes();
        if (!brief.observations) {
            feedback.textContent = "Write an observation before saving a field note.";
            return;
        }
        notes.unshift({
            title: brief.title || "Untitled observation",
            region: brief.region || "Unspecified region",
            text: brief.observations,
            date: new Date().toLocaleString()
        });
        localStorage.setItem(storageKey, JSON.stringify(notes.slice(0, 12)));
        renderNotes();
        feedback.textContent = "Field note saved in this browser.";
    });

    document.getElementById("clear-notes").addEventListener("click", () => {
        localStorage.removeItem(storageKey);
        renderNotes();
        feedback.textContent = "Local field notes cleared.";
    });

    renderNotes();
    updateReadiness();
    console.log("Vallesyn Mission Brief Studio initialized.");
}
