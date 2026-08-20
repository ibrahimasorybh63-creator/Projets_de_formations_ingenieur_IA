const btnAjouterModif = document.getElementById("btn_ajouter_ligne");
const lignesProduitsModif = document.getElementById("lignes_produits");

if (btnAjouterModif && lignesProduitsModif) {
    btnAjouterModif.addEventListener("click", () => {
        const ligne = document.createElement("div");
        ligne.className = "ligne_produit";

        ligne.innerHTML = `
            <input type="number" min='1' placeholder="id produit" name="produits_id[]" class="border-2 border-black rounded m-1" required/>
            <input type="number" min='1' placeholder="quantité" name="quantite[]" class="border-2 border-black rounded m-1" required/>
            <button type="button" class="supprimer">❌</button>`
            ;
        ligne.querySelector(".supprimer").addEventListener("click", () => {
            ligne.remove();
        });

        lignesProduitsModif.appendChild(ligne);
    });
}

document.querySelectorAll('.ligne_produit .supprimer').forEach(bouton => {
    bouton.addEventListener('click', () => {
        bouton.closest('.ligne_produit').remove();
    });
});