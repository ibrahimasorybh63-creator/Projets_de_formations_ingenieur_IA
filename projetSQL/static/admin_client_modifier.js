function switch_state(to_show, to_hide) {
    const elementShow = document.getElementById(to_show);
    const elementHide = document.getElementById(to_hide);

    if (!elementShow || !elementHide) return;

    elementHide.classList.add("hidden");
    elementShow.classList.remove("hidden");
}
function initialiserGestionClient() {
    const supprimer_client = document.getElementById('sup_client');
    if (supprimer_client) {
        supprimer_client.addEventListener('click', function() {
            switch_state('confirm_sup', 'fiche_client');
            const confirmation = document.getElementById('suppression_client');
            const negation = document.getElementById('annulation_sup');
            const id = document.getElementById('identif').value;
            confirmation.addEventListener('click', function() {
                fetch("/clients/supprimer", {
                    method: "POST",
                    body: new URLSearchParams({
                        clients_id: id
                    })
                })
                .then(response => {

                    if (response.ok) {
                        afficherToast("Utilisateur supprimé de la base.");
                        chargerContenu("/clients");
                    }

                });
            });
            negation.addEventListener('click', function() {
                switch_state('fiche_client', 'confirm_sup');
            });
        });
    }
    const modifier_client = document.getElementById('modifier_client')
    if (modifier_client) {
        modifier_client.addEventListener('click',function(){
            switch_state('formulaire','fiche_client')
            form = document.getElementById('formulaire')
            if (!form)
                return
            else
                if (document.getElementById('zone_catalogue')) {
                    interceptFormulaire('formulaire');
                } 
                else {
                    interceptFormulaireProfil('formulaire');
                }
        })
    }
}
function interceptFormulaireProfil(formId) {
    const conteneur = document.getElementById(formId);
    if (!conteneur) return;
    const form = conteneur.querySelector("form");
    if (!form) return;
    form.addEventListener("submit", async function(event) {
        event.preventDefault();
        const donnees = new FormData(form);
        const response = await fetch(form.action, {
            method: "POST",
            body: donnees
        });
        if (response.ok) {
            afficherToast("Informations mises à jour.", "succes");
            setTimeout(() => window.location.reload(), 1500);
        } else {
            afficherToast("Erreur lors de la mise à jour.", "erreur");
        }
    });
}

