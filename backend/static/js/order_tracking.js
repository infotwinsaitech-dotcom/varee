function getOrderId() {
    const parts = window.location.pathname.split("/");
    return parts[parts.length - 2];
}

async function loadTracking() {

    const id = getOrderId();

    const res = await fetch(`/api/orders/${id}/`);
    const data = await res.json();

    // =========================
    // BASIC INFO
    // =========================
    document.getElementById("order-id").innerText = data.id;

    document.getElementById("order-date").innerText =
        new Date(data.created_at).toDateString();

    // =========================
    // STEP LOGIC (MAIN FIX)
    // =========================
    let current = 0;

    if (data.status === "pending") current = 0;
    else if (data.status === "processing") current = 1;
    else if (data.status === "shipped") current = 2;
    else if (data.status === "out_for_delivery") current = 3;
    else if (data.status === "delivered") current = 4;

    // =========================
    // STEP UI UPDATE
    // =========================
    for (let i = 0; i <= 4; i++) {

        const step = document.getElementById(`step-${i}`);

        if (!step) continue;

        if (i < current) {
            step.className =
                "w-12 h-12 mx-auto rounded-full flex items-center justify-center bg-[#7a5c00] text-white";
        }

        else if (i === current) {
            step.className =
                "w-12 h-12 mx-auto rounded-full flex items-center justify-center bg-[#5c3d2e] text-white";
        }

        else {
            step.className =
                "w-12 h-12 mx-auto rounded-full flex items-center justify-center bg-gray-200";
        }
    }

    // =========================
    // PRODUCT (OPTIONAL)
    // =========================
    const item = data.items[0];

    if (item && document.getElementById("product-box")) {

        const img = item.product_image
            ? "http://127.0.0.1:8000" + item.product_image
            : "";

        document.getElementById("product-box").innerHTML = `
            <div class="flex items-center gap-4">
                <img src="${img}" class="w-16 h-16 rounded-xl object-cover">

                <div>
                    <p class="font-semibold">${item.product_name}</p>
                    <p class="text-sm text-gray-400">
                        Qty: ${item.quantity}
                    </p>
                    <p class="text-[#7a5c00] font-semibold">
                        ₹${item.price}
                    </p>
                </div>
            </div>
        `;
    }
}

// =========================
// INIT
// =========================
window.addEventListener("DOMContentLoaded", loadTracking);


function viewReceipt() {
    const id = window.location.pathname.split("/")[2];
    window.location.href = `/order-detail/${id}/`;
}
function downloadInvoice() {

    const id = window.location.pathname.split("/")[2];

    const content = `
        VAREE ORDER RECEIPT
        ------------------------
        Order ID: ${id}

        Thank you for shopping with Varee ❤️
    `;

    const blob = new Blob([content], { type: "text/plain" });
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = `invoice_${id}.txt`;   // 👈 file name
    a.click();
}

