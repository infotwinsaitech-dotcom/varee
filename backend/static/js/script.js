// ==============================
// 🔐 CSRF TOKEN
// ==============================
function getCSRFToken() {
    let cookieValue = null;
    const cookies = document.cookie.split(';');

    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith('csrftoken=')) {
            cookieValue = cookie.substring('csrftoken='.length);
            break;
        }
    }
    return cookieValue;
}

// ==============================
// 🛍️ LOAD PRODUCTS
// ==============================
// 🛒 LOAD CART
async function loadCart() {
    const container = document.getElementById("cart-items");
    if (!container) return;

    const res = await fetch("/api/cart/");
    const cart = await res.json();

    container.innerHTML = "";
    let total = 0;

    cart.forEach(item => {
        const price = item.product.price * item.quantity;
        total += price;

        container.innerHTML += `
        <div class="flex gap-4 border-b py-4">

            <img src="${item.product.image}" class="w-20 h-20"/>

            <div class="flex-1">
                <h3>${item.product.name}</h3>
                <p>${item.product.category}</p>
                <p>₹${item.product.price}</p>

                <div class="flex gap-2 mt-2 items-center">
                    <button onclick="updateQty(${item.id}, -1)">-</button>
                    <span>${item.quantity}</span>
                    <button onclick="updateQty(${item.id}, 1)">+</button>

                    <span onclick="removeItem(${item.id})"
                        class="text-red-500 cursor-pointer ml-3">
                        Remove
                    </span>
                </div>
            </div>

            <div>₹${price}</div>
        </div>
        `;
    });

    document.getElementById("cart-total").innerText = total;
}

// 🔄 UPDATE QTY
async function updateQty(id, change) {
    const res = await fetch(`/api/cart/${id}/`);
    const item = await res.json();

    const newQty = item.quantity + change;

    if (newQty < 1) return;

    await fetch(`/api/cart/${id}/`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ quantity: newQty })
    });

    loadCart();
}

// ❌ REMOVE ITEM
async function removeItem(id) {
    await fetch(`/api/cart/${id}/`, {
        method: "DELETE"
    });

    loadCart();
}

// ==============================
// UPDATE QTY
// ==============================
async function updateQty(id, change) {
    const res = await fetch(`/api/cart/${id}/`);
    const item = await res.json();

    const newQty = item.quantity + change;
    if (newQty < 1) return;

    await fetch(`/api/cart/${id}/`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ quantity: newQty })
    });

    loadCart();
}


// ==============================
// REMOVE ITEM
// ==============================
async function removeItem(id) {
    await fetch(`/api/cart/${id}/`, {
        method: "DELETE"
    });

    loadCart();
}



// ==============================
// 🔗 NAVIGATION
// ==============================
function goToProduct(id) {
    window.location.href = `/product/?id=${id}`;
}

// ==============================
// 🚀 INIT
// ==============================
window.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("product-container")) loadProducts();
    if (document.getElementById("cart-items")) loadCart();
});