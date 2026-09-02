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
// Ajoute au formulaire une ligne produit autonome avec ses champs et son propre bouton de suppression.
function initAjoutLigneProduit(btnId, conteneurId) {
    const bouton = document.getElementById(btnId);
    const conteneur = document.getElementById(conteneurId);

    if (!bouton || !conteneur) return;

    bouton.addEventListener("click", () => {
        const ligne = document.createElement("div");
        ligne.className = "ligne_produit flex flex-wrap items-center gap-2 bg-gray-50 border rounded p-3";

        ligne.innerHTML = `
            <div class="flex flex-col flex-1 text-left">
                <label class="text-sm">Identifiant du produit</label>
                <input type="number" min='1' placeholder="id produit" class="border-2 border-black rounded m-1 text-center" name="produits_id[]" required />
            </div>
            <div class="flex flex-col flex-1 text-left">
                <label class="text-sm">Quantité</label>
                <input type="number" min='1' placeholder="quantité" class="border-2 border-black rounded m-1 text-center" name="quantite[]" required />
            </div>
            <button type="button" class="supprimer bg-red-500 hover:bg-red-700 text-white rounded w-8 h-8 mt-4">❌</button>
        `;

        ligne.querySelector(".supprimer").addEventListener("click", () => {
            ligne.remove();
        });

        conteneur.appendChild(ligne);
    });
}

function ajusterEspaceNav() {
    const nav = document.getElementById('barre_nav');
    const espace = document.getElementById('espace_nav');
    if (nav && espace) {
        espace.style.height = nav.offsetHeight + 'px';
    }
}
window.addEventListener('load', ajusterEspaceNav);
window.addEventListener('resize', ajusterEspaceNav);