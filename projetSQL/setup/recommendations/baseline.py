# Calcule la part de ventes de chaque produit sur la période puis actualise les scores de recommandation globaux.
def recalculer_taux_vente(conn,plage_jours=30):
    cur = conn.cursor()
    quantite_par_produit = cur.execute("""
        SELECT
            d.produits_id,
            SUM(d.quantite) AS somme
        FROM details_comm AS d
        JOIN commandes AS c
            ON c.commandes_id = d.commandes_id
        WHERE c.date_comm >= date('now', ?)
        GROUP BY d.produits_id
        ORDER BY somme DESC;
    """, (f"-{plage_jours} days",)).fetchall()
    quantite_total = cur.execute("""
        SELECT SUM(d2.quantite)
        FROM details_comm AS d2
        JOIN commandes AS c2
            ON c2.commandes_id = d2.commandes_id
        WHERE c2.date_comm >= date('now', ?);
    """, (f"-{plage_jours} days",)).fetchone()[0]
    if quantite_total is None or quantite_total == 0:
        return
    score = {}
    for produit_id, revenu in quantite_par_produit:
        if revenu > 0:
            calcul_score = revenu / quantite_total
            score[produit_id] = {
                "score": calcul_score
            }
    for produit_id, donnees in score.items():
        cur.execute("""
            INSERT OR REPLACE INTO recommandations_produits
            (produits_id, score, plage_temps)
            VALUES (?, ?, ?)
        """, (
            produit_id,
            donnees["score"],
            plage_jours
        ))
    conn.commit()
    print("Recommandation appliqué.")
