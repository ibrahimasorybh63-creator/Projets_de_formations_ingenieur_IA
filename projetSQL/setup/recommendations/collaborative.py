import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Construit la matrice binaire produit x client (achat / non achat) à partir des commandes passées.
def matrice_produits_clients(conn):
    cur = conn.cursor()
    donnees = cur.execute("""
        SELECT DISTINCT d.produits_id, c.clients_id
        FROM details_comm AS d
        JOIN commandes AS c ON c.commandes_id = d.commandes_id
    """).fetchall()
    ids_produits = sorted({produit_id for produit_id, client_id in donnees})
    ids_clients = sorted({client_id for produit_id, client_id in donnees})
    index_produits = {pid: i for i, pid in enumerate(ids_produits)}
    index_clients = {cid: i for i, cid in enumerate(ids_clients)}
    matrice = np.zeros((len(ids_produits), len(ids_clients)))
    for produit_id, client_id in donnees:
        matrice[index_produits[produit_id], index_clients[client_id]] = 1
    return matrice, ids_produits, ids_clients


# Calcule la similarité cosinus entre chaque paire de produits à partir de leurs co-achats (item-based collaborative filtering).
def calculer_similarites_collab(conn):
    matrice, ids_produits, ids_clients = matrice_produits_clients(conn)
    similarites = cosine_similarity(matrice)
    return similarites, ids_produits


# Recommande des produits à un client à partir des produits co-achetés avec ceux de son historique, en excluant ce qu'il a déjà acheté.
def recommandations_collaboratives(client_id, conn, similarites, ids_produits, k=8):
    cur = conn.cursor()
    produits_achetes = cur.execute("""
        SELECT DISTINCT d.produits_id FROM details_comm AS d
        JOIN commandes AS c ON c.commandes_id = d.commandes_id
        WHERE c.clients_id = ?
    """, (client_id,)).fetchall()
    ids_achetes = [p[0] for p in produits_achetes if p[0] in ids_produits]
    if not ids_achetes:
        return []
    positions_achats = [ids_produits.index(pid) for pid in ids_achetes]
    lignes_achats = similarites[positions_achats]
    sim_max = np.max(lignes_achats, axis=0)
    ordre_trie = np.argsort(sim_max, descending=True)
    positions_valides = [pos for pos in ordre_trie if pos not in positions_achats]
    positions_finales = positions_valides[:k]
    produits_id = [ids_produits[pos] for pos in positions_finales]
    if not produits_id:
        return []
    placeholders = ",".join("?" for _ in produits_id)
    produits_bruts = cur.execute(
        f"SELECT * FROM produits WHERE produits_id IN ({placeholders})",
        produits_id
    ).fetchall()
    produits = sorted(produits_bruts, key=lambda p: produits_id.index(p[0]))
    return produits
