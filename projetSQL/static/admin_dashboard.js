const toutesLesZones = [
    "zone_catalogue","zone_dashboard",
    "form_ajout_produit", "form_modifier_produit", "form_supprimer_produit",
    "form_modifier_client", "form_supprimer_client",
    "form_ajout_commande","form_supprimer_commande",
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
    "form_ajout_produit", "form_modifier_produit", "form_supprimer_produit",
    "form_modifier_client", "form_supprimer_client",
    "form_ajout_commande","form_supprimer_commande"
].forEach(interceptFormulaire);

const btnAjouter = document.getElementById("btn_ajouter_ligne");
const lignesProduits = document.getElementById("lignes_produits");

if (btnAjouter && lignesProduits) {
    btnAjouter.addEventListener("click", () => {
        const ligne = document.createElement("div");
        ligne.className = "ligne_produit";

        ligne.innerHTML = `
            <input type="number" min='1' placeholder="id produit" class="border-2 border-black rounded m-1" name="produits_id[]" required />
            <input type="number" min='1' placeholder="quantité" class="border-2 border-black rounded m-1" name="quantite[]" required />
            <button type="button" class="supprimer">❌</button>
        `;

        ligne.querySelector(".supprimer").addEventListener("click", () => {
            ligne.remove();
        });

        lignesProduits.appendChild(ligne);
    });
}