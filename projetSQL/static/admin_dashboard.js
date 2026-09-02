const toutesLesZones = [
    "zone_catalogue","zone_dashboard",
    "form_ajout_produit",
    "form_ajout_commande",
];

function cacherTout() {
    toutesLesZones.forEach(id => document.getElementById(id).style.display = "none");
}

function afficher(id) {
    cacherTout();
    document.getElementById(id).style.display = "block";
}

// Charge un fragment HTML dans le tableau de bord puis réactive les gestionnaires associés à ce contenu dynamique.
function chargerContenu(url) {
    cacherTout();
    fetch(url)
        .then(response => response.text())
        .then(html => {
            document.getElementById("zone_catalogue").innerHTML = html;
            document.getElementById("zone_catalogue").style.display = "block";
            interceptFormulaireProduit();
            initformcommande();
            initialiserGestionClient();
        });
}

// Intercepte un formulaire chargé dans le tableau de bord pour soumettre ses données et remplacer le catalogue sans rechargement.
function interceptFormulaire(formId) {
    const conteneur = document.getElementById(formId);
    if (!conteneur) return;
    const form = conteneur.querySelector("form");
    if (!form) return;
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        const url = form.action;
        const donnees = new FormData(form);

        fetch(url, {
            method: "POST",
            body: donnees
        })
        .then(response => response.text())
        .then(html => {
            document.getElementById("zone_catalogue").innerHTML = html;
            afficher("zone_catalogue");
        });
    });
}

[
    "form_ajout_produit",
    "form_ajout_commande",].forEach(interceptFormulaire);

initAjoutLigneProduit("btn_ajouter_ligne", "lignes_produits");

// Gère spécifiquement l'envoi asynchrone du formulaire de modification d'un produit et le retour visuel associé.
function interceptFormulaireProduit() {
    const formulaire = document.getElementById('formulaire');
    if (!formulaire) return;
    formulaire.addEventListener('submit', async function(event) {
        event.preventDefault();
        const donnees = new FormData(formulaire);
        const response = await fetch(formulaire.action, {
            method: "POST",
            body: donnees
        });
        const html = await response.text();
        document.getElementById("zone_catalogue").innerHTML = html;
        afficherToast("Produit modifié avec succès.", "succes");
    });
}
function supprimer_produit(){
                const id = document.getElementById('identif').value;
                fetch("/produits/supprimer?id="+id,{
                    method:'POST'
                })
                .then(response => {
                    if (response.ok) {
                        afficherToast("Produit supprimé de la base.");
                        chargerContenu("/produits");
                    }

                });
};
