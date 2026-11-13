
export function initPlanner() {
    const planner = {
        selectedRegion: "",
        notes: []
    };

    const style = document.createElement("style");

    style.textContent = `
        .mission-planner {
            margin-top: 22px;
            padding: 24px;
            border: 1px solid rgba(130,160,190,0.2);
            border-radius: 12px;
            background: rgba(15,25,40,0.7);
        }

        .mission-planner h3 {
            margin: 0 0 18px;
            font-size: 16px;
            letter-spacing: 1px;
        }

        .planner-field {
            display: grid;
            gap: 9px;
            margin-bottom: 18px;
        }

        .planner-field label {
            font-size: 11px;
            letter-spacing: 1px;
        }

        .planner-field select,
        .planner-field textarea {
            width: 100%;
            padding: 12px;
            color: inherit;
            background: #111c2b;
            border: 1px solid rgba(130,160,190,0.3);
            border-radius: 7px;
            font: inherit;
        }

        .planner-field textarea {
            min-height: 110px;
            resize: vertical;
        }

        .planner-action {
            padding: 11px 18px;
            border: 0;
            border-radius: 6px;
            cursor: pointer;
            color: white;
            background: #2876a8;
        }

        .planner-notes {
            display: grid;
            gap: 10px;
            margin-top: 20px;
        }

        .planner-note {
            padding: 13px;
            border-radius: 7px;
            background: rgba(80,110,140,0.15);
            font-size: 13px;
            overflow-wrap: anywhere;
        }

        .planner-note small {
            display: block;
            margin-top: 7px;
            opacity: 0.6;
        }
    `;

    document.head.appendChild(style);

    const dashboard = document.createElement("section");
    dashboard.className = "mission-planner";
    dashboard.id = "mission-planner";
    dashboard.hidden = true;

    dashboard.innerHTML = `
        <h3>MISSION PLANNING WORKSPACE</h3>

        <div class="planner-field">
            <label for="planner-region">EXPLORATION REGION</label>

            <select id="planner-region">
                <option value="">Select a region</option>
                <option value="East Melas">East Melas</option>
                <option value="Valles Marineris">Valles Marineris</option>
                <option value="Olympus Mons">Olympus Mons</option>
                <option value="Gale Crater">Gale Crater</option>
            </select>
        </div>

        <div class="planner-field">
            <label for="planner-notes-input">MISSION NOTES</label>

            <textarea
                id="planner-notes-input"
                placeholder="Write exploration objectives or observations..."
            ></textarea>
        </div>

        <button class="planner-action" id="planner-add-note">
            SAVE MISSION NOTE
        </button>

        <div class="planner-notes" id="planner-notes-list">
            <p>No mission notes added yet.</p>
        </div>
    `;

    const pageHeading = document.querySelector(".page-heading");

    if (pageHeading) {
        pageHeading.insertAdjacentElement("afterend", dashboard);
    }

    const regionSelect = dashboard.querySelector("#planner-region");
    const noteInput = dashboard.querySelector("#planner-notes-input");
    const addButton = dashboard.querySelector("#planner-add-note");
    const notesList = dashboard.querySelector("#planner-notes-list");

    function renderNotes() {
        notesList.innerHTML = "";

        if (planner.notes.length === 0) {
            notesList.innerHTML = "<p>No mission notes added yet.</p>";
            return;
        }

        planner.notes.forEach(note => {
            const card = document.createElement("article");
            card.className = "planner-note";

            const text = document.createElement("div");
            text.textContent = note.text;

            const date = document.createElement("small");
            date.textContent = new Date(note.createdAt).toLocaleString();

            card.append(text, date);
            notesList.appendChild(card);
        });
    }

    regionSelect.addEventListener("change", () => {
        planner.selectedRegion = regionSelect.value;
    });

    addButton.addEventListener("click", () => {
        const text = noteInput.value.trim();

        if (!planner.selectedRegion) {
            alert("Please select an exploration region.");
            return;
        }

        if (!text) {
            alert("Please enter a mission note.");
            return;
        }

        planner.notes.push({
            region: planner.selectedRegion,
            text,
            createdAt: new Date().toISOString()
        });

        noteInput.value = "";
        renderNotes();
    });

    const originalNotes = renderNotes;

    window.VallesynPlanner = {
        selectRegion(name) {
            planner.selectedRegion = name;
            regionSelect.value = name;
        },

        addNote(note) {
            if (!note || !note.trim()) return;

            if (!planner.selectedRegion) return;

            planner.notes.push({
                region: planner.selectedRegion,
                text: note.trim(),
                createdAt: new Date().toISOString()
            });

            originalNotes();
        },

        getState() {
            return {
                selectedRegion: planner.selectedRegion,
                notes: [...planner.notes]
            };
        }
    };

    document.querySelectorAll(".nav-button").forEach(button => {
        button.addEventListener("click", () => {
            dashboard.hidden = button.dataset.page !== "planner";
        });
    });

    console.log("Vallesyn mission planner initialized.");
}
