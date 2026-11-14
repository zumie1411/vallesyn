export function initEnvironmentIntel() {
    const note = document.getElementById("environment-note");
    const save = document.getElementById("environment-save-note");
    const status = document.getElementById("environment-note-status");
    const list = document.getElementById("environment-saved-notes");
    if (!note || !save || !status || !list) return;

    const storageKey = "vallesyn-environment-observations";

    function readNotes() {
        try {
            const value = JSON.parse(localStorage.getItem(storageKey) || "[]");
            return Array.isArray(value) ? value : [];
        } catch {
            return [];
        }
    }

    function renderNotes() {
        const notes = readNotes();
        list.replaceChildren();
        if (!notes.length) {
            list.textContent = "No observations saved.";
            return;
        }
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
        if (!value) {
            status.textContent = "Enter an observation before saving.";
            return;
        }
        const notes = readNotes();
        notes.push({ time: new Date().toLocaleString(), text: value });
        try {
            localStorage.setItem(storageKey, JSON.stringify(notes.slice(-30)));
            note.value = "";
            status.textContent = "Observation saved in this browser.";
            renderNotes();
        } catch {
            status.textContent = "Could not save. Browser storage may be unavailable.";
        }
    });

    renderNotes();
    console.log("Vallesyn Environmental Intelligence initialized.");
}
