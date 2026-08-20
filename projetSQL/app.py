from flask import Flask, render_template, request ,redirect
import sqlite3
import entite
from werkzeug.security import generate_password_hash, check_password_hash

ADMIN_EMAIL = "admin@boutique.com"
ADMIN_MDP_HASH = generate_password_hash("ibra")
app = Flask(__name__)
app.secret_key = "dev_secret_key_2026"   

def get_conn():
    conn = sqlite3.connect("boutique.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

#page de l'admin et ses routes
@app.route("/admin")
def accueil_admin():
    conn = get_conn()
    stats = entite.get_stats(conn)
    produits_top = entite.produits_les_plus_achetes(conn)
    conn.close()
    noms_produits = [p[0] for p in produits_top]
    quantites = [p[1] for p in produits_top]
    return render_template("/admin/main.html", stats=stats,noms_produits=noms_produits, quantites=quantites)

@app.post("/produits/ajouter")
def ajouter_produit():
    nom = request.form["nom"]
    prix = float(request.form["prix"])
    type_prod = request.form["type_prod"]
    conn = get_conn()
    produit = entite.Produit(conn, nom, prix, type_prod)
    produit.ajouter_en_base()
    conn.close()
    return redirect("/produits")

@app.post("/clients/ajouter")
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
        id = int(request.form["produits_id"])
        prix = float(request.form["prix"])
        entite.Produit.modifier_prix(conn, prix, id)
        conn.close()
        return redirect("/produits")
    liste = entite.liste_produits(conn)
    conn.close()
def supprimer_produit():
    conn = get_conn()
    if request.method == "POST": 
        id = int(request.form["produits_id"])
        entite.Produit.supprimer(conn, id)
        conn.close()
        return redirect("/produits")
    liste = entite.liste_produits(conn)
    conn.close()
    return render_template("/categorie/produits_supprimer.html", produits=liste)

@app.route("/clients/modifier", methods=["GET", "POST"])
def modifier_client():
    conn = get_conn()
    if request.method == "POST":
        id = int(request.form["clients_id"])
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        adresse = request.form["adresse"]
        entite.Clients.modifier_client(conn, nom, prenom, adresse, id)
        conn.close()
        return redirect("/clients")
    liste = entite.liste_clients(conn)
    conn.close()
    return render_template("/categorie/clients_modifier.html", clients=liste)

@app.route("/clients/supprimer", methods=["GET", "POST"])
def supprimer_client():
    conn = get_conn()
    if request.method == "POST":
        id = int(request.form["clients_id"])
        entite.Clients.supprimer(conn, id)
        conn.close()
        return redirect("/clients")
    liste = entite.liste_clients(conn)
    conn.close()
    return render_template("/categorie/clients_supprimer.html", clients=liste)

@app.post("/commandes/ajouter")
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
        for id, quantite in zip(produits_ids, quantites):
            cur.execute("select prix,prix_promo from produits where produits_id = ?;", (id,))
            resultat = cur.fetchone()
            prix_unitaire = resultat[0]
            prix_promo = resultat[1]
            prix_final = prix_promo if prix_promo is not None else prix_unitaire
            liste_produits.append((int(id), int(quantite), prix_final))
        for produit_id, quantite, prix in liste_produits:
            cur.execute("INSERT INTO details_comm(quantite,prix_unitaire,commandes_id,produits_id) values(?,?,?,?);",
            (quantite, prix, comm_id, produit_id))    
        conn.commit()
        conn.close()
        return redirect("/commandes")
    id_param = request.args.get('id')
    if id_param is None:
        return (jsonify({"message": "Identifiant de commande manquant."}), 400)
    comm_id = int(id_param)
    toutes_comm = entite.commandes_groupees(conn)
    try:
        comm_cible = toutes_comm[comm_id]
    except KeyError:
        return (jsonify({"message": "Commande introuvable."}), 404)
    conn.close()
    return render_template("/admin/commandes_modifier.html", commandes=comm_cible, commande_id=comm_id)

@app.route("/commandes/supprimer", methods=["GET", "POST"])
def supprimer_commande():
    conn = get_conn()
    if request.method == "POST":
        id = int(request.form["commandes_id"])
        entite.Commandes.supprimer(conn, id)
        conn.close()
        return redirect("/commandes")
    liste = entite.liste_commandes(conn)
    conn.close()
    return render_template("/categorie/commandes_supprimer.html", commandes=liste)



#routes utilisées pour les 2 parties du site (admin et shop)
@app.route("/produits")
def produits():
    conn = get_conn()
    liste = entite.liste_produits(conn)
    conn.close()
    return render_template("/categorie/produits.html", produits=liste)

@app.route("/clients")
def clients():
    conn = get_conn()
    liste = entite.liste_clients(conn)
    conn.close()
    return render_template("/categorie/clients.html", clients=liste)

@app.route("/commandes")
def commandes():
    conn = get_conn()
    liste = entite.commandes_groupees(conn)
    conn.close()
    return render_template("/categorie/commandes.html", commandes=liste)


#routes utilisées pour la partie shop
from flask import session
@app.route("/shop")
def shop():

    conn = get_conn()
    produits_bruts = entite.liste_produits(conn)
    produits = entite.enrichir_produits(produits_bruts)
    panier = session.get('panier',[])
    long_panier = len(panier)
    return render_template('/shop/shop.html', produits=produits,long_panier=long_panier)


from flask import jsonify
@app.route('/ajouter_panier', methods=['POST'])
def ajouter_panier():
    data = request.get_json()
    id_produit = data['id_produit']
    quantite_ajoutee = data['quantite']
    conn = get_conn() 
    produit = entite.Produit.recuperer_prix_par_id(conn, id_produit)
    if produit is None:
        message = jsonify({
            "message" : "Identifiant de produit invalide"
            })
        return (message,400)
    else:
        if 'panier' not in session:
            session['panier'] = {id_produit: {'quantite': quantite_ajoutee, 'prix': produit[0]}} 
        else:
            if id_produit in session['panier']:
                session['panier'][id_produit]['quantite'] += quantite_ajoutee
                session.modified = True
            else:
                session['panier'][id_produit] = {'quantite': quantite_ajoutee, 'prix': produit[0]}
                session.modified = True
    retour = jsonify({
            "message" : "Produit ajouté au panier avec succès",
            "quantite" : len(session['panier'])
            })
    return (retour,200)


import random
@app.route('/shop_vitrine',methods=['GET'])
def vitrine_produit():
    conn = get_conn()
    produits_bruts = entite.liste_produits(conn)
    produits = entite.enrichir_produits(produits_bruts)
    produits = random.sample(produits, 20)
    conn.close()
    return render_template("shop/shop_produits.html", produits=produits)



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
    conn.close()
    return render_template('shop/shop_panier.html', produits =liste_flask,total=total)



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


 
from datetime import date
@app.route('/valider_commande',methods=['POST'])
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
            "message": "Commande enregistré."
        })
    return (message, 200)



#routes pour la connexion/inscription du client
@app.route('/inscription',methods=['POST'])
def inscription():
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


@app.route('/inscription',methods = ['GET'])
def afficher_inscrip():
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
        session['id_client'] = id_client
        return (jsonify({"message":"connexion réussie"}),200)
    else:
        return (login,code)   
    

@app.route('/admin_connexion', methods=['POST'])
def admin_connexion():
    data = request.get_json()
    email = data.get('email')
    mdp = data.get('mdp')
    if email == ADMIN_EMAIL and check_password_hash(ADMIN_MDP_HASH, mdp):
        session['admin_connecte'] = True
        return (jsonify({"message": "Connexion admin réussie."}), 200)
    else:
        return (jsonify({"message": "Email ou mot de passe incorrect."}), 400)
    


@app.route('/admin_connexion',methods=['GET'])
def admin_login():
    return render_template('/admin/admin_login.html')


@app.route('/',methods=['GET'])
def portail_login():
    if 'id_client' in session:
        return redirect('/shop')
    else:
        return render_template('/shop/connexion.html')


@app.before_request
def verif_admin():
    liste = ["/admin","/produits","/produits/modifier","/produits/supprimer","/clients","/clients/modifier",
            "/clients/supprimer","/commandes","/commandes/ajouter","/commandes/modifier","/commandes/supprimer"]
    for route in liste:
        if request.path == route:
            if 'admin_connecte' in session:
                return None
            else:
                return redirect('/admin_connexion')
    return None
    

if __name__ == "__main__":
    app.run(debug=True)
