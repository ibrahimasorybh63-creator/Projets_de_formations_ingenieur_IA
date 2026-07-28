from flask import Flask, render_template, request ,redirect
import sqlite3
import entite

app = Flask(__name__)

def get_conn():
    conn = sqlite3.connect("boutique.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@app.get("/")
def afficher_accueil():
    return render_template("main.html")

@app.route("/produits")
def produits():
    conn = get_conn()
    liste = entite.liste_produits(conn)
    conn.close()
    return render_template("produits.html", produits=liste)

@app.route("/clients")
def clients():
    conn = get_conn()
    liste = entite.liste_clients(conn)
    conn.close()
    return render_template("clients.html", clients=liste)

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
    return render_template("produits_modifier.html", produits=liste)

@app.route("/produits/supprimer", methods=["GET", "POST"])
def supprimer_produit():
    conn = get_conn()
    if request.method == "POST":
        id = int(request.form["produits_id"])
        entite.Produit.supprimer(conn, id)
        conn.close()
        return redirect("/produits")
    liste = entite.liste_produits(conn)
    conn.close()
    return render_template("produits_supprimer.html", produits=liste)

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
    return render_template("clients_modifier.html", clients=liste)

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
    return render_template("clients_supprimer.html", clients=liste)

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
        cur.execute("select prix from produits where produits_id = ?;", (produits_id,))
        resultat = cur.fetchone()
        prix_unitaire = resultat[0]
        liste_produits.append((int(produits_id), int(quantite), prix_unitaire))

    commande = entite.Commandes(conn, date_comm, clients_id, liste_produits)
    commande.ajouter_en_base()
    conn.close()
    return redirect("/produits")

@app.route("/commandes")
def commandes():
    conn = get_conn()
    liste = entite.commandes_groupees(conn)
    conn.close()
    return render_template("commandes.html", commandes=liste)

@app.route("/commandes/modifier", methods=["GET", "POST"])
def modifier_commande():
    conn = get_conn()
    if request.method == "POST":
        id = int(request.form["commandes_id"])
        date_comm = request.form["date_comm"]
        clients_id = int(request.form["clients_id"])
        entite.Commandes.modifier(conn, date_comm, clients_id, id)
        conn.close()
        return redirect("/commandes")
    liste = entite.liste_commandes(conn)
    conn.close()
    return render_template("commandes_modifier.html", commandes=liste)

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
    return render_template("commandes_supprimer.html", commandes=liste)

if __name__ == "__main__":
    app.run(debug=True)

