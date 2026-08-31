const envoie = document.getElementById('envoie');
if (envoie) {
    envoie.addEventListener("click", async function() {
        let email = document.getElementById('mail').value
        let mdp = document.getElementById('mdp').value
        const response = await fetch('/connexion',{
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, mdp: mdp })
        });
        const data = await response.json();
        if (response.status === 200) {
            afficherToast(data.message,"succes")
            setTimeout(() => {
                window.location.href = '/shop';
            }, 2500);
            return;
        };
        if (!response.ok){
            afficherToast(data.message,"erreur");
            return;
        };
    });
}

const toggle_mdp = document.getElementById('toggle_mdp');
if (toggle_mdp) {
    toggle_mdp.addEventListener('click', function() {
        const champ = document.getElementById('mdp');
        champ.type = champ.type === 'password' ? 'text' : 'password';
        document.getElementById('open_eye').classList.toggle('hidden')
        document.getElementById('closed_eye').classList.toggle('hidden')
    });
}

const confirmer_inscrip = document.getElementById('confirmer_inscrip');
if (confirmer_inscrip) {
    confirmer_inscrip.addEventListener("click", async function() {
        let email = document.getElementById('email_inscrip').value
        let mdp = document.getElementById('mdp').value
        let nom = document.getElementById('nom_inscrip').value
        let prenom = document.getElementById('prenom_inscrip').value
        let adresse = document.getElementById('adresse_inscrip').value
        let confirm = document.getElementById('mdp_confirm').value
        if (email === "" || mdp === "" || nom === "" || prenom === "") {
            afficherToast("Veuillez remplir tous les champs obligatoires.", "erreur");
            return;
        };
        if (mdp != confirm){
            afficherToast("Les mots de passe ne correspondent pas.","erreur")
            return;
        };
        const response = await fetch('/inscription',{
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, mdp: mdp, nom: nom, prenom: prenom, adresse: adresse })
        });
        const data = await response.json();
        if (response.status === 200) {
            afficherToast(data.message,"succes")
            setTimeout(() => {
                window.location.href = '/shop';
            }, 2500);
            return;
        };
        if (!response.ok){
            afficherToast(data.message,"erreur");
            return;
        };
    });
}
const admin = document.getElementById('admin_login');
if (admin) {
    admin.addEventListener("click", async function() {
        let email = document.getElementById('mail').value
        let mdp = document.getElementById('mdp').value
        const response = await fetch('/admin_connexion',{
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, mdp: mdp })
        });
        const data = await response.json();
        if (response.status === 200) {
            afficherToast(data.message,"succes")
            setTimeout(() => {
                window.location.href = '/admin';
            }, 2500);
            return;
        };
        if (!response.ok){
            afficherToast(data.message,"erreur");
            return;
        };
    });
}