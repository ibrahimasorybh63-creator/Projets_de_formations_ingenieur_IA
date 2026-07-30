const toutesLesZones = [
    "zone_catalogue","zone_dashboard",
    "form_ajout_produit", "form_modifier_produit", "form_supprimer_produit",
    "form_ajout_client", "form_modifier_client", "form_supprimer_client",
    "form_ajout_commande", "form_modifier_commande", "form_supprimer_commande",
];

function cacherTout() {
    toutesLesZones.forEach(id => document.getElementById(id).style.display = "none");
}

function afficher(id) {
    cacherTout();
    document.getElementById(id).style.display = "block";
}
function chargerContenu(url) {
    cacherTout();
    fetch(url)
        .then(response => response.text())
        .then(html => {
            document.getElementById("zone_catalogue").innerHTML = html;
            document.getElementById("zone_catalogue").style.display = "block";
        });
}
function interceptFormulaire(formId) {
    const form = document.getElementById(formId).querySelector("form");
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
    "form_ajout_produit", "form_modifier_produit", "form_supprimer_produit",
    "form_ajout_client", "form_modifier_client", "form_supprimer_client",
    "form_ajout_commande", "form_modifier_commande", "form_supprimer_commande",
].forEach(interceptFormulaire);
const btnAjouter = document.getElementById("btn_ajouter_ligne");
const lignesProduits = document.getElementById("lignes_produits");

btnAjouter.addEventListener("click", () => {
    const ligne = document.createElement("div");
    ligne.className = "ligne_produit";

    ligne.innerHTML = `
        <input
            type="number"
            placeholder="id produit"
            name="produits_id[]"
            required
        />
        <input
            type="number"
            placeholder="quantité"
            name="quantite[]"
            required
        />
        <button type="button" class="supprimer">❌</button>
    `;

    ligne.querySelector(".supprimer").addEventListener("click", () => {
        ligne.remove();
    });

    lignesProduits.appendChild(ligne);
});