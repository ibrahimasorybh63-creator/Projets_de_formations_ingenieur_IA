function chargerCont_shop(url) {
    fetch(url)
        .then(response => response.text())
        .then(html => {
            document.getElementById("zone_catalogue").innerHTML = html;
            document.getElementById("zone_catalogue").style.display = "block";
        });
}

toutesLesZones = ["zone_haut_vitrine"];
function cacherTout() {
    toutesLesZones.forEach(id => document.getElementById(id).style.display = "none");
    document.getElementById('zone_recherche').style.display = ''
}
function afficherTout() {
    toutesLesZones.forEach(id => document.getElementById(id).style.display = "");
}
function filtre_on() {
    document.getElementById("zone_filtre").style.display = "flex";
}
function filtre_off() {
    document.getElementById("zone_filtre").style.display = "none";
}
function cacher_barre() {
    document.getElementById('zone_recherche').style.display = 'none'
}

// --- Gestion des filtres combinés (catégorie, recherche, promo) ---

let modePromo = false;

function appliquerFiltres() {
    const categorie = document.getElementById('filtre_categorie').value;
    const texte = document.getElementById('barre_recherche').value;

    let url = '/shop_produit?';
    if (categorie) {
        url += 'categorie=' + categorie + '&';
    }
    if (texte) {
        url += 'recherche=' + texte + '&';
    }
    if (modePromo) {
        url += 'promo=true&';
    }

    chargerCont_shop(url);
}

function activerModePromo() {
    modePromo = true;
    appliquerFiltres();
}

function activerModeCatalogue() {
    modePromo = false;
    appliquerFiltres();
}

const el_filtre_categorie = document.getElementById("filtre_categorie");
if (el_filtre_categorie) {
    el_filtre_categorie.addEventListener("change", function() {
        appliquerFiltres();
    });
}

let timer;
function debounce(fn, delai) {
    clearTimeout(timer);
    timer = setTimeout(fn, delai);
}

const el_barre_recherche = document.getElementById("barre_recherche");
if (el_barre_recherche) {
    el_barre_recherche.addEventListener('input', function() {
        debounce(function() {
            appliquerFiltres();
        }, 300);
    });
}

function afficherToast(message, type = "succes") {
    const couleur = type === "succes" ? "bg-green-500" : "bg-red-500";

    const toast = document.createElement("div");
    toast.className = `${couleur} text-white px-4 py-2 rounded shadow-lg transition-opacity duration-300`;
    toast.textContent = message;

    document.getElementById("zone_toast").appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 2000);
}

async function ajouterAuPanier(id) {
    const inputQuantite = document.getElementById("quantite_" + id);
    const quantite = parseInt(inputQuantite.value);

    const response = await fetch('/ajouter_panier', {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id_produit: id, quantite: quantite })
    });

    const data = await response.json();

    if (!response.ok) {
        afficherToast(data.message,"erreur")
        return;
    }

    const badge = document.getElementById("compteur_panier");
    badge.textContent = data.quantite;
    badge.classList.remove("hidden");
    afficherToast(data.message)
};

function panier_est_vide() {
    return document.querySelectorAll('[id^="zone_commande"]').length === 0;
};

function supprimerDuPanier(id_produit){
    sous_total =  document.getElementById('sous_total' + id_produit).textContent
    total_general = document.getElementById('total_general').textContent
    nv_total = parseInt(total_general) - parseInt(sous_total)
    document.getElementById('total_general').textContent = nv_total
    fetch('/supprimer_panier?id=' + id_produit, {
    method: 'POST'
})
    document.getElementById('zone_commande'+id_produit).remove();
    afficherToast("Produit supprimer du panier.","suppression");
    if (panier_est_vide() == true){
        page = ` <p class="flex text-gray-500 text-center justify-center">Votre panier est vide.</p>`
        document.getElementById('zone_card').innerHTML = page
    }
    
};

async function modifierQuantite(id_produit) {
    const input = document.getElementById("nv_quantite_" + id_produit);
    const nouvelleQuantite = parseInt(input.value);

    const response = await fetch('/modifier_panier', {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id_produit: id_produit, quantite: nouvelleQuantite })
    });

    const data = await response.json();

    if (!response.ok) {
        afficherToast(data.message, "erreur");
        return;
    }

    // Mettre à jour le sous-total affiché de cette ligne
    const ancienSousTotal = parseInt(document.getElementById("sous_total" + id_produit).textContent);
    document.getElementById("sous_total" + id_produit).textContent = data.sous_total;

    // Mettre à jour le total général
    const totalActuel = parseInt(document.getElementById("total_general").textContent);
    const nouveauTotal = totalActuel - ancienSousTotal + data.sous_total;
    document.getElementById("total_general").textContent = nouveauTotal;

    afficherToast("Quantité mise à jour.", "succes");
};

async function validerCommande() {
    const response = await fetch('/valider_commande',{
        method:"POST",
    });
    const data = await response.json();
    if (response.status === 401) {
    window.location.href = '/';
    return;
    };
    if (!response.ok){
        afficherToast(data.message,"erreur");
        return;
    };
    afficherToast(data.message,"succes")
    setTimeout(() => {
    window.location.href = '/shop';
    }, 2500);
};

const el_envoie = document.getElementById('envoie');
if (el_envoie) {
    el_envoie.addEventListener("click", async function() {
        let email = document.getElementById('mail').value
        let mdp = document.getElementById('mdp').value
        const response = await fetch('/connexion',{
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, mdp: mdp })
        });
        const data = await response.json();
        if (response.status === 200) {
            afficherToast(data.message,"succes")
            setTimeout(() => {
                window.location.href = '/shop';
            }, 2500);
            return;
        };
        if (!response.ok){
            afficherToast(data.message,"erreur");
            return;
        };
    });
}

const el_toggle_mdp = document.getElementById('toggle_mdp');
if (el_toggle_mdp) {
    el_toggle_mdp.addEventListener('click', function() {
        const champ = document.getElementById('mdp');
        champ.type = champ.type === 'password' ? 'text' : 'password';
        document.getElementById('open_eye').classList.toggle('hidden')
        document.getElementById('closed_eye').classList.toggle('hidden')
    });
}

const el_confirmer_inscrip = document.getElementById('confirmer_inscrip');
if (el_confirmer_inscrip) {
    el_confirmer_inscrip.addEventListener("click", async function() {
        let email = document.getElementById('email_inscrip').value
        let mdp = document.getElementById('mdp').value
        let nom = document.getElementById('nom_inscrip').value
        let prenom = document.getElementById('prenom_inscrip').value
        let adresse = document.getElementById('adresse_inscrip').value
        let confirm = document.getElementById('mdp_confirm').value
        if (email === "" || mdp === "" || nom === "" || prenom === "") {
            afficherToast("Veuillez remplir tous les champs obligatoires.", "erreur");
            return;
        };
        if (mdp != confirm){
            afficherToast("Les mots de passe ne correspondent pas.","erreur")
            return;
        };
        const response = await fetch('/inscription',{
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, mdp: mdp, nom: nom, prenom: prenom, adresse: adresse })
        });
        const data = await response.json();
        if (response.status === 200) {
            afficherToast(data.message,"succes")
            setTimeout(() => {
                window.location.href = '/shop';
            }, 2500);
            return;
        };
        if (!response.ok){
            afficherToast(data.message,"erreur");
            return;
        };
    });
}
const el_admin = document.getElementById('admin_login');
if (el_admin) {
    el_admin.addEventListener("click", async function() {
        let email = document.getElementById('mail').value
        let mdp = document.getElementById('mdp').value
        const response = await fetch('/admin_connexion',{
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, mdp: mdp })
        });
        const data = await response.json();
        if (response.status === 200) {
            afficherToast(data.message,"succes")
            setTimeout(() => {
                window.location.href = '/admin';
            }, 2500);
            return;
        };
        if (!response.ok){
            afficherToast(data.message,"erreur");
            return;
        };
    });
}