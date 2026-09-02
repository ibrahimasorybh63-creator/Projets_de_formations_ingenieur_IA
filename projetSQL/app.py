from flask import Flask, render_template, request, redirect
import sqlite3
import entite
from flask import session
from flask import jsonify
import random
import os
from dotenv import load_dotenv
from setup.recommendations import content_based, collaborative
from datetime import date
from setup.recommendations.baseline import recalculer_taux_vente
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

ADMIN_EMAIL = os.environ["ADMIN_EMAIL"]
ADMIN_MDP_HASH = generate_password_hash(os.environ["ADMIN_PASSWORD"])
app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

def get_conn():
    conn = sqlite3.connect("boutique.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def id_depuis_requete(source, cle):
    """Récupère un identifiant entier depuis request.args ou request.form.
    Renvoie None si absent ou non numérique, plutôt que de lever une exception."""
    valeur = source.get(cle)
    if valeur is None:
        return None
    try:
        return int(valeur)
    except ValueError:
        return None 


def _sauvegarder_client(conn, id_client, form):
    """Valide l'unicité de l'email et met à jour un client.
    Renvoie une réponse d'erreur (tuple) en cas d'échec, sinon None."""
    nom = form["nom"]
    prenom = form["prenom"]
    adresse = form["adresse"]
    email = form["email"]
    cur = conn.cursor()
    cur.execute("SELECT clients_id FROM clients WHERE email = ? AND clients_id != ?", (email, id_client))
    if cur.fetchone():
        return jsonify({"message": "Cet email existe déjà."}), 400
    entite.Clients.modifier_client(conn, nom, prenom, adresse, email, id_client)
    return None

#page de l'admin et ses routes
@app.route("/admin")
def accueil_admin():
    conn = get_conn()
    stats = entite.get_stats(conn)
    produits_top = entite.produits_les_plus_achetes(conn)
    top5_clients = [{"nom": c[0], "prenom": c[1], "montant": c[2]} for c in entite.top_5(conn)]
    ca_categories = entite.donnut_CA(conn)
    conn.close()
    noms_produits = [p[0] for p in produits_top]
    quantites = [p[1] for p in produits_top]
    categories = [c[0] for c in ca_categories]
    montants_ca = [c[1] for c in ca_categories]
    return render_template("/admin/main.html", stats=stats,noms_produits=noms_produits, quantites=quantites,categories = categories,montants_ca = montants_ca,top_client = top5_clients)

@app.route("/produits/ajouter",methods=['GET','POST'])
def ajouter_produit():
    if request.method == 'POST':
        nom = request.form["nom"]
        prix = float(request.form["prix"])
        type_prod = request.form["type_prod"]
        prix_promo = request.form.get('prix_promo')
        description = request.form.get('descrip',None)
        if prix_promo:
            prix_promo = float(prix_promo)
        else:
            prix_promo = None
        conn = get_conn()
        produit = entite.Produit(conn, nom, prix, type_prod,prix_promo,description)
        produit.ajouter_en_base()
        liste_produit = entite.liste_produits(conn)
        conn.close()
        return render_template("/categorie/produits.html", produits=liste_produit)
    conn = get_conn()
    liste_produit = entite.liste_produits(conn)
    conn.close()
    return render_template("/categorie/produits.html", produits=liste_produit)
    

@app.route("/clients/ajouter",methods = ['POST'])
def ajouter_client():
    nom = request.form["nom"]
    prenom = request.form["prenom"]
    adresse = request.form["adresse"]
    conn = get_conn()
    client = entite.Clients(conn, nom, prenom, adresse)
    client.ajouter_en_base()
    conn.close()
    return redirect("/clients")

@app.route("/produits/modifier", methods=["GET", "POST"])
def modifier_produit():
    conn = get_conn()
    if request.method == "POST":
        produit_id = int(request.form["id"])
        prix = float(request.form["prix"])
        nom = request.form["nom"]
        type_prod = request.form["type_prod"]
        prix_promo = request.form.get('prix_promo')
        if prix_promo:
            prix_promo = float(prix_promo)
        else:
            prix_promo = None
        descrip = request.form.get('descrip',None)
        entite.Produit.modifier(conn,nom,type_prod,prix,prix_promo,descrip,produit_id)
        liste_produit = entite.liste_produits(conn)
        conn.close()
        return render_template('/categorie/produits.html',produits=liste_produit)
    produit_id = request.args.get('id')
    if produit_id is None:
        message = {"message":"identifiant introuvable"}
        return (jsonify(message),404)
    produit = entite.Produit.recuperer_par_id(conn,produit_id)
    conn.close()
    return render_template('/admin/produits_modifier.html',produit= produit)

@app.route('/produits/supprimer',methods= ['POST'])
def supprimer_produit():
    produits_id = id_depuis_requete(request.args, "id")
    if produits_id is None:
        return (jsonify({"message": "Identifiant de produit invalide."}), 400)
    conn = get_conn()
    entite.Produit.supprimer(conn, produits_id)
    liste_produit = entite.liste_produits(conn)
    conn.close()
    return render_template("/categorie/produits.html",produits = liste_produit)

@app.route("/clients/modifier", methods=["GET", "POST"])
def modifier_client():
    conn = get_conn()
    if request.method == "POST":
        client_id = id_depuis_requete(request.form, "clients_id")
        if client_id is None:
            return (jsonify({"message": "Identifiant de client invalide."}), 400)
        erreur = _sauvegarder_client(conn, client_id, request.form)
        if erreur:
            return erreur
        liste_client = entite.liste_clients(conn)
        conn.close()
        return render_template("/categorie/clients.html", clients = liste_client)
    client_id = id_depuis_requete(request.args, 'id')
    if client_id is None:
        return (jsonify({"message": "Identifiant de client invalide."}), 400)
    liste_client = entite.Clients.recuperer_par_id(conn,client_id)
    conn.close()
    return render_template("/admin/clients_modifier.html", client=liste_client)

@app.route("/clients/supprimer", methods=["GET", "POST"])
def supprimer_client():
    conn = get_conn()
    if request.method == "POST":
        client_id = id_depuis_requete(request.form, "clients_id")
        if client_id is None:
            return (jsonify({"message": "Identifiant de client invalide."}), 400)
        entite.Clients.supprimer(conn, client_id)
        conn.close()
        return render_template("/categorie/clients.html")
    liste_client = entite.liste_clients(conn)
    conn.close()
    return render_template("/categorie/clients.html", clients=liste_client)

@app.route("/commandes/ajouter",methods = ['POST'])
# Convertit les lignes de formulaire en détails de commande en conservant le prix promotionnel lorsqu'il existe.
def ajouter_commande():
    clients_id = int(request.form["clients_id"])
    date_comm = request.form["date_comm"]
    produits_ids = request.form.getlist("produits_id[]")
    quantites = request.form.getlist("quantite[]")
    conn = get_conn()
    cur = conn.cursor()
    liste_produits = []
    for produits_id, quantite in zip(produits_ids, quantites):
        cur.execute("select prix,prix_promo from produits where produits_id = ?;", (produits_id,))
        resultat = cur.fetchone()
        prix_unitaire = resultat[0]
        prix_promo = resultat[1]
        prix_final = prix_promo if prix_promo is not None else prix_unitaire
        liste_produits.append((int(produits_id), int(quantite), prix_final))
    commande = entite.Commandes(conn, date_comm, clients_id, liste_produits)
    commande.ajouter_en_base()
    conn.close()
    return redirect("/commandes")

@app.route("/commandes/modifier", methods=["GET", "POST"])
# Reconstruit les lignes d'une commande lors d'une modification afin de recalculer les prix réellement appliqués.
def modifier_commande():
    conn = get_conn()
    cur = conn.cursor()
    if request.method == "POST":
        comm_id = int(request.form["id"])
        date_comm = request.form["date_comm"]
        clients_id = int(request.form["clients_id"])
        produits_ids = request.form.getlist("produits_id[]")
        quantites = request.form.getlist("quantite[]")
        cur.execute("delete from details_comm where commandes_id = ?",(comm_id,))
        conn.commit()
        entite.Commandes.modifier(conn, date_comm, clients_id,comm_id)
        liste_produits = []
        for identifiant, quantite in zip(produits_ids, quantites):
            cur.execute("select prix,prix_promo from produits where produits_id = ?;", (identifiant,))
            resultat = cur.fetchone()
            prix_unitaire = resultat[0]
            prix_promo = resultat[1]
            prix_final = prix_promo if prix_promo is not None else prix_unitaire
            liste_produits.append((int(identifiant), int(quantite), prix_final))
        for produit_id, quantite, prix in liste_produits:
            cur.execute("INSERT INTO details_comm(quantite,prix_unitaire,commandes_id,produits_id) values(?,?,?,?);",
            (quantite, prix, comm_id, produit_id)) 
        liste_commande = entite.commandes_groupees(conn)   
        conn.commit()
        conn.close()
        return render_template("/categorie/commandes.html",commandes = liste_commande)
    comm_id = id_depuis_requete(request.args, 'id')
    if comm_id is None:
        return (jsonify({"message": "Identifiant de commande invalide."}), 400)
    toutes_comm = entite.commandes_groupees(conn)
    try:
        comm_cible = toutes_comm[comm_id]
    except KeyError:
        return (jsonify({"message": "Commande introuvable."}), 404)
    conn.close()
    return render_template("/admin/commandes_modifier.html", commandes=comm_cible, commande_id=comm_id)

@app.route("/commandes/supprimer", methods=["POST"])
def supprimer_commande():
    id_commande = id_depuis_requete(request.args, "id")
    if id_commande is None:
        return (jsonify({"message": "Identifiant de commande invalide."}), 400)
    conn = get_conn()
    entite.Commandes.supprimer(conn, id_commande)
    conn.close()
    return redirect("/commandes")



#routes utilisées pour les 2 parties du site (admin et shop)
@app.route("/produits")
def produits():
    conn = get_conn()
    liste_produit = entite.liste_produits(conn)
    conn.close()
    return render_template("/categorie/produits.html", produits=liste_produit)

@app.route("/clients")
def clients():
    conn = get_conn()
    liste_client = entite.liste_clients(conn)
    conn.close()
    return render_template("/categorie/clients.html", clients=liste_client)

@app.route("/commandes")
def commandes():
    conn = get_conn()
    liste_commande = entite.commandes_groupees(conn)
    conn.close()
    return render_template("/categorie/commandes.html", commandes=liste_commande)


#routes utilisées pour la partie shop

@app.route("/shop")
def shop():
    conn = get_conn()
    produits_bruts = entite.liste_produits(conn)
    produits = entite.enrichir_produits(produits_bruts)
    panier = session.get('panier',[])
    long_panier = len(panier)
    return render_template('/shop/shop.html', produits=produits,long_panier=long_panier)



@app.route('/ajouter_panier', methods=['POST'])
# Ajoute ou cumule un produit dans le panier de session en mémorisant le prix applicable au moment de l'ajout.
def ajouter_panier():
    data = request.get_json()
    id_produit = data['id_produit']
    quantite_ajoutee = data['quantite']
    if not isinstance(quantite_ajoutee, int) or quantite_ajoutee <= 0:
        return (jsonify({"message": "Quantité invalide."}), 400)
    conn = get_conn() 
    produit = entite.Produit.recuperer_prix_par_id(conn, id_produit)
    if produit is None:
        message = jsonify({
            "message" : "Identifiant de produit invalide"
            })
        return (message,400)
    else:
        prix_final = produit[1] if produit[1] is not None else produit[0]
        if 'panier' not in session:
            session['panier'] = {id_produit: {'quantite': quantite_ajoutee, 'prix': prix_final}} 
        else:
            if id_produit in session['panier']:
                session['panier'][id_produit]['quantite'] += quantite_ajoutee
                session.modified = True
            else:
                session['panier'][id_produit] = {'quantite': quantite_ajoutee, 'prix': prix_final}
                session.modified = True
    retour = jsonify({
            "message" : "Produit ajouté au panier avec succès",
            "quantite" : len(session['panier'])
            })
    return (retour,200)



@app.route('/shop_vitrine', methods=['GET'])
# Choisit des recommandations personnalisées après achat, ou le classement global pour un visiteur sans historique.
def vitrine_produit():
    conn = get_conn()
    cur = conn.cursor()
    client_id = session.get('id_client')
    a_des_achats = False
    if client_id:
        resultat = cur.execute(
            "SELECT 1 FROM commandes WHERE clients_id = ? LIMIT 1",
            (client_id,)
        ).fetchone()
        a_des_achats = resultat is not None
    if a_des_achats:
        similarites, ids = content_based.calculer_similarites(conn)
        recommandation_brute = content_based.recommandations_par_historique(
            client_id, conn, similarites, ids, k=8
        )
        similarites_collab, ids_collab = collaborative.calculer_similarites_collab(conn)
        recommandation_collab_brute = collaborative.recommandations_collaboratives(
            client_id, conn, similarites_collab, ids_collab, k=8
        )
    else:
        recommandation_brute = entite.top_k_baseline(conn, k=8)
        recommandation_collab_brute = []

    recommandation = entite.enrichir_produits(recommandation_brute)
    recommandation_collab = entite.enrichir_produits(recommandation_collab_brute)
    produits_bruts = entite.liste_produits(conn)
    produits = entite.enrichir_produits(produits_bruts)
    produits = random.sample(produits, min(20, len(produits)))
    conn.close()
    return render_template(
        "shop/shop_produits.html",
        produits=produits,
        recommandation=recommandation,
        recommandation_collab=recommandation_collab,
        a_des_achats=a_des_achats
    )



@app.route('/shop_produit', methods=['GET'])
def voir_catalogue():
    categorie = request.args.get('categorie')
    texte = request.args.get('recherche')
    promo = request.args.get('promo')
    conn = get_conn()
    produits_bruts = entite.liste_produits(conn)
    produits = entite.enrichir_produits(produits_bruts)
    if categorie is not None:
        produits = [p for p in produits if p['type'] == categorie]
    if texte is not None:
        produits = [p for p in produits if texte.lower() in p['nom'].lower()]
    if promo == 'true':
        produits = [p for p in produits if p['prix_promo'] is not None]
    conn.close()
    return render_template("shop/shop_produits.html", produits=produits)


@app.route('/shop_contact',methods=['GET'])
def voir_contact():
    return render_template("shop/contact.html")



@app.route('/shop_panier', methods=['GET'])
# Recompose le panier depuis la session, calcule ses sous-totaux et propose des articles similaires au dernier produit ajouté.
def afficher_panier():
    conn = get_conn()
    cur = conn.cursor()
    panier = session.get('panier', {})
    ids_produits = list(panier.keys())
    if ids_produits == []:
        liste_flask = []
    else:
        placeholders = ",".join(["?"] * len(ids_produits))
        requete = f"SELECT * FROM produits WHERE produits_id IN ({placeholders})"
        cur.execute(requete, ids_produits)
        liste_sql = cur.fetchall()
        liste_flask = []
        for p in liste_sql:
            id_str = str(p[0])
            prix_unitaire = p[4] if p[4] is not None else p[2]
            quantite = panier[id_str]['quantite']
            liste_flask.append({
                "id": p[0],
                "nom": p[1],
                "type": p[3],
                "prix": prix_unitaire,
                "quantite": quantite,
                "sous_total": prix_unitaire * quantite,
            })
    total = sum([p['sous_total'] for p in liste_flask])
    produits_similaires_liste = []
    if ids_produits:
        dernier_id = int(ids_produits[-1])
        similarites, ids = content_based.calculer_similarites(conn)
        ids_recommandes = content_based.produits_similaires(dernier_id, similarites, ids, k=5)

        placeholders_reco = ",".join(["?"] * len(ids_recommandes))
        cur.execute(
            f"SELECT produits_id, nom, prix, type_prod, prix_promo FROM produits WHERE produits_id IN ({placeholders_reco})",
            ids_recommandes
        )
        produits_similaires_liste = entite.enrichir_produits(cur.fetchall())
    conn.close()
    return render_template(
        'shop/shop_panier.html',
        produits=liste_flask,
        total=total,
        produits_similaires=produits_similaires_liste
    )



@app.route('/supprimer_panier', methods=['POST'])
def supprimer_produit_panier():
    id_produit = request.args.get('id')
    session['panier'].pop(id_produit,None)
    session.modified = True
    return (jsonify({"message": "Produit supprimé du panier"}), 200)



@app.route('/modifier_panier', methods=['POST'])
def modifier_panier():
    data = request.get_json()
    id_produit = data['id_produit']
    quantite_ajoutee = data['quantite']
    if not isinstance(quantite_ajoutee, int) or quantite_ajoutee <= 0:
        return (jsonify({"message": "Quantité invalide."}), 400)
    if id_produit in session['panier']:
        session['panier'][id_produit]['quantite'] = quantite_ajoutee
        session.modified = True
        prix = session['panier'][id_produit]['prix']
        nouveau_sous_total = prix * quantite_ajoutee
        message = jsonify({
            "message": "La quantité du produit a été modifiée.",
            "sous_total": nouveau_sous_total
        })
        return (message, 200)
    else:
        message = jsonify({
            "message": "Identifiant de produit invalide"
        })
        return (message, 400)


 

@app.route('/valider_commande',methods=['POST'])
# Transforme le panier de session en commande et en lignes de détail, puis réinitialise le panier après enregistrement.
def valider_commande():
    panier = session.get('panier',{})
    if 'id_client' not in session:
        return (jsonify({"message": "Vous devez être connecté pour valider votre commande."}), 401)
    id_client = session['id_client']
    date_jour = date.today()
    conn = get_conn()
    cur = conn.cursor()
    if panier == {}:
        message = jsonify({
            "message": "Erreur panier vide."
        })
        return (message, 400)
    cur.execute("INSERT INTO commandes(clients_id,date_comm) values(?,?);",(id_client,date_jour))
    conn.commit()
    id_commande = cur.lastrowid
    for produit_id,details in panier.items():
        cur.execute("INSERT INTO details_comm(quantite,prix_unitaire,commandes_id,produits_id) values(?,?,?,?);",(details['quantite'],details['prix'],id_commande,int(produit_id)))
    conn.commit()
    conn.close()
    session['panier'] = {}
    session.modified = True
    message = jsonify({
            "message": "Commande enregistré.",
            "commande_id":id_commande
        })
    recalculer_taux_vente(conn,30)
    return (message, 200)



#routes pour la connexion/inscription du client
@app.route('/inscription',methods=['GET','POST'])
def inscription():
    if request.method == 'POST':
        data = request.get_json()
        conn = get_conn()
        nom = data.get('nom')
        prenom = data.get('prenom')
        email = data.get('email')
        mdp = data.get('mdp')
        adresse = data.get('adresse')
        liste_requise = [nom,prenom,email,mdp]
        for i in liste_requise:
            if i is None:
                return (jsonify({"message": "Champ manquant"}), 400)
        client_session = entite.Clients(conn,nom,prenom,email,mdp,adresse)
        message = client_session.ajouter_en_base()
        conn.close()
        return message
    return render_template('/shop/inscription.html')    



@app.route('/connexion',methods=['POST'])
def connexion():
    data = request.get_json()
    conn = get_conn()
    email = data.get('email')
    mdp = data.get('mdp')
    liste_requise = [email,mdp]
    for i in liste_requise:
        if i is None:
            return (jsonify({"message": "Champ manquant"}), 400)
    login,code = entite.Clients.connexion(conn,email,mdp)
    conn.close()
    if code == 200:
        id_client = login["id"]
        session.pop("admin",None)
        session['id_client'] = id_client
        return (jsonify({"message":"connexion réussie"}),200)
    else:
        return (login,code)   
    

@app.route('/admin_connexion', methods=['GET','POST'])
def admin_connexion():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        mdp = data.get('mdp')
        if email == ADMIN_EMAIL and check_password_hash(ADMIN_MDP_HASH, mdp):
            session.pop("id_client", None)
            session['admin_connecte'] = True
            return (jsonify({"message": "Connexion admin réussie."}), 200)
        else:
            return (jsonify({"message": "Email ou mot de passe incorrect."}), 400)
    return render_template('/admin/admin_login.html')



@app.route('/',methods=['GET'])
def portail_login():
    if 'id_client' in session:
        return redirect('/shop')
    else:
        return render_template('/shop/connexion.html')
    

@app.route('/profil',methods = ['GET'])
def voir_profil():
    if 'id_client' not in session:
        return redirect('/')
    conn = get_conn()
    client_id = int(session['id_client'])
    client = entite.Clients.recuperer_par_id(conn,client_id)
    commandes_client = entite.commandes_groupees(conn,client_id)
    return render_template('/shop/profil.html',client = client,commandes = commandes_client)


@app.before_request
# Protège les routes d'administration en redirigeant toute requête non authentifiée vers la page de connexion admin.
def verif_admin():
    liste_route = ["/admin","/produits","/produits/modifier","/produits/supprimer","/clients","/clients/modifier",
            "/clients/supprimer","/commandes","/commandes/ajouter","/commandes/modifier","/commandes/supprimer",
            "/produits/ajouter","/clients/ajouter"]
    for route in liste_route:
        if request.path == route:
            if 'admin_connecte' in session:
                return None
            else:
                return redirect('/admin_connexion')
    return None
    

@app.route("/profil/modifier", methods=["GET", "POST"])
def modifier_profil():
    conn = get_conn()
    if request.method == "POST":
        if 'id_client' not in session:
            return jsonify({"message": "Session expirée, veuillez vous reconnecter."}), 401
        profil_id = int(session["id_client"])
        erreur = _sauvegarder_client(conn, profil_id, request.form)
        if erreur:
            return erreur
        conn.close()
        return jsonify({"message": "Profil mis à jour."}), 200
    if 'id_client' not in session:
        return redirect('/')
    return jsonify({"connecte": True})



@app.route('/confirmation_commande',methods = ['GET'])
# Vérifie que la commande demandée existe et appartient bien au client connecté avant d'afficher sa confirmation.
def confirm_comm():
    conn = get_conn()
    id_param = request.args.get('id')
    if id_param is None:
        return (jsonify({"message": "Identifiant de commande manquant."}), 400)
    comm_id = int(id_param)
    toutes_comm = entite.commandes_groupees(conn)
    try:
        comm_cible = toutes_comm[comm_id]
    except KeyError:
        return (jsonify({"message": "Commande introuvable."}), 404)
    if 'id_client' not in session:
        return redirect('/')
    if comm_cible['client_id'] != session['id_client']:
        message = jsonify({"message":"numero de commande invalide"})
        return(message,400)
    conn.close()
    return render_template("/shop/confirmation_commande.html", commandes=comm_cible, commande_id=comm_id)



@app.route("/contact", methods=["POST"])
def envoyer_mail():
    email = request.form["email"]
    message = request.form["message"]

    return jsonify({"message": "Message envoyé"})


@app.route('/log_out',methods = ['GET'])
def log_out():
    session.pop('id_client', None)
    return redirect ('/')

if __name__ == "__main__":
    app.run(debug=True)
