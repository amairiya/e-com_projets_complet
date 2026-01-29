let products = [];
let orders = [];
let token = localStorage.getItem("admin_token");

/* =======================
   AUTH & HEADERS
======================= */

function authHeaders() {
    return {
        // "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    };
}

function isLoggedIn() {
    return !!token;
}

/* =======================
   LOGIN
======================= */

function login() {
    const user = document.getElementById("user").value;
    const password = document.getElementById("password").value;
    const primary_key = document.getElementById("primary_key").value;
    const secondary_key = document.getElementById("secondary_key").value;
    fetch("/api/admin/login", {   // ⚠ ici /api/admin/login
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user, password , primary_key ,secondary_key})
    })
    .then(res => res.json())
    .then(data => {
        if (data.token) {
            token = data.token;
            localStorage.setItem("admin_token", token);
            showPanel();
        } else {
            alert("Identifiants incorrects");
        }
    })
    .catch(() => alert("Erreur login"));
}

function logout() {
    localStorage.removeItem("admin_token");
    token = null;
    document.getElementById("panel").style.display = "none";
    document.getElementById("login").style.display = "block";
}

/* =======================
   INIT UI
======================= */

function showPanel() {
    document.getElementById("login").style.display = "none";
    document.getElementById("panel").style.display = "block";
    loadProducts();
    loadOrders();
}

if (isLoggedIn()) {
    showPanel();
}

/* =======================
   PRODUITS
======================= */

function loadProducts() {
    fetch("/api/admin/products", {
        headers: authHeaders()
    })
    .then(res => {
        if (res.status === 401) throw new Error("Unauthorized");
        return res.json();
    })
    .then(data => {
        products = data;
        renderProducts();
    })
    .catch(() => logout());
}

function renderProducts() {
    const table = document.getElementById("products");
    table.innerHTML = `
    <tr>
        <th>ID</th><th>Nom</th><th>Prix</th><th>Promo</th>
        <th>Description</th><th>Images</th><th>Stock</th><th>❌</th>
    </tr>`;

    products.forEach((p, i) => {
        table.innerHTML += `
        <tr>
            <td>${p.id}</td>
            <td><input value="${p.name}" class="form-control"
                onchange="products[${i}].name=this.value"></td>
            <td><input type="number" value="${p.price}" class="form-control"
                onchange="products[${i}].price=this.value"></td>
            <td><input type="number" value="${p.promo_price}" class="form-control"
                onchange="products[${i}].promo_price=this.value"></td>
            <td><input value="${p.description}" class="form-control"
                onchange="products[${i}].description=this.value"></td>
            <td><input value="${p.images}" class="form-control"
                onchange="products[${i}].images=this.value"></td>
            <td><input type="number" value="${p.stock}" class="form-control"
                onchange="products[${i}].stock=this.value"></td>
            <td><button class="btn btn-danger btn-sm" onclick="deleteProduct(${i})">X</button></td>
        </tr>`;
    });
}

function addProduct() {
    const id = document.getElementById("new_id").value;
    const name = document.getElementById("new_name").value;
    const price = parseFloat(document.getElementById("new_price").value);
    const promo_price = parseFloat(document.getElementById("new_promo_price").value) || price;
    const promo = document.getElementById("new_promo").value;
    const description = document.getElementById("new_description").value;
    const images = document.getElementById("new_images").value;
    const stock = parseInt(document.getElementById("new_stock").value) || 0;

    products.push({id, name, price, promo_price, promo, description, images, stock});
    renderProducts();

    document.getElementById("new_id").value = "";
    document.getElementById("new_name").value = "";
    document.getElementById("new_price").value = "";
    document.getElementById("new_promo_price").value = "";
    document.getElementById("new_promo").value = "";
    document.getElementById("new_description").value = "";
    document.getElementById("new_images").value = "";
    document.getElementById("new_stock").value = "";
}

function deleteProduct(index) {
    const productId = products[index].id;
    if (confirm("Voulez-vous vraiment supprimer ce produit ?")) {
        fetch(`/api/admin/products/${productId}`, {
            method: "DELETE",
            headers: authHeaders()
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "ok") {
                products.splice(index, 1); // supprime du tableau local
                renderProducts();           // rafraîchit l'affichage
                alert("Produit supprimé !");
            } else {
                alert("Erreur : " + (data.message || "Impossible de supprimer"));
            }
        })
        .catch(err => alert("Erreur réseau : " + err));
    }
}

function saveProducts() {
    // récupérer les valeurs du formulaire
    const id = document.getElementById("new_id").value;
    const name = document.getElementById("new_name").value;
    const price = parseFloat(document.getElementById("new_price").value);
    const promo_price = parseFloat(document.getElementById("new_promo_price").value) || price;
    const promo = document.getElementById("new_promo").value;
    const description = document.getElementById("new_description").value;
    const images = document.getElementById("new_images").value;
    const stock = parseInt(document.getElementById("new_stock").value) || 0;

    const newProduct = { id, name, price, promo_price, promo, description, images, stock };

    fetch("/api/admin/products", {
        method: "POST",  // POST pour ajouter
        headers: authHeaders(),
        body: JSON.stringify(newProduct)  // envoyer juste le produit
    })
    .then(res => res.json())
    .then(data => {
        if(data.status === "ok"){
            alert("Produit ajouté !");
            loadProducts(); // rafraîchit la liste
        } else {
            alert("Erreur : " + (data.message || "Impossible d'ajouter le produit"));
        }
    })
    .catch(err => alert("Erreur : " + err));
}

/* =======================
   COMMANDES
======================= */

function loadOrders() {
    fetch("/api/admin/orders", {
        headers: authHeaders()
    })
    .then(res => {
        if (res.status === 401) throw new Error("Unauthorized");
        return res.json();
    })
    .then(data => {
        orders = data;
        renderOrders();
    })
    .catch(() => logout());
}

// function renderOrders() {
//     const table = document.getElementById("orders");
//     table.innerHTML = `
//     <tr>
//         <th>Date</th><th>Client</th><th>Produit</th>
//         <th>Qté</th><th>Prix</th>
//         <th>Livré</th><th>Retourné</th><th>Fermé</th>
//     </tr>`;

//     orders.forEach((o, i) => {
//         table.innerHTML += `
//         <tr>
//             <td>${o.date}</td>
//             <td>${o.name}</td>
//             <td>${o.product}</td>
//             <td>${o.quantity}</td>
//             <td>${o.price}</td>
//             <td>${selectStatus(i, "livré", o.livré)}</td>
//             <td>${selectStatus(i, "retourné", o.retourné)}</td>
//             <td>${selectStatus(i, "fermé", o.fermé)}</td>
//         </tr>`;
//     });
// }

function renderOrders() {
    const table = document.getElementById("orders");
    table.innerHTML = `
    <tr>
        <th>Numéro</th>
        <th>Date</th>
        <th>Client</th>
        <th>Produit</th>
        <th>Qté</th>
        <th>Prix</th>
        <th>Livré</th>
        <th>Retourné</th>
        <th>Fermé</th>
    </tr>`;

    orders.forEach((o, i) => {
        table.innerHTML += `
        <tr>
            <td>${o.order_number || "-"}</td>
            <td>${new Date(o.date).toLocaleString()}</td>
            <td>${o.name}</td>
            <td>${o.product}</td>
            <td>${o.quantity}</td>
            <td>${parseFloat(o.price).toFixed(2)} €</td>
            <td>${selectStatus(i, "livré", o.livré)}</td>
            <td>${selectStatus(i, "retourné", o.retourné)}</td>
            <td>${selectStatus(i, "fermé", o.fermé)}</td>
        </tr>`;
    });
}

function selectStatus(index, field, value) {
    return `
    <select onchange="updateOrder(${index}, '${field}', this.value)">
        <option value="Non" ${value === "Non" ? "selected" : ""}>Non</option>
        <option value="Oui" ${value === "Oui" ? "selected" : ""}>Oui</option>
    </select>`;
}

// function updateOrder(index, field, value) {
//     fetch("/api/admin/order/update", {
//         method: "PATCH",
//         headers: authHeaders(),
//         body: JSON.stringify({ index, field, value })
//     })
//     .then(res => res.json())
//     .then(() => loadOrders())
//     .catch(() => alert("Erreur mise à jour"));
// }









        // -------------------------------
        // Télécharger CSV downloadProductsCSV
        // -------------------------------
        async function downloadProductsCSV() {
            try {
                const response = await fetch(`/api/admin/export/products`,{headers: authHeaders()});
                if (!response.ok) throw new Error("Erreur téléchargement CSV");

                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `products.csv`;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
            } catch (err) {
                alert(err);
            }
        }


        const downloadBtnOrders = document.getElementById("downloadBtnOrders");
        async function downloadOrdersCSV() {
            try {
                const response = await fetch(`/api/admin/export/orders`,{headers: authHeaders()});
                if (!response.ok) throw new Error("Erreur téléchargement CSV");

                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `orders.csv`;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
            } catch (err) {
                alert(err);
            }
        }




        



const downloadBtn = document.getElementById("downloadBtn");
const uploadBtn = document.getElementById("uploadBtn");
const fileInput = document.getElementById("fileInput");
const message = document.getElementById("message");

// Événement click pour uploader le CSV
    uploadBtn.addEventListener("click", async () => {
        const file = fileInput.files[0];
        if (!file) {
            message.textContent = "Sélectionne un fichier CSV.";
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("/api/admin/upload/products", {
                method: "POST",
                headers: authHeaders(), // ✅ seulement Authorization
                body: formData
            });

            const data = await response.json();

            if (response.ok && data.success) {
                message.textContent = data.success;
                alert("Importation terminée avec succès. La page va se recharger !");
                window.location.reload(); // reload après l'alerte
            } else {
                message.textContent = "Erreur: " + (data.error || data.message || "Impossible d'uploader");
            }
        } catch (err) {
            message.textContent = "Erreur: " + err.message;
        }
    });






document.getElementById("generateInvoiceBtn").addEventListener("click", async () => {
    const orderNumber = document.getElementById("orderNumberInput").value.trim();
    if (!orderNumber) {
        alert("Merci d'entrer un numéro de commande !");
        return;
    }

    try {
        const response = await fetch(`/api/admin/invoice/${orderNumber}`, {
            headers: authHeaders()
        });

        if (!response.ok) {
            alert("Erreur récupération facture !");
            return;
        }

        const htmlContent = await response.text();

        // Crée un Blob avec le HTML
        const blob = new Blob([htmlContent], { type: "text/html" });
        const url = URL.createObjectURL(blob);

        // Crée un lien temporaire pour télécharger le fichier
        const a = document.createElement("a");
        a.href = url;
        a.download = `facture_${orderNumber}.html`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(url);

        alert("Facture téléchargée !");
    } catch (err) {
        alert("Erreur: " + err.message);
    }
});



