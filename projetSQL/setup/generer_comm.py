import random
from datetime import datetime, timedelta

# Génère un historique de commandes pondéré pour simuler des achats récents et anciens, avec des produits plus ou moins populaires.
def generer_commandes(conn):
    cur = conn.cursor()
    # On récupère les IDs
    cur.execute("SELECT clients_id FROM clients")
    clients = [ligne[0] for ligne in cur.fetchall()]
    cur.execute("""
        SELECT produits_id, prix, prix_promo
        FROM produits
    """)
    produits = cur.fetchall()
    # Pour avoir toujours les mêmes résultats
    random.seed(41)
    # Quelques produits volontairement très populaires
    produits_populaires = [
        1,   # Riz 25kg
        2,   # Huile 5L
        3,   # Sucre
        5,   # Lait
        6,   # Pâtes
        28,  # Oeufs
        70,  # Eau
        71,  # Jus
        72,  # Café
    ]
    # Produits moyennement populaires
    produits_moyens = [
        4, 7, 8, 9, 10,
        31, 32, 33, 35,
        49, 50, 51, 56,
        67, 68, 69,
        73, 74, 75, 76
    ]
    # Produits récupérables par ID
    prix_produits = {
        produit_id: prix_promo if prix_promo is not None else prix
        for produit_id, prix, prix_promo in produits
    }
    maintenant = datetime.now()
    commandes_generees = 0
    details_generes = 0


    for _ in range(70):
        client_id = random.choice(clients)
        jours_avant = random.randint(0, 29)
        date_commande = maintenant - timedelta(
            days=jours_avant,
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        cur.execute("""
            INSERT INTO commandes (date_comm, clients_id)
            VALUES (?, ?)
        """, (
            date_commande.strftime("%Y-%m-%d"),
            client_id
        ))
        commande_id = cur.lastrowid
        commandes_generees += 1
        nombre_produits = random.randint(1, 5)
        candidats = (
            random.choices(
                produits_populaires,
                k=nombre_produits
            )
            if random.random() < 0.65
            else random.sample(
                [p[0] for p in produits],
                nombre_produits
            )
        )
        candidats = list(set(candidats))
        for produit_id in candidats:
            quantite = random.randint(1, 5)
            prix_unitaire = prix_produits[produit_id]
            cur.execute("""
                INSERT INTO details_comm
                (quantite, prix_unitaire, commandes_id, produits_id)
                VALUES (?, ?, ?, ?)
            """, (
                quantite,
                prix_unitaire,
                commande_id,
                produit_id
            ))
            details_generes += 1
    for _ in range(15):
        client_id = random.choice(clients)
        jours_avant = random.randint(31, 90)
        date_commande = maintenant - timedelta(
            days=jours_avant
        )
        cur.execute("""
            INSERT INTO commandes (date_comm, clients_id)
            VALUES (?, ?)
        """, (
            date_commande.strftime("%Y-%m-%d"),
            client_id
        ))
        commande_id = cur.lastrowid
        commandes_generees += 1
        nombre_produits = random.randint(1, 4)
        candidats = random.sample(
            [p[0] for p in produits],
            nombre_produits
        )
        for produit_id in candidats:
            quantite = random.randint(1, 4)
            prix_unitaire = prix_produits[produit_id]
            cur.execute("""
                INSERT INTO details_comm
                (quantite, prix_unitaire, commandes_id, produits_id)
                VALUES (?, ?, ?, ?)
            """, (
                quantite,
                prix_unitaire,
                commande_id,
                produit_id
            ))
            details_generes += 1
    conn.commit()
    print(f"{commandes_generees} commandes générées.")
    print(f"{details_generes} lignes de détails générées.")
