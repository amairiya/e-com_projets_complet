let products = [];
let cart = JSON.parse(localStorage.getItem("cart")) || [];

/* =====================
   CHARGEMENT PRODUITS
===================== */

fetch("/api/products")
.then(res => res.json())
.then(data => {
    products = data;
    renderProducts();
    renderCart();
    updateCartCount();
});

/* =====================
   AFFICHAGE PRODUITS
===================== */

function renderProducts() {
    const container = document.getElementById("products");
    container.innerHTML = "";

    products.forEach((p, index) => {
        const images = p.images ? p.images.split("|").map(i => i.trim()) : [];
        const isPromo = p.promo === "yes";
        const price = isPromo ? p.promo_price : p.price;
        const inStock = p.stock > 0;
        const stockText = inStock ? `En stock (${p.stock})` : "Rupture de stock";
        const stockClass = inStock ? "stock-in" : "stock-out";
        const disabled = inStock ? "" : "disabled";

        let carouselItems = "";
        images.forEach((img, i) => {
            carouselItems += `
            <div class="carousel-item ${i === 0 ? "active" : ""}">
                ${p.promo === "yes" || p.promo_price < p.price
                    ? `<span class="badge bg-danger promo-badge">Promo</span>`
                    : ""}
                <img src="${img}" class="d-block w-100 rounded">
            </div>`;
        });

        container.innerHTML += `
        <div class="col-md-4">
            <div class="card mb-4 shadow position-relative">
                ${isPromo ? `<span class="badge bg-danger promo-badge">-${p.discount || 0}%</span>` : ""}

                ${images.length ? `
                <div id="carousel${index}" class="carousel slide" data-bs-ride="carousel">
                    <div class="carousel-inner">${carouselItems}</div>
                    <button class="carousel-control-prev" type="button" data-bs-target="#carousel${index}" data-bs-slide="prev">
                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    </button>
                    <button class="carousel-control-next" type="button" data-bs-target="#carousel${index}" data-bs-slide="next">
                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    </button>
                </div>` : ""}

                <div class="card-body">
                    <h5>${p.name}</h5>
                    <p>${p.description || ""}</p>
                    <p class="${stockClass}"><strong>${stockText}</strong></p>
                    ${isPromo ? `<p><span class="old-price">${p.price} €</span> <strong class="text-success">${p.promo_price} €</strong></p>` 
                    : `<p><strong>${p.price} €</strong></p>`}

                    <input type="number" min="1" value="1" id="qty-${index}" class="form-control mb-2" placeholder="Quantité" ${disabled}>
                    <button class="btn btn-cart w-100" onclick="addToCart(${index})">Ajouter au panier</button>
                </div>
            </div>
        </div>`;
    });
}



// // Commander
// function order() {
//     if (!cart.length) {
//         alert("Panier vide");
//         return;
//     }

//     const customer = {
//         name: document.getElementById("name").value,
//         email: document.getElementById("email").value,
//         phone: document.getElementById("phone").value,
//         address: document.getElementById("address").value
//     };

//     if (!customer.name || !customer.phone) {
//         alert("Nom et téléphone obligatoires");
//         return;
//     }

//     fetch("/api/order", {
//         method: "POST",
//         headers: {"Content-Type": "application/json"},
//         body: JSON.stringify({
//             customer: customer,
//             items: cart
//         })
//     }).then(res => {
//         if(res.ok){
//             alert("✅ Commande enregistrée !");
            
//             // Mettre à jour le stock local
//             cart.forEach(item => {
//                 const prod = products.find(p => p.name === item.product);
//                 if (prod) {
//                     prod.stock -= item.quantity;
//                     if (prod.stock < 0) prod.stock = 0;
//                 }
//             });

//             cart = [];
//             total = 0;
//             renderCart();
//             renderProducts(); // Re-render pour mettre à jour le stock affiché

//             document.getElementById("name").value = "";
//             document.getElementById("email").value = "";
//             document.getElementById("phone").value = "";
//             document.getElementById("address").value = "";
//         } else {
//             alert("Erreur lors de la commande.");
//         }
//     });
// }


// Commander
function order() {
    if (!cart.length) {
        alert("Panier vide");
        return;
    }

    const customer = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        phone: document.getElementById("phone").value,
        address: document.getElementById("address").value
    };

    if (!customer.name || !customer.phone) {
        alert("Nom et téléphone obligatoires");
        return;
    }

    fetch("/api/order", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            customer: customer,
            items: cart
        })
    })
    .then(res => res.json())
    .then(data => {
        if(data.status === "ok"){
            // Affiche un popup avec le numéro de commande
            const orderNumber = data.order_number || "N/A";
            alert(`✅ Commande enregistrée !\nNuméro de commande : ${orderNumber}`);

            // Mettre à jour le stock local
            cart.forEach(item => {
                const prod = products.find(p => p.name === item.product);
                if (prod) {
                    prod.stock -= item.quantity;
                    if (prod.stock < 0) prod.stock = 0;
                }
            });

            cart = [];
            total = 0;
            renderCart();
            renderProducts(); // Re-render pour mettre à jour le stock affiché

            document.getElementById("name").value = "";
            document.getElementById("email").value = "";
            document.getElementById("phone").value = "";
            document.getElementById("address").value = "";
        } else {
            alert("Erreur lors de la commande.");
        }
    })
    .catch(err => alert("Erreur : " + err));
}


/* =====================
   AJOUT AU PANIER ✅
===================== */

function addToCart(index) {
    const product = products[index];
    const qty = parseInt(document.getElementById(`qty-${index}`).value) || 1;

    if (qty > product.stock) {
        alert(`Stock maximum : ${product.stock}`);
        return;
    }

    const existing = cart.find(p => p.id === product.id);

    if (existing) {
        existing.quantity += qty;
    } else {
        cart.push({
            id: product.id,
            name: product.name,
            price: product.promo === "yes" ? product.promo_price : product.price,
            quantity: qty
        });
    }

    saveCart();
}

/* =====================
   PANIER
===================== */

function renderCart() {
    const el = document.getElementById("cart");
    let total = 0;
    el.innerHTML = "";

    cart.forEach((item, i) => {
        total += item.price * item.quantity;
        el.innerHTML += `
        <li class="list-group-item d-flex justify-content-between align-items-center">
            ${item.name} x ${item.quantity}
            <span>${(item.price * item.quantity).toFixed(2)} €</span>
            <button class="btn btn-sm btn-danger"
                onclick="removeFromCart(${i})">X</button>
        </li>`;
    });

    document.getElementById("total").innerText = total.toFixed(2);
}

/* =====================
   SUPPRESSION
===================== */

function removeFromCart(index) {
    cart.splice(index, 1);
    saveCart();
}

/* =====================
   LOCAL STORAGE
===================== */

function saveCart() {
    localStorage.setItem("cart", JSON.stringify(cart));
    renderCart();
    updateCartCount();
}

function updateCartCount() {
    const count = cart.reduce((sum, i) => sum + i.quantity, 0);
    document.getElementById("cart-count").innerText = count;
}


fetch('footer.html')
    .then(response => response.text())
    .then(data => {
        document.getElementById('footer-container').innerHTML = data;
    })
    .catch(err => console.error('Erreur lors du chargement du footer :', err));
