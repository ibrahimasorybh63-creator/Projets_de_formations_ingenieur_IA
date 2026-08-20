import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("boutique.db")
conn.execute("PRAGMA foreign_keys = ON;")
cur = conn.cursor()

produits = [
    # --- Alimentaire ---
    ("Riz (sac 25kg)", 250000, "Alimentaire", None),
    ("Huile végétale (5L)", 85000, "Alimentaire", 75000),
    ("Sucre (1kg)", 12000, "Alimentaire", None),
    ("Farine de blé (1kg)", 9000, "Alimentaire", None),
    ("Lait en poudre (400g)", 25000, "Alimentaire", None),
    ("Pâtes alimentaires (500g)", 8000, "Alimentaire", None),
    ("Tomate concentrée (boîte)", 5000, "Alimentaire", None),
    ("Riz (sac 5kg)", 55000, "Alimentaire", None),
    ("Riz parfumé (sac 10kg)", 105000, "Alimentaire", 95000),
    ("Haricot rouge (1kg)", 15000, "Alimentaire", None),
    ("Maïs moulu (1kg)", 7000, "Alimentaire", None),
    ("Semoule de blé (1kg)", 10000, "Alimentaire", None),
    ("Oignons (filet 5kg)", 30000, "Alimentaire", None),
    ("Pomme de terre (5kg)", 35000, "Alimentaire", None),
    ("Ail (sachet 250g)", 8000, "Alimentaire", None),
    ("Piment sec (250g)", 6000, "Alimentaire", None),
    ("Sel de cuisine (1kg)", 3000, "Alimentaire", None),
    ("Cube Maggi (paquet)", 4000, "Alimentaire", None),
    ("Vinaigre (500ml)", 6000, "Alimentaire", None),
    ("Mayonnaise (400g)", 18000, "Alimentaire", 15000),
    ("Sardines en boîte", 7000, "Alimentaire", None),
    ("Thon en boîte", 12000, "Alimentaire", None),
    ("Corned-beef (boîte)", 15000, "Alimentaire", None),
    ("Biscuits (paquet)", 5000, "Alimentaire", None),
    ("Chocolat en poudre (400g)", 22000, "Alimentaire", None),
    ("Confiture (400g)", 17000, "Alimentaire", None),
    ("Beurre (250g)", 20000, "Alimentaire", None),
    ("Œufs (plateau de 30)", 45000, "Alimentaire", 40000),
    ("Pain de mie", 10000, "Alimentaire", None),
    ("Miel naturel (500ml)", 35000, "Alimentaire", None),

    # --- Hygiène ---
    ("Savon de Marseille", 3000, "Hygiène", None),
    ("Dentifrice", 15000, "Hygiène", None),
    ("Shampoing (250ml)", 22000, "Hygiène", None),
    ("Papier hygiénique (pack 4)", 18000, "Hygiène", None),
    ("Gel douche (500ml)", 30000, "Hygiène", 25000),
    ("Brosse à dents (unité)", 6000, "Hygiène", None),
    ("Coton-tiges (paquet)", 5000, "Hygiène", None),
    ("Serviettes hygiéniques (paquet)", 12000, "Hygiène", None),
    ("Couches bébé (paquet)", 45000, "Hygiène", 38000),
    ("Déodorant roll-on", 20000, "Hygiène", None),
    ("Crème hydratante (200ml)", 28000, "Hygiène", None),
    ("Rasoir jetable (lot de 3)", 9000, "Hygiène", None),
    ("Mousse à raser", 18000, "Hygiène", None),
    ("Savon liquide pour mains (500ml)", 15000, "Hygiène", None),
    ("Lingettes bébé (paquet)", 16000, "Hygiène", None),
    ("Talc pour bébé", 10000, "Hygiène", None),
    ("Bain moussant (500ml)", 24000, "Hygiène", None),
    ("Cure-dents (boîte)", 2000, "Hygiène", None),

    # --- Papeterie ---
    ("Cahier 100 pages", 5000, "Papeterie", None),
    ("Stylo bic (unité)", 1500, "Papeterie", None),
    ("Crayon à papier (unité)", 1000, "Papeterie", None),
    ("Gomme", 1500, "Papeterie", None),
    ("Taille-crayon", 2000, "Papeterie", None),
    ("Règle 30cm", 2500, "Papeterie", None),
    ("Classeur A4", 12000, "Papeterie", None),
    ("Feuilles A4 (rame 500)", 35000, "Papeterie", 30000),
    ("Surligneur (lot de 4)", 8000, "Papeterie", None),
    ("Colle en bâton", 3000, "Papeterie", None),
    ("Ciseaux", 5000, "Papeterie", None),
    ("Agrafeuse", 15000, "Papeterie", None),
    ("Agrafes (boîte)", 2000, "Papeterie", None),
    ("Calculatrice scientifique", 65000, "Papeterie", 55000),
    ("Sac à dos scolaire", 90000, "Papeterie", None),
    ("Trousse", 12000, "Papeterie", None),
    ("Marqueur permanent (lot de 3)", 9000, "Papeterie", None),
    ("Cahier de brouillon", 3000, "Papeterie", None),

    # --- Électronique ---
    ("Clé USB 32GB", 45000, "Électronique", None),
    ("Ampoule LED", 12000, "Électronique", None),
    ("Pile AA (paquet de 4)", 10000, "Électronique", None),
    ("Chargeur téléphone (câble USB-C)", 25000, "Électronique", None),
    ("Écouteurs filaires", 20000, "Électronique", None),
    ("Écouteurs Bluetooth", 120000, "Électronique", 99000),
    ("Powerbank 10000mAh", 150000, "Électronique", 130000),
    ("Rallonge électrique (5m)", 35000, "Électronique", None),
    ("Multiprise 4 prises", 40000, "Électronique", None),
    ("Lampe torche LED", 18000, "Électronique", None),
    ("Radio portable", 55000, "Électronique", None),
    ("Câble HDMI (2m)", 30000, "Électronique", None),
    ("Souris USB", 35000, "Électronique", None),
    ("Clavier USB", 60000, "Électronique", None),
    ("Casque audio filaire", 45000, "Électronique", None),
    ("Ventilateur de bureau USB", 50000, "Électronique", None),
    ("Adaptateur secteur universel", 28000, "Électronique", None),
    ("Batterie rechargeable AA (lot de 4)", 25000, "Électronique", None),

    # --- Boisson ---
    ("Eau minérale (1.5L)", 5000, "Boisson", None),
    ("Jus de fruit (1L)", 15000, "Boisson", None),
    ("Café soluble (100g)", 20000, "Boisson", None),
    ("Thé vert (boîte 25 sachets)", 12000, "Boisson", None),
    ("Boisson gazeuse (1.5L)", 10000, "Boisson", None),
    ("Boisson gazeuse (canette 33cl)", 4000, "Boisson", None),
    ("Jus d'orange (1L)", 16000, "Boisson", None),
    ("Eau minérale (pack 6x1.5L)", 27000, "Boisson", 24000),
    ("Sirop de fruit (750ml)", 18000, "Boisson", None),
    ("Lait concentré sucré", 9000, "Boisson", None),
    ("Yaourt à boire (1L)", 14000, "Boisson", None),
    ("Bissap (jus local, 1L)", 10000, "Boisson", None),
    ("Gingembre (jus local, 1L)", 11000, "Boisson", None),
    ("Café moulu (250g)", 25000, "Boisson", None),
    ("Boisson énergisante (canette)", 8000, "Boisson", None),
    ("Nescafé 3 en 1 (boîte 10 sticks)", 15000, "Boisson", None),
]
cur.executemany(
    "INSERT INTO produits (nom, prix, type_prod, prix_promo) VALUES (?, ?, ?, ?)",
    produits
)

conn.commit()
print(f"{len(produits)} produits insérés.")

clients_bruts = [
    ("Bah", "Ibrahima Sory", "Ratoma, Conakry", "ibrahimasorybh63@gmail.com"),
    ("Bah", "Fatoumata", "Kaloum, Conakry", "fatoumata.bah@mail.com"),
    ("Camara", "Mohamed", "Kindia", "mohamed.camara@mail.com"),
    ("Barry", "Aissatou", "Dixinn, Conakry", "aissatou.barry@mail.com"),
    ("Sylla", "Mamadou", "Kankan", "mamadou.sylla@mail.com"),
    ("Conde", "Hadja Djénabou", "Matam, Conakry", "hadja.conde@mail.com"),
    ("Toure", "Alpha Oumar", "Labé", "alpha.toure@mail.com"),
    ("Keita", "Mariama", "Ratoma, Conakry", "mariama.keita@mail.com"),
    ("Sow", "Ousmane", "Nzérékoré", "ousmane.sow@mail.com"),
    ("Cissé", "Kadiatou", "Kaloum, Conakry", "kadiatou.cisse@mail.com"),
    ("Bangoura", "Sékou", "Boké", "sekou.bangoura@mail.com"),
    ("Fofana", "Aminata", "Kissidougou", "aminata.fofana@mail.com"),
    ("Diakite", "Lansana", "Ratoma, Conakry", "lansana.diakite@mail.com"),
    ("Soumah", "Binta", "Coyah", "binta.soumah@mail.com"),
    ("Kourouma", "Alseny", "Faranah", "alseny.kourouma@mail.com"),
]

# Mot de passe de test unique pour tous les clients de seed : "test1234"
mdp_hash_test = generate_password_hash("test1234")

clients = [
    (nom, prenom, adresse, email, mdp_hash_test)
    for (nom, prenom, adresse, email) in clients_bruts
]

cur.executemany(
    "INSERT INTO clients (nom, prenom, adresse, email, mdp_hash) VALUES (?, ?, ?, ?, ?)",
    clients
)

conn.commit()
print(f"{len(clients)} clients insérés.")
conn.close()


