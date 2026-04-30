// ==============================
// 🔐 CSRF TOKEN (GLOBAL)
// ==============================
function getCSRFToken() {
    let cookieValue = null;

    if (document.cookie) {
        document.cookie.split(';').forEach(c => {
            if (c.trim().startsWith('csrftoken=')) {
                cookieValue = c.trim().substring('csrftoken='.length);
            }
        });
    }

    return cookieValue;
}

// ==============================
// 🆔 GET PRODUCT ID (GLOBAL)
// ==============================
function getProductId() {
    const parts = window.location.pathname.split("/");
    return parts[parts.length - 2];
}

// ==============================
// 🛍️ LOAD PRODUCTS (HOME PAGE)
// ==============================
async function loadProducts() {

    const container = document.getElementById("product-container");
    if (!container) return;

    const res = await fetch("/api/products/");
    const products = await res.json();

    container.innerHTML = "";

    products.slice(0, 8).forEach(p => {

        container.innerHTML += `
        <div class="bg-white rounded-2xl p-3 shadow hover:shadow-lg transition">

            <a href="/product-detail/${p.id}/">
                <img src="${p.image}" class="rounded-xl h-48 w-full object-cover"/>
                <h3 class="mt-3 font-semibold">${p.name}</h3>
            </a>

            <p class="text-gray-500 text-sm">${p.category}</p>
            <p class="font-bold mt-1">₹${p.price}</p>

            <button onclick="addToCart(${p.id})"
            class="mt-2 w-full bg-black text-white py-2 rounded-full">
            Add to Cart
            </button>

        </div>
        `;
    });
}

// ==============================
// 📦 LOAD PRODUCT DETAIL
// ==============================
async function loadProductDetail() {

    const name = document.getElementById("product-name");
    if (!name) return;

    const id = getProductId();

    const res = await fetch(`/api/products/${id}/`);
    const p = await res.json();

    document.getElementById("product-name").innerText = p.name;
    document.getElementById("product-price").innerText = "₹" + p.price;
    document.getElementById("product-img").src = p.image || "/static/default.png";
    document.getElementById("product-desc").innerText = p.description || "";
    document.getElementById("product-category").innerText = p.category;
}

// ==============================
// ❤️ RELATED PRODUCTS
// ==============================
async function loadRelatedProducts() {

    const container = document.getElementById("related-products");
    if (!container) return;

    const res = await fetch("/api/products/");
    const data = await res.json();

    container.innerHTML = "";

    data.slice(0, 4).forEach(p => {

        container.innerHTML += `
        <div class="bg-white p-4 rounded-xl shadow hover:shadow-lg">

            <a href="/product-detail/${p.id}/">
                <img src="${p.image}" class="h-40 w-full object-cover rounded mb-2">
                <h3 class="font-semibold">${p.name}</h3>
            </a>

            <p class="text-gray-500">₹${p.price}</p>

            <button onclick="addToCart(${p.id})"
            class="mt-2 w-full bg-black text-white py-2 rounded-full">
            Add
            </button>

        </div>
        `;
    });
}

// ==============================
// 🛒 ADD TO CART (GLOBAL FIX)
// ==============================
async function addToCart(productId = null) {

    const id = productId || getProductId();

    const res = await fetch("/api/cart/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        credentials: "same-origin",
        body: JSON.stringify({
            product_id: id
        })
    });

    if (res.ok) {
        alert("✅ Added to cart");
    } else {
        alert("⚠️ Already in cart");
    }
}

// ==============================
// ⚡ BUY NOW
// ==============================
function buyNow() {
    window.location.href = "/checkout/";
}

// ==============================
// 🛒 LOAD CART
// ==============================
// ==============================
// 🛒 LOAD CART (PREMIUM UI)
// ==============================
async function loadCart() {

    const container = document.getElementById("cart-items");
    if (!container) return;

    const res = await fetch("/api/cart/");
    const cart = await res.json();

    container.innerHTML = "";
    let subtotal = 0;

    cart.forEach(item => {

        const price = item.product.price * item.quantity;
        subtotal += price;

        container.innerHTML += `
        <div class="cart-item">

            <img src="${item.product.image}" />

            <div class="flex-1">
                <h3 class="text-lg">${item.product.name}</h3>
                <p class="subtitle">${item.product.category}</p>

                <div class="qty-box mt-3">
                    <button class="qty-btn" onclick="updateQty(${item.id}, -1)">-</button>
                    <span class="qty-number">${item.quantity}</span>
                    <button class="qty-btn" onclick="updateQty(${item.id}, 1)">+</button>
                </div>

                <div class="mt-3">
                    <span onclick="removeItem(${item.id})" class="remove-btn">
                        Remove
                    </span>
                </div>
            </div>

            <div class="price">₹${price}</div>

        </div>
        `;
    });

    const tax = Math.floor(subtotal * 0.05);
    const total = subtotal + tax;

    document.getElementById("subtotal").innerText = "₹" + subtotal;
    document.getElementById("tax").innerText = "₹" + tax;
    document.getElementById("cart-total").innerText = total;
}

// ==============================
// 🚀 CHECKOUT
// ==============================
function goCheckout() {
    window.location.href = "/checkout/";
}


// ==============================
// 🔄 UPDATE QTY
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
            "X-CSRFToken": getCSRFToken()
        },
        credentials: "same-origin",
        body: JSON.stringify({
            quantity: newQty
        })
    });

    loadCart();
}


// ==============================
// ❌ REMOVE ITEM
// ==============================
async function removeItem(id) {

    await fetch(`/api/cart/${id}/`, {
        method: "DELETE",
        headers: {
            "X-CSRFToken": getCSRFToken()
        },
        credentials: "same-origin"
    });

    loadCart();
}


// ==============================
// 🚀 INIT (SMART AUTO LOAD)
// ==============================
window.addEventListener("DOMContentLoaded", () => {

    // HOME
    if (document.getElementById("product-container")) {
        loadProducts();
    }

    // PRODUCT DETAIL
    if (document.getElementById("product-name")) {
        loadProductDetail();
        loadRelatedProducts();
    }

    // CART
    if (document.getElementById("cart-items")) {
        loadCart();
    }

});

// ==============================
// 🎟️ PROMO TOGGLE
// ==============================
function togglePromo() {
    const box = document.getElementById("promo-box");
    box.classList.toggle("hidden");
}

// ==============================
// 🎟️ APPLY PROMO
// ==============================
function applyPromo() {

    const code = document.getElementById("promo-input").value;

    if (!code) {
        alert("Enter promo code");
        return;
    }

    // 🔥 DEMO LOGIC (you can connect backend later)
    if (code === "SAVE10") {

        let total = parseInt(document.getElementById("cart-total").innerText);
        let discount = Math.floor(total * 0.1);

        total = total - discount;

        document.getElementById("cart-total").innerText = total;

        alert("✅ Promo Applied (10% OFF)");

    } else {
        alert("❌ Invalid Code");
    }
}
// ==============================
// 💳 SELECT PAYMENT METHOD
// ==============================
function setPaymentMethod() {
    const radios = document.querySelectorAll('input[name="payment"]');
    const hidden = document.getElementById("payment-method");

    radios.forEach(r => {
        if (r.checked) {
            hidden.value = r.value;
        }
    });
}

// ==============================
// 🧾 LOAD CHECKOUT (UPDATED UI)
// ==============================
async function loadCheckout() {

    const container = document.getElementById("checkout-items");
    if (!container) return;

    const res = await fetch("/api/cart/");
    const cart = await res.json();

    let subtotal = 0;
    container.innerHTML = "";

    cart.forEach(item => {

        const price = item.product.price * item.quantity;
        subtotal += price;

        container.innerHTML += `
        <div class="flex items-center gap-4 mb-4">

            <img src="${item.product.image}"
                class="w-14 h-14 rounded-lg object-cover">

            <div class="flex-1">
                <p class="text-sm">${item.product.name}</p>
                <p class="text-xs text-gray-500">Qty: ${item.quantity}</p>
            </div>

            <div class="text-sm">₹${price}</div>

        </div>
        `;
    });

    const tax = Math.floor(subtotal * 0.05);
    const total = subtotal + tax;

    document.getElementById("checkout-subtotal").innerText = "₹" + subtotal;
    document.getElementById("checkout-tax").innerText = "₹" + tax;
    document.getElementById("checkout-total").innerText = "₹" + total;
}

// ==============================
// 🚀 INIT UPDATE
// ==============================
window.addEventListener("DOMContentLoaded", () => {

    if (document.getElementById("checkout-items")) {
        loadCheckout();
    }

    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", setPaymentMethod);
    }
});

// ==============================
// 💳 SELECT PAYMENT
// ==============================
function selectPayment(method, el) {

    document.querySelectorAll(".payment-box").forEach(box => {
        box.classList.remove("active");
    });

    el.classList.add("active");

    el.querySelector("input").checked = true;

    document.getElementById("payment-method").value = method;

    // hide all
    document.getElementById("upi-box").classList.add("hidden");
    document.getElementById("card-box").classList.add("hidden");

    // show selected
    if (method === "UPI") {
        document.getElementById("upi-box").classList.remove("hidden");
    }

    if (method === "CARD") {
        document.getElementById("card-box").classList.remove("hidden");
    }
}

let deliveryCharge = 0;

function selectDelivery(price, el) {

    document.querySelectorAll(".delivery-box").forEach(box => {
        box.classList.remove("active");
    });

    el.classList.add("active");

    deliveryCharge = price;

    document.getElementById("shipping-cost").innerText =
        price === 0 ? "FREE" : "₹" + price;

    updateTotal();
}

function selectPayment(method, el) {

    document.querySelectorAll(".payment-box").forEach(box => {
        box.classList.remove("active");
    });

    el.classList.add("active");
    el.querySelector("input").checked = true;

    document.getElementById("payment-method").value = method;

    document.getElementById("upi-box").classList.add("hidden");
    document.getElementById("card-box").classList.add("hidden");

    if (method === "UPI") {
        document.getElementById("upi-box").classList.remove("hidden");
    }

    if (method === "CARD") {
        document.getElementById("card-box").classList.remove("hidden");
    }
}

function updateTotal() {

    let subtotal = parseInt(document.getElementById("checkout-subtotal").innerText.replace("₹","")) || 0;
    let tax = parseInt(document.getElementById("checkout-tax").innerText.replace("₹","")) || 0;

    let total = subtotal + tax + deliveryCharge;

    document.getElementById("checkout-total").innerText = "₹" + total;
}

window.addEventListener("DOMContentLoaded", () => {

    if (document.getElementById("checkout-items")) {
        loadCheckout();
    }

    document.querySelector(".delivery-box")?.click();
    document.querySelector(".payment-box")?.click();
});

// CANCEL
async function cancelOrder(id) {
    await fetch(`/api/orders/cancel/${id}/`, {
        method: "POST",
        credentials: "include"
    });

    loadOrders();
}

// INIT
loadOrders();

async function loadOrders() {

    const container = document.getElementById("orders-container");
    if (!container) return;

    const res = await fetch("/api/orders/", {
        credentials: "include"
    });

    const orders = await res.json();

    if (!orders.length) {
        container.innerHTML = "<p>No orders yet 😔</p>";
        return;
    }

    container.innerHTML = "";

    orders.forEach(order => {

        const item = order.items[0];

       
const img = item.product_image 
    ? item.product_image 
    : "https://via.placeholder.com/100";
        let statusColor = "bg-gray-200 text-gray-700";

        if (order.status === "Delivered") {
            statusColor = "bg-green-100 text-green-700";
        } else if (order.status === "Shipped") {
            statusColor = "bg-yellow-100 text-yellow-700";
        } else if (order.status === "Processing") {
            statusColor = "bg-pink-100 text-pink-700";
        }

        container.innerHTML += `
        <div class="bg-white rounded-[40px] p-8 flex justify-between items-center shadow-sm">

            <div class="flex items-center gap-6">

                <img src="${img}" class="w-24 h-24 rounded-2xl object-cover">

                <div>
                    <p class="text-xs text-gray-400 tracking-widest">ORDER REFERENCE</p>
                    <p class="text-lg font-semibold">#VR-${order.id}</p>

                    <p class="text-sm text-gray-500 mt-1">
                        Total Amount 
                        <span class="text-[#7a5c00] font-semibold">
                        ₹${order.total_price}
                        </span>
                    </p>

                    <div class="flex gap-6 mt-4 items-center">

                        <a href="/order-detail/${order.id}/"
                        class="text-sm underline">
                        VIEW DETAILS
                        </a>

                        <a href="/order-tracking/${order.id}/"
                        class="px-6 py-2 rounded-full text-white text-xs"
                        style="background:linear-gradient(135deg,#7a5c00,#c8a646)">
                        TRACK ORDER
                        </a>

                        ${order.status === "Pending" ? `
                        <button onclick="cancelOrder(${order.id})"
                        class="text-red-500 text-sm">
                        Cancel Order
                        </button>
                        ` : ""}

                    </div>
                </div>

            </div>

            <div class="text-right">
                <span class="px-4 py-1 rounded-full text-xs ${statusColor}">
                    ${order.status}
                </span>

                <p class="text-xs text-gray-400 mt-2">
                    ${new Date(order.created_at).toDateString()}
                </p>
            </div>

        </div>
        `;
    });
}

async function loadRecommended() {

    const container = document.getElementById("recommended");
    if (!container) return;

    const res = await fetch("/api/products/");
    const products = await res.json();

    container.innerHTML = "";

    products.slice(0,3).forEach(p => {

        container.innerHTML += `
        <div>
            <img src="${p.image}" 
            class="rounded-3xl h-72 w-full object-cover mb-4">

            <p class="text-xs text-gray-400 uppercase">New Arrival</p>
            <h3 class="font-semibold">${p.name}</h3>
            <p class="text-[#7a5c00] mt-1">₹${p.price}</p>
        </div>
        `;
    });
}

// ==============================
// 📦 LOAD ORDER DETAIL (FIXED)
// ==============================
async function loadOrderDetail() {

    const path = window.location.pathname.split("/");
    const orderId = path[path.length - 2];

    const res = await fetch(`/api/orders/${orderId}/`);
    const order = await res.json();

    document.getElementById("order-date").innerText =
        "Placed on " + new Date(order.created_at).toLocaleString();

    document.getElementById("order-address").innerText = order.address;
    document.getElementById("order-payment").innerText = order.payment_method;

    document.getElementById("order-total").innerText = "₹" + order.total_price;
    document.getElementById("order-total-final").innerText = "₹" + order.total_price;

    const container = document.getElementById("order-items");
    container.innerHTML = "";

    order.items.forEach(item => {

       
const img = item.product_image 
    ? item.product_image 
    : "https://via.placeholder.com/100";

        container.innerHTML += `
        <div class="bg-white rounded-[30px] p-6 flex items-center gap-6 shadow-sm">

            <img src="${img}" class="w-24 h-28 object-cover rounded-xl">

            <div class="flex-1">
                <h3 class="text-lg font-semibold">${item.product_name}</h3>

                <p class="text-sm text-gray-400 mt-1">
                    Quantity: ${item.quantity}
                </p>

                <a href="/product-detail/${item.product_id}/"
                class="text-xs underline mt-3 inline-block">
                VIEW PRODUCT
                </a>
            </div>

            <div class="font-semibold">
                ₹${item.price}
            </div>

        </div>
        `;
    });
}
// ==============================
// 🚀 INIT ORDER DETAIL
// ==============================
window.addEventListener("DOMContentLoaded", () => {

    if (window.location.pathname.includes("order-detail")) {
        loadOrderDetail();
    }

});

// ==============================
// 🎯 GET ORDER ID
// ==============================
function getOrderId() {
    const parts = window.location.pathname.split("/");
    return parts[parts.length - 2];
}

// ==============================
// 🚚 TRACK ORDER
// ==============================
function trackOrder() {
    const id = getOrderId();
    window.location.href = `/order-tracking/${id}/`;
}

// ==============================
// 🚚 TRACK DELIVERY
// ==============================
function trackDelivery() {
    const id = getOrderId();
    window.location.href = `/order-tracking/${id}/`;
}

// ==============================
// ❌ CANCEL ORDER (API CONNECTED)
// ==============================
async function cancelOrderDetail() {

    const id = getOrderId();

    if (!confirm("Are you sure you want to cancel this order?")) return;

    const res = await fetch(`/api/orders/cancel/${id}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken()
        },
        credentials: "include"
    });

    if (res.ok) {
        alert("✅ Order Cancelled");
        location.reload();
    } else {
        alert("❌ Failed to cancel order");
    }
}

// ==============================
// 🔄 RETURN ORDER (UI ONLY)
// ==============================
function returnOrder() {
    alert("🔁 Return request submitted");
}

// ==============================
// 🧾 DOWNLOAD INVOICE
// ==============================
function downloadInvoice() {

    const id = getOrderId();

    // Simple invoice PDF (demo)
    const content = `
        Order ID: ${id}
        Thank you for your purchase!
    `;

    const blob = new Blob([content], { type: "text/plain" });
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "invoice.txt";
    a.click();
}

let actionType = ""; // cancel या return

// ==============================
// 🎯 OPEN MODAL
// ==============================
function openReasonModal(type) {
    actionType = type;

    document.getElementById("reasonModal").classList.remove("hidden");
    document.getElementById("reasonModal").classList.add("flex");
}

// ==============================
// ❌ CLOSE MODAL
// ==============================
function closeModal() {
    document.getElementById("reasonModal").classList.add("hidden");
}

// ==============================
// 👀 SHOW TEXTAREA IF OTHER
// ==============================
document.addEventListener("change", function(e) {
    if (e.target.name === "reason") {
        if (e.target.value === "Other") {
            document.getElementById("otherReason").classList.remove("hidden");
        } else {
            document.getElementById("otherReason").classList.add("hidden");
        }
    }
});

// ==============================
// 🚀 SUBMIT REASON
// ==============================
async function submitReason() {

    const id = getOrderId();

    let selected = document.querySelector('input[name="reason"]:checked');

    if (!selected) {
        alert("Please select a reason");
        return;
    }

    let reason = selected.value;

    if (reason === "Other") {
        reason = document.getElementById("otherReason").value;
    }

    if (!reason) {
        alert("Please enter reason");
        return;
    }

    let url = "";

    if (actionType === "cancel") {
        url = `/api/orders/cancel/${id}/`;
    }

    if (actionType === "return") {
        url = `/api/orders/return/${id}/`; // (you will add later)
    }

    const res = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        credentials: "include",
        body: JSON.stringify({ reason: reason })
    });

    if (res.ok) {
        alert("✅ Success");
        closeModal();
        location.reload();
    } else {
        alert("❌ Failed");
    }
}

const orderId = window.location.pathname.split("/")[2];

async function loadTracking() {

    const res = await fetch(`/api/orders/${orderId}/`);
    const data = await res.json();

    document.getElementById("order-id").innerText = data.id;
    document.getElementById("order-date").innerText =
        new Date(data.created_at).toDateString();

    // ETA fake
    document.getElementById("eta").innerText = "12 mins";

    // ======================
    // STATUS LOGIC
    // ======================
    let progress = 20;

    if (data.status === "processing") progress = 40;
    if (data.status === "shipped") progress = 70;
    if (data.status === "delivered") progress = 100;

    document.getElementById("progress-bar").style.width = progress + "%";

    // ======================
    // TIMELINE
    // ======================
    const steps = [
        "Order Placed",
        "Packed",
        "Shipped",
        "Out for Delivery",
        "Delivered"
    ];

    let currentIndex = 0;

    if (data.status === "pending") currentIndex = 0;
    if (data.status === "processing") currentIndex = 1;
    if (data.status === "shipped") currentIndex = 2;
    if (data.status === "delivered") currentIndex = 4;

    let timelineHTML = "";

    steps.forEach((step, index) => {

        const active = index <= currentIndex;

        timelineHTML += `
        <div class="flex items-center gap-4">

            <div class="w-6 h-6 rounded-full flex items-center justify-center
            ${active ? "bg-[#7a5c00] text-white" : "bg-gray-200"}">
                ${active ? "✓" : ""}
            </div>

            <div>
                <p class="${active ? "text-black" : "text-gray-400"}">${step}</p>
            </div>

        </div>
        `;
    });

    document.getElementById("timeline").innerHTML = timelineHTML;

    // ======================
    // PRODUCT
    // ======================
    const item = data.items[0];

    
const img = item.product_image 
    ? item.product_image 
    : "https://via.placeholder.com/100";

    document.getElementById("product-box").innerHTML = `
        <div class="flex gap-4 items-center">

            <img src="${img}" class="w-16 h-16 rounded-xl object-cover">

            <div class="flex-1">
                <p class="font-semibold">${item.product_name}</p>
                <p class="text-sm text-gray-400">Qty: ${item.quantity}</p>
            </div>

            <div class="font-semibold">
                ₹${item.price}
            </div>

        </div>
    `;
}

window.addEventListener("DOMContentLoaded", loadTracking);

async function placeOrder() {

    const address = document.querySelector("input[name='address']")?.value;
    const payment = document.getElementById("payment-method")?.value;

    if (!address || address.trim() === "") {
        alert("❌ Enter address");
        return;
    }

    if (!payment) {
        alert("❌ Select payment method");
        return;
    }

const res = await fetch("/api/orders/place/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken()
    },
    credentials: "include",   // ✅ MUST
    body: JSON.stringify({
        address: address,
        payment_method: payment
    })
});

    const data = await res.json();

    if (!res.ok) {
        alert(data.error || "Order failed");
        return;
    }

    alert("✅ Order placed successfully");
    window.location.href = "/orders/";
}
