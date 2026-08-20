import sqlite3
import entite
import pandas as pd
from datetime import datetime

conn = sqlite3.connect("boutique.db")
conn.execute("PRAGMA foreign_keys = ON;")
cur = conn.cursor()


def sous_menu(choix):
    print(f"1. Voir le catalogue complet({choix})")
    print(f"2. Ajouter un {choix}")
    print(f"3. Modifier le {choix}")
    print(f"4. Supprimer un {choix} ")
    print("5. Retour au menu principal")


def demander_entier(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Veuillez entrer un entier valide")


def demander_date(message):
    while True:
        try:
            return datetime.strptime(input(message), "%Y-%m-%d")
        except ValueError:
            print("format invalide")


def vers_dataframe(cur, view):
    col = [description[0] for description in cur.description]
    df = pd.DataFrame(view, columns=col)
    return df


while True:
    print("--------------gestionnaire de boutique SQL---------------")
    print("1. Gérer les produits")
    print("2. Gérer les clients")
    print("3. Gérer les commandes")
    print("4. Quitter le programme")
    choix_accueil = demander_entier("Votre choix : ")
    if choix_accueil == 4:
        break
    elif choix_accueil == 1:
        sous_menu("produit")
        choix_prod = demander_entier("Votre choix : ")
        if choix_prod == 1:
            cur.execute("select * from produits;")
            view = cur.fetchall()
            if view != []:
                df = vers_dataframe(cur, view)
                print(df)
            else:
                print("Aucun produit enregistré")
        if choix_prod == 2:
            nom = input("Quelle est le nom du produit ?")
            prix = demander_entier("Quel prix attribuer vous au produit ?")
            type_prod = input("Votre produit est de quel type ?(vêtements,accessoire,cosmétique,etc...)")
            produit = entite.Produit(conn, nom, prix, type_prod)
            produit.ajouter_en_base()
        elif choix_prod == 3:
            cur.execute("select * from produits;")
            view = cur.fetchall()
            if view != []:
                df = vers_dataframe(cur, view)
                print(df)
                cible = demander_entier("Quel produit voulez vous modifier ?(Entrer son id ) : ")
                cur.execute("select produits_id from produits where produits_id = ?;", (cible,))
                resultat = cur.fetchone()
                if resultat is not None:
                    nv_prix = demander_entier("Entrer le nouveau prix : ")
                    entite.Produit.modifier_prix(conn, nv_prix, cible)
                    print("Le prix a été modifié avec succès")
                else:
                    print("L'id correspondant n'a pas été trouvé")
            else:
                print("Aucun produit n'existe,veuillez créer un produit ")

        elif choix_prod == 4:
            cur.execute("select * from produits;")
            view = cur.fetchall()
            if view != []:
                df = vers_dataframe(cur, view)
                print(df)
                cible = demander_entier("Quel produit voulez vous supprimer ?(Entrer son id ) : ")
                cur.execute("select produits_id from produits where produits_id = ?;", (cible,))
                resultat = cur.fetchone()
                if resultat is not None:
                    entite.Produit.supprimer(conn, cible)
                    print("Le produit a été supprimé avec succès")
                else:
                    print("L'id correspondant n'a pas été trouvé")
            else:
                print("Aucun produit n'existe,veuillez créer un produit ")
    elif choix_accueil == 2:
        sous_menu("client")
        choix_client = demander_entier("Votre choix : ")
        if choix_client == 1:
            cur.execute("select * from clients;")
            view = cur.fetchall()
            if view != []:
                df = vers_dataframe(cur, view)
                print(df)
            else:
                print("Aucun clients enregistré")
        if choix_client == 2:
            nom = input("Quelle est le nom du client ?(nom de famille) :")
            prenom = input("Quel est le prenom du client  ?")
            adresse = input("Quel est l'adresse du client ?(optionel)")
            client = entite.Clients(conn, nom, prenom, adresse)
            client.ajouter_en_base()
        elif choix_client == 3:
            cur.execute("select * from clients;")
            view = cur.fetchall()
            if view != []:
                df = vers_dataframe(cur, view)
                print(df)
                cible = demander_entier("Quel client voulez vous modifier ?(Entrer son id ) : ")
                cur.execute("select clients_id from clients where clients_id = ?;", (cible,))
                resultat = cur.fetchone()
                if resultat is not None:
                    nom = input("Quelle est le nom du client ?(nom de famille)")
                    prenom = input("Quel est le prenom du client  ?")
                    adresse = input("Quel est l'adresse du client ?(optionel)")
                    entite.Clients.modifier_client(conn, nom, prenom, adresse, cible)
                else:
                    print("L'id correspondant n'a pas été trouvé")
            else:
                print("Aucun client n'existe,veuillez créer un client ")
        elif choix_client == 4:
            cur.execute("select * from clients;")
            view = cur.fetchall()
            if view != []:
                df = vers_dataframe(cur, view)
                print(df)
                cible = demander_entier("Quel clients voulez vous supprimer ?(Entrer son id ) : ")
                cur.execute("select clients_id from clients where clients_id = ?;", (cible,))
                resultat = cur.fetchone()
                if resultat is not None:
                    entite.Clients.supprimer(conn, cible)
                    print("Le client a été supprimé avec succès")
                else:
                    print("L'id correspondant n'a pas été trouvé")
            else:
                print("Aucun client n'existe,veuillez créer un client ")
    elif choix_accueil == 3:
        print("--- Gestion des commandes ---")
        print("1. Voir une commande")
        print("2. Ajouter une commande")
        print("3. Retour au menu principal")
        choix_comm = demander_entier("Votre choix : ")
        if choix_comm == 2:
            cur.execute("select * from clients;")
            view = cur.fetchall()
            if view != []:
                df = vers_dataframe(cur, view)
                print(df)
                clients_id = demander_entier("Id du client qui passe la commande : ")
                cur.execute("select clients_id from clients where clients_id = ?;", (clients_id,))
                resultat = cur.fetchone()
                if resultat is not None:
                    objet_date = demander_date("Date de la commande (AAAA-MM-JJ) : ")
                    date_comm = objet_date.strftime("%Y-%m-%d")
                    liste_produits = []
                    nb_produits = demander_entier("Combien de produits dans cette commande ? ")
                    for i in range(nb_produits):
                        while True:
                            # Requête "produits" affichée : on lit description
                            # juste après cet execute, avant le execute suivant.
                            cur.execute("select * from produits;")
                            view_produits = cur.fetchall()
                            df_produits = vers_dataframe(cur, view_produits)
                            print(df_produits)
                            produits_id = demander_entier("Id du produit : ")
                            cur.execute("select prix from produits where produits_id = ?;", (produits_id,))
                            resultat_prix = cur.fetchone()
                            if resultat_prix is not None:
                                break
                            else:
                                print("Produit introuvable, réessayez")
                        prix_unitaire = resultat_prix[0]
                        quantite = demander_entier("Quantité : ")
                        liste_produits.append((produits_id, quantite, prix_unitaire))
                    commande = entite.Commandes(conn, date_comm, clients_id, liste_produits)
                    commande.ajouter_en_base()
                    print("La commande a été enregistrée avec succès")
                else:
                    print("L'id correspondant n'a pas été trouvé")
            else:
                print("Aucun client n'existe, veuillez créer un client")
        elif choix_comm == 1:
            cur.execute("select * from commandes;")
            view = cur.fetchall()
            if view != []:
                df = vers_dataframe(cur, view)
                print(df)
                commandes_id = demander_entier("Id de la commande à afficher : ")
                view,cur_commande = entite.Commandes.afficher(conn, commandes_id)
                if view != []:
                    df = vers_dataframe(cur_commande,view)
                    print(df)
                else:
                    print('commande inexistante')
            else:
                print("Aucune commande existante ")
    else:
        print("choix invalide")