import sqlite3

conn = sqlite3.connect("boutique.db")
conn.execute("PRAGMA foreign_keys = ON;")
cur = conn.cursor()

produits = [
    ("Riz (sac 25kg)", 250000, "Alimentaire"),
    ("Huile végétale (5L)", 85000, "Alimentaire"),
    ("Sucre (1kg)", 12000, "Alimentaire"),
    ("Farine de blé (1kg)", 9000, "Alimentaire"),
    ("Lait en poudre (400g)", 25000, "Alimentaire"),
    ("Pâtes alimentaires (500g)", 8000, "Alimentaire"),
    ("Tomate concentrée (boîte)", 5000, "Alimentaire"),
    ("Savon de Marseille", 3000, "Hygiène"),
    ("Dentifrice", 15000, "Hygiène"),
    ("Shampoing (250ml)", 22000, "Hygiène"),
    ("Papier hygiénique (pack 4)", 18000, "Hygiène"),
    ("Gel douche (500ml)", 30000, "Hygiène"),
    ("Cahier 100 pages", 5000, "Papeterie"),
    ("Stylo bic (unité)", 1500, "Papeterie"),
    ("Clé USB 32GB", 45000, "Électronique"),
    ("Ampoule LED", 12000, "Électronique"),
    ("Pile AA (paquet de 4)", 10000, "Électronique"),
    ("Eau minérale (1.5L)", 5000, "Boisson"),
    ("Jus de fruit (1L)", 15000, "Boisson"),
    ("Café soluble (100g)", 20000, "Boisson"),
]

cur.executemany(
    "INSERT INTO produits (nom, prix, type_prod) VALUES (?, ?, ?)",
    produits
)

conn.commit()
print(f"{len(produits)} produits insérés.")

clients = [
    ("Diallo", "Ibrahima Sory", "Ratoma, Conakry"),
    ("Bah", "Fatoumata", "Kaloum, Conakry"),
    ("Camara", "Mohamed", "Kindia"),
    ("Barry", "Aissatou", "Dixinn, Conakry"),
    ("Sylla", "Mamadou", "Kankan"),
    ("Conde", "Hadja Djénabou", "Matam, Conakry"),
    ("Toure", "Alpha Oumar", "Labé"),
    ("Keita", "Mariama", "Ratoma, Conakry"),
    ("Sow", "Ousmane", "Nzérékoré"),
    ("Cissé", "Kadiatou", "Kaloum, Conakry"),
    ("Bangoura", "Sékou", "Boké"),
    ("Fofana", "Aminata", "Kissidougou"),
    ("Diakite", "Lansana", "Ratoma, Conakry"),
    ("Soumah", "Binta", "Coyah"),
    ("Kourouma", "Alseny", "Faranah"),
]

cur.executemany(
    "INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",
    clients
)

conn.commit()
print(f"{len(clients)} clients insérés.")
conn.close()
