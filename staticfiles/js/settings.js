// ==============================
// CSRF
// ==============================
function getCSRFToken() {
    let cookieValue = null;
    document.cookie.split(';').forEach(c => {
        if (c.trim().startsWith('csrftoken=')) {
            cookieValue = c.trim().substring('csrftoken='.length);
        }
    });
    return cookieValue;
}

// ==============================
// LOAD PROFILE
// ==============================
async function loadProfile() {

    const res = await fetch("/api/users/profile/", {
        credentials: "include"
    });

    const data = await res.json();

    document.getElementById("username").value = data.username || "";
    document.getElementById("email").value = data.email || "";
    document.getElementById("email-display").innerText = data.email || "";
}

// ==============================
// SAVE PROFILE
// ==============================
async function saveProfile() {

    const res = await fetch("/api/users/profile/update/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        credentials: "include",
        body: JSON.stringify({
            username: document.getElementById("username").value,
            email: document.getElementById("email").value
        })
    });

    if (res.ok) {
        alert("✅ Profile Updated");
    } else {
        alert("❌ Error updating profile");
    }
}

// ==============================
// BUTTON ACTIONS
// ==============================
function changePassword() {
    window.location.href = "/reset-password/";
}

function deleteAccount() {
    if (confirm("Are you sure?")) {
        alert("Delete feature coming soon");
    }
}

// INIT
window.onload = loadProfile;