let modePromo = false;
let timerRecherche;

const zoneCatalogue = document.getElementById("zone_catalogue");
const zoneHero = document.getElementById("zone_haut_vitrine");
const zoneRecherche = document.getElementById("zone_recherche");
const zoneFiltre = document.getElementById("zone_filtre");
const filtreCategorie = document.getElementById("filtre_categorie");
const barreRecherche = document.getElementById("barre_recherche");

function definirVisibilite(element, visible) {
    element?.classList.toggle("hidden", !visible);
}

function revenirEnHaut() {
    window.scrollTo({ top: 0, behavior: "smooth" });
}

async function chargerContenuShop(url) {
    const response = await fetch(url);
    if (!response.ok) {
        zoneCatalogue.innerHTML = "<p class='text-center text-red-600'>Le contenu n’a pas pu être chargé.</p>";
        return;
    }
    zoneCatalogue.innerHTML = await response.text();
}

function construireUrlCatalogue() {
    const params = new URLSearchParams();
    const categorie = filtreCategorie.value;
    const texte = barreRecherche.value.trim();
    if (categorie) params.set("categorie", categorie);
    if (texte) params.set("recherche", texte);
    if (modePromo) params.set("promo", "true");
    return `/shop_produit?${params.toString()}`;
}

function appliquerFiltres() {
    return chargerContenuShop(construireUrlCatalogue());
}

function afficherAccueil() {
    modePromo = false;
    filtreCategorie.value = "";
    barreRecherche.value = "";
    definirVisibilite(zoneHero, true);
    definirVisibilite(zoneRecherche, true);
    definirVisibilite(zoneFiltre, false);
    chargerContenuShop("/shop_vitrine");
    revenirEnHaut();
}

function afficherProduits() {
    modePromo = false;
    definirVisibilite(zoneHero, false);
    definirVisibilite(zoneRecherche, true);
    definirVisibilite(zoneFiltre, true);
    appliquerFiltres();
    revenirEnHaut();
}

function afficherPromotions() {
    modePromo = true;
    definirVisibilite(zoneHero, false);
    definirVisibilite(zoneRecherche, true);
    definirVisibilite(zoneFiltre, true);
    appliquerFiltres();
    revenirEnHaut();
}

function afficherContact() {
    modePromo = false;
    definirVisibilite(zoneHero, false);
    definirVisibilite(zoneRecherche, false);
    definirVisibilite(zoneFiltre, false);
    chargerContenuShop("/shop_contact");
    revenirEnHaut();
}

function naviguer(onglet) {
    const actions = {
        accueil: afficherAccueil,
        produits: afficherProduits,
        promotions: afficherPromotions,
        contact: afficherContact,
    };
    actions[onglet]?.();
}

document.getElementById("navigation_accueil")?.addEventListener("click", () => naviguer("accueil"));
document.getElementById("navigation_produits")?.addEventListener("click", () => naviguer("produits"));
document.getElementById("navigation_promotions")?.addEventListener("click", () => naviguer("promotions"));
document.getElementById("navigation_contact")?.addEventListener("click", () => naviguer("contact"));
document.querySelectorAll("[data-navigation]").forEach((lien) => {
    lien.addEventListener("click", () => naviguer(lien.dataset.navigation));
});

filtreCategorie?.addEventListener("change", appliquerFiltres);
barreRecherche?.addEventListener("focus", () => {
    modePromo = false;
    definirVisibilite(zoneHero, false);
    definirVisibilite(zoneFiltre, true);
    appliquerFiltres();
});
barreRecherche?.addEventListener("input", () => {
    window.clearTimeout(timerRecherche);
    timerRecherche = window.setTimeout(appliquerFiltres, 300);
});

function afficherToast(message, type = "succes") {
    const couleur = type === "succes" ? "bg-green-500" : "bg-red-500";
    const toast = document.createElement("div");
    toast.className = `${couleur} text-white px-4 py-2 rounded shadow-lg transition-opacity duration-300`;
    toast.textContent = message;
    document.getElementById("zone_toast")?.appendChild(toast);
    setTimeout(() => toast.remove(), 2000);
}

async function ajouterAuPanier(id) {
    const quantite = parseInt(document.getElementById("quantite_" + id).value, 10);
    const response = await fetch("/ajouter_panier", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id_produit: id, quantite }),
    });
    const data = await response.json();
    if (!response.ok) return afficherToast(data.message, "erreur");
    const badge = document.getElementById("compteur_panier");
    badge.textContent = data.quantite;
    badge.classList.remove("hidden");
    afficherToast(data.message);
}

function panier_est_vide() {
    return document.querySelectorAll('[id^="zone_commande"]').length === 0;
}

function supprimerDuPanier(id_produit) {
    const sousTotal = Number(document.getElementById("sous_total" + id_produit).textContent);
    const totalGeneral = document.getElementById("total_general");
    totalGeneral.textContent = Number(totalGeneral.textContent) - sousTotal;
    fetch("/supprimer_panier?id=" + id_produit, { method: "POST" });
    document.getElementById("zone_commande" + id_produit).remove();
    afficherToast("Produit supprimé du panier.", "suppression");
    if (panier_est_vide()) document.getElementById("zone_card").innerHTML = '<p class="flex text-gray-500 text-center justify-center">Votre panier est vide.</p>';
}

async function modifierQuantite(id_produit) {
    const nouvelleQuantite = parseInt(document.getElementById("nv_quantite_" + id_produit).value, 10);
    const response = await fetch("/modifier_panier", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id_produit, quantite: nouvelleQuantite }),
    });
    const data = await response.json();
    if (!response.ok) return afficherToast(data.message, "erreur");
    const sousTotal = document.getElementById("sous_total" + id_produit);
    const totalGeneral = document.getElementById("total_general");
    totalGeneral.textContent = Number(totalGeneral.textContent) - Number(sousTotal.textContent) + data.sous_total;
    sousTotal.textContent = data.sous_total;
    afficherToast("Quantité mise à jour.");
}

async function validerCommande() {
    const response = await fetch("/valider_commande", { method: "POST" });
    const data = await response.json();
    if (response.status === 401) return window.location.assign("/");
    if (!response.ok) return afficherToast(data.message, "erreur");
    afficherToast(data.message);
    setTimeout(() => window.location.assign("/shop"), 2500);
}

async function connecter(url, email, mdp, destination) {
    const response = await fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, mdp }) });
    const data = await response.json();
    if (!response.ok) return afficherToast(data.message, "erreur");
    afficherToast(data.message);
    setTimeout(() => window.location.assign(destination), 2500);
}

document.getElementById("envoie")?.addEventListener("click", () => connecter("/connexion", document.getElementById("mail").value, document.getElementById("mdp").value, "/shop"));
document.getElementById("admin_login")?.addEventListener("click", () => connecter("/admin_connexion", document.getElementById("mail").value, document.getElementById("mdp").value, "/admin"));

document.getElementById("toggle_mdp")?.addEventListener("click", () => {
    const champ = document.getElementById("mdp");
    champ.type = champ.type === "password" ? "text" : "password";
    document.getElementById("open_eye").classList.toggle("hidden");
    document.getElementById("closed_eye").classList.toggle("hidden");
});

document.getElementById("confirmer_inscrip")?.addEventListener("click", async () => {
    const email = document.getElementById("email_inscrip").value;
    const mdp = document.getElementById("mdp").value;
    const nom = document.getElementById("nom_inscrip").value;
    const prenom = document.getElementById("prenom_inscrip").value;
    const adresse = document.getElementById("adresse_inscrip").value;
    const confirmation = document.getElementById("mdp_confirm").value;
    if (!email || !mdp || !nom || !prenom) return afficherToast("Veuillez remplir tous les champs obligatoires.", "erreur");
    if (mdp !== confirmation) return afficherToast("Les mots de passe ne correspondent pas.", "erreur");
    const response = await fetch("/inscription", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email, mdp, nom, prenom, adresse }) });
    const data = await response.json();
    if (!response.ok) return afficherToast(data.message, "erreur");
    afficherToast(data.message);
    setTimeout(() => window.location.assign("/shop"), 2500);
});
