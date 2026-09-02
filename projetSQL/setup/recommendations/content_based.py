from sklearn.feature_extraction.text import TfidfVectorizer
from entite import descriptions_produits
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity

# Vectorise les descriptions des produits puis calcule une matrice de proximité cosinus entre chaque paire de produits.
def calculer_similarites(conn):
    vectorizer = TfidfVectorizer()
    donnees = descriptions_produits(conn)
    ids = [produit_id for produit_id, description in donnees]
    descriptions = [description for produit_id, description in donnees]
    matrice = vectorizer.fit_transform(descriptions)
    similarites = cosine_similarity(matrice)
    return similarites,ids


# Extrait les identifiants des produits les plus proches du produit courant, sans inclure ce produit lui-même.
def produits_similaires(produit_id, similarites, ids, k=5):
    index = ids.index(produit_id)
    ligne_sim = similarites[index]
    ligne_sim = np.argsort(ligne_sim,descending=True)
    ligne_sim = np.delete(ligne_sim,0)
    positions = ligne_sim[:k]
    produits_id = [ids[pos] for pos in positions]
    return produits_id


# Classe les produits non achetés selon leur meilleure similarité avec l'ensemble de l'historique du client.
def recommandations_par_historique(client_id, conn, similarites, ids, k=8):
    cur = conn.cursor()
    produits_achetes = cur.execute("""
        SELECT d.produits_id FROM details_comm AS d
        JOIN commandes AS c ON c.commandes_id = d.commandes_id
        JOIN clients AS cl ON cl.clients_id = c.clients_id
        WHERE cl.clients_id = ?
    """, (client_id,)).fetchall()
    positions_achats = [ids.index(p[0]) for p in produits_achetes]
    lignes_achats = similarites[positions_achats]
    sim_max = np.max(lignes_achats, axis=0)
    ordre_trie = np.argsort(sim_max, descending=True)
    positions_valides = [pos for pos in ordre_trie if pos not in positions_achats]
    positions_finales = positions_valides[:k]
    produits_id = [ids[pos] for pos in positions_finales]
    placeholders = ",".join("?" for _ in produits_id)
    produits_bruts = cur.execute(
        f"""
        SELECT *
        FROM produits
        WHERE produits_id IN ({placeholders})
        """,
        produits_id
    ).fetchall()
    produits = sorted(produits_bruts,key=lambda p: produits_id.index(p[0]))
    return produits
