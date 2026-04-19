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

    document.getElementById("name").innerText = data.username;
    document.getElementById("sidebar-name").innerText = data.username;

    document.getElementById("edit-name").value = data.username;
    document.getElementById("edit-email").value = data.email;

    // ✅ IMAGE FIX (MAIN ISSUE)
    if (data.profile_image) {

        let img = data.profile_image;

        // force reload (cache fix)
        img += "?t=" + new Date().getTime();

        document.getElementById("profile-image").src = img;
        document.getElementById("profile-image-big").src = img;

    } else {
        document.getElementById("profile-image").src = "https://i.pravatar.cc/100";
        document.getElementById("profile-image-big").src = "https://i.pravatar.cc/120";
    }
}
// ==============================
// SAVE PROFILE
// ==============================
async function saveProfile() {

    const formData = new FormData();

    formData.append("username", document.getElementById("edit-name").value);
    formData.append("email", document.getElementById("edit-email").value);

    const file = document.getElementById("edit-image").files[0];
    if (file) {
        formData.append("image", file);
    }

    const res = await fetch("/api/users/profile/update/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken()
        },
        credentials: "include",
        body: formData
    });

    const data = await res.json();

    if (res.ok) {

        document.getElementById("name").innerText = data.username;
        document.getElementById("sidebar-name").innerText = data.username;

        // ✅ IMAGE UPDATE
        if (data.profile_image) {
            const img = data.profile_image + "?t=" + new Date().getTime();

            document.getElementById("profile-image").src = img;
            document.getElementById("profile-image-big").src = img;
        }

        alert("✅ Updated");
        document.getElementById("editBox").classList.add("hidden");

    } else {
        alert("❌ Failed");
    }
}

// ==============================
// UI
// ==============================
function toggleEdit() {
    document.getElementById("editBox").classList.toggle("hidden");
}

// INIT
window.onload = loadProfile;