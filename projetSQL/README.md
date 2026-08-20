# ProjetSQL — Gestion de Boutique (Flask + SQLite)

Application web de gestion d'une boutique (produits, clients, commandes), construite avec **Flask** et **SQLite**. Comprend une interface **admin** (tableau de bord, gestion CRUD) et une interface **client** (boutique publique avec panier et commande).

## Contenu

- `schema.sql` — définition des 4 tables : `clients` (avec authentification : `email`, `mdp_hash`), `produits` (avec `prix_promo` optionnel), `commandes`, `details_comm` (table de jonction avec clé primaire composite), avec clés étrangères en cascade.
- `seed.py` — remplit la base `boutique.db` avec un jeu de données de démonstration (produits répartis en 5 catégories, clients avec mots de passe hashés).
- `entite.py` — classes `Produit`, `Clients` (inscription, connexion avec hash bcrypt), `Commandes` : CRUD complet, plus des fonctions utilitaires (statistiques, produits les plus achetés, commandes groupées avec total).
- `app.py` — application Flask :
  - **Admin** : tableau de bord, gestion des produits/clients/commandes, protégé par authentification (`@app.before_request`)
  - **Client** : catalogue filtrable, panier, inscription/connexion, validation de commande
- `templates/` — pages HTML (admin et boutique).
- `static/` — fichiers JS (séparés par page) et images du frontend.

## Installation et lancement

```bash
cd projetSQL
pip install flask werkzeug

# Créer la base à partir du schéma (une seule fois)
sqlite3 boutique.db < schema.sql

# Remplir la base avec des données de démonstration
python seed.py

# Lancer l'application
python app.py
```

L'application sera accessible sur `http://127.0.0.1:5000`.

## Fonctionnalités

**Côté admin** (accès protégé par connexion) :

- Tableau de bord : statistiques de vente, produits les plus vendus.
- Gestion des produits : liste, modification, suppression.
- Gestion des clients : liste, modification, suppression (création réservée à l'inscription client).
- Gestion des commandes : création, modification (lignes produits dynamiques, prix promo pris en compte, total affiché), suppression.

**Côté client** :

- Inscription et connexion (mot de passe hashé, session sécurisée).
- Catalogue filtrable (catégorie, recherche, promotions).
- Panier : ajout, modification de quantité, suppression.
- Validation de commande (connexion requise).

## Concepts mis en œuvre

- SQL : jointures multi-tables, clés étrangères (`PRAGMA foreign_keys`), requêtes paramétrées, contraintes `UNIQUE`/`NOT NULL`.
- Python : classes avec méthodes d'instance et méthodes statiques, connexion SQLite par requête.
- Sécurité : hash de mot de passe (`werkzeug.security`), messages d'erreur génériques anti-énumération, protection des routes sensibles.
- Flask : routage GET/POST, sessions, JSON (API AJAX), redirections, templates Jinja2.
- Frontend : JavaScript vanilla (`fetch`/`async`), manipulation du DOM, Tailwind CSS.

## Auteur

**Ibrahima (Bah Ibrahima Sory)** — Étudiant en Prépa Ingénieur (L1) à BEM Conakry, Guinée
