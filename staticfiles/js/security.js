// TOGGLE 2FA
function toggle(el) {
    el.classList.toggle("active");
}

// UPDATE PASSWORD
function updatePassword() {

    const newPass = document.getElementById("new-password").value;
    const confirmPass = document.getElementById("confirm-password").value;

    if (newPass !== confirmPass) {
        alert("❌ Passwords do not match");
        return;
    }

    alert("✅ Password Updated (demo)");
}

// LOGOUT ALL
function logoutAll() {
    alert("🔒 Logged out from all devices (demo)");
}