// ==============================
// SELECT FREQUENCY
// ==============================
function selectFreq(el) {

    document.querySelectorAll(".freq-btn").forEach(btn => {
        btn.classList.remove("bg-[#efe6d3]");
        btn.classList.add("bg-gray-100");
    });

    el.classList.remove("bg-gray-100");
    el.classList.add("bg-[#efe6d3]");
}

// ==============================
// SAVE (DEMO)
// ==============================
function savePreferences() {
    alert("✅ Preferences Saved (demo)");
}
// TOGGLE SWITCH
function toggle(el) {
    el.classList.toggle("active");
}

// FREQUENCY
function selectFreq(el) {

    document.querySelectorAll(".freq").forEach(btn => {
        btn.classList.remove("active");
    });

    el.classList.add("active");
}

// SAVE
function savePreferences() {
    alert("✅ Preferences Saved");
}