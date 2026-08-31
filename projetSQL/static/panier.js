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
    if (badge) {
        badge.textContent = data.quantite;
        badge.classList.remove("hidden");
    }
    afficherToast(data.message);
    recomm_panier = document.getElementById('zone_recomm_panier')
    if (recomm_panier)
        window.location.reload()
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
    window.location.href = '/confirmation_commande?id=' + data.commande_id;
    }, 2500);
};