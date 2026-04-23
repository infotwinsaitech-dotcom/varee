// TOGGLE
function toggle(el) {
    el.classList.toggle("active");
}

// UNIT SELECT
function selectUnit(el) {

    document.querySelectorAll(".unit").forEach(btn => {
        btn.classList.remove("active");
    });

    el.classList.add("active");
}