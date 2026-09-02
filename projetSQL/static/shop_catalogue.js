let modePromo = false;
let timerRecherche;

const zoneCatalogue = document.getElementById("zone_catalogue");
const zoneHero = document.getElementById("zone_haut_vitrine");
const iconesCategorie = document.getElementById("icone_categorie");
const zoneRecherche = document.getElementById("zone_recherche");
const zoneFiltre = document.getElementById("zone_filtre");
const filtreCategorie = document.getElementById("filtre_categorie");
const barreRecherche = document.getElementById("barre_recherche");

function definirVisibilite(element, visible) {
    element?.classList.toggle("hidden", !visible);
}

function retourHaut() {
    window.scrollTo({ top: 0, behavior: "smooth" });
}

async function chargerContenuShop(url) {
    const response = await fetch(url);
    if (!response.ok) {
        zoneCatalogue.innerHTML = "<p class='text-center text-red-600'>Le contenu n’a pas pu être chargé.</p>";
        definirVisibilite(zoneCatalogue, true);
        return;
    }
    zoneCatalogue.innerHTML = await response.text();
    definirVisibilite(zoneCatalogue, true);
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

function masquerAccueil() {
    definirVisibilite(zoneHero, false);
    definirVisibilite(iconesCategorie, false);
}

function allerAccueil() {
    modePromo = false;
    filtreCategorie.value = "";
    barreRecherche.value = "";
    definirVisibilite(zoneHero, true);
    definirVisibilite(iconesCategorie, true);
    definirVisibilite(zoneRecherche, false);
    definirVisibilite(zoneFiltre, false);
    chargerContenuShop("/shop_vitrine");
    retourHaut();
}

function allerProduits() {
    modePromo = false;
    masquerAccueil();
    definirVisibilite(zoneRecherche, true);
    definirVisibilite(zoneFiltre, true);
    appliquerFiltres();
    retourHaut();
}

function allerPromotions() {
    modePromo = true;
    masquerAccueil();
    definirVisibilite(zoneRecherche, true);
    definirVisibilite(zoneFiltre, true);
    appliquerFiltres();
    retourHaut();
}

function allerContact() {
    modePromo = false;
    masquerAccueil();
    definirVisibilite(zoneRecherche, false);
    definirVisibilite(zoneFiltre, false);
    chargerContenuShop("/shop_contact");
    retourHaut();
}

function ouvrirRecherche() {
    modePromo = false;
    masquerAccueil();
    definirVisibilite(zoneRecherche, true);
    definirVisibilite(zoneFiltre, true);
    appliquerFiltres();
    barreRecherche.focus();
    retourHaut();
}

function filtrerParCategorie(categorie) {
    modePromo = false;
    filtreCategorie.value = categorie;
    allerProduits();
}

function naviguer(destination) {
    const actions = {
        accueil: allerAccueil,
        produits: allerProduits,
        promotions: allerPromotions,
        contact: allerContact,
    };
    actions[destination]?.();
}

document.getElementById("navigation_accueil")?.addEventListener("click", () => naviguer("accueil"));
document.getElementById("navigation_produits")?.addEventListener("click", () => naviguer("produits"));
document.getElementById("navigation_promotions")?.addEventListener("click", () => naviguer("promotions"));
document.getElementById("navigation_contact")?.addEventListener("click", () => naviguer("contact"));
document.getElementById("recherche")?.addEventListener("click", ouvrirRecherche);
document.querySelectorAll("[data-navigation]").forEach((element) => {
    element.addEventListener("click", () => naviguer(element.dataset.navigation));
});
document.querySelectorAll("[data-categorie]").forEach((element) => {
    element.addEventListener("click", () => filtrerParCategorie(element.dataset.categorie));
});

filtreCategorie?.addEventListener("change", appliquerFiltres);
barreRecherche?.addEventListener("input", () => {
    clearTimeout(timerRecherche);
    timerRecherche = setTimeout(appliquerFiltres, 300);
});

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

function appliquer_font_text() {
    document.querySelectorAll("h1, h2, h3, p").forEach((element) => {
        element.classList.add("font-serif");
    });
}

appliquer_font_text();
