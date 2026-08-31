function initformcommande() {
    initAjoutLigneProduit("btn_ajouter_ligne_modif", "lignes_produits_modif");

    document.querySelectorAll('.ligne_produit .supprimer').forEach(bouton => {
        bouton.addEventListener('click', () => {
            bouton.closest('.ligne_produit').remove();
        });
    });
    form = document.getElementById('formulaire')
    if (!form)
        return
    else
        interceptFormulaire('formulaire')
}
function supprimer_commande(){
                const id = document.getElementById('identif').value;
                fetch("/commandes/supprimer?id="+id,{
                    method:'POST'
                })
                .then(response => {
                    if (response.ok) {
                        afficherToast("commande supprimé de la base.");
                        chargerContenu("/commandes");
                    }

                });
};