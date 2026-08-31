function chargerCont_shop(url) {
    fetch(url)
        .then(response => response.text())
        .then(html => {
                document.getElementById("zone_catalogue").innerHTML = html;
                document.getElementById("zone_catalogue").style.display = "block";  
        });
}


toutesLesZones = ["zone_haut_vitrine","icone_categorie"];
function cacherTout() {
    toutesLesZones.forEach(id => document.getElementById(id).style.display = "none");
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

function afficher_barre() {
    document.getElementById('zone_recherche').classList.toggle('hidden')
    cible =  document.getElementById('zone_haut_vitrine')
    if (cible)
        cible.classList.toggle('hidden')
}


let modePromo = false;

function appliquerFiltres(panel_categorie = null) {
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
    if (panel_categorie) {
        url += 'categorie=' + panel_categorie + '&';
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
const filtre_categorie = document.getElementById("filtre_categorie");
if (filtre_categorie) {
    filtre_categorie.addEventListener("change", function() {
        appliquerFiltres();
    });
}

let timer;
function debounce(fn, delai) {
    clearTimeout(timer);
    timer = setTimeout(fn, delai);
}

const barre_recherche = document.getElementById("barre_recherche");
if (barre_recherche) {
    barre_recherche.addEventListener('input', function() {
        debounce(function() {
            appliquerFiltres();
        }, 300);
    });
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
function appliquer_font_text() {
    document.querySelectorAll('h1, h2, h3, p').forEach(element => {
        element.classList.add('font-serif');
    });
}

appliquer_font_text();