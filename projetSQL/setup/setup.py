from base import creer_base
from seed import remplir_base
from recommendations.baseline import recalculer_taux_vente
import sqlite3
conn = sqlite3.connect("boutique.db")
conn.execute("PRAGMA foreign_keys = ON;")
creer_base()
remplir_base()
recalculer_taux_vente(conn)
print("Opération de setup réussie.")