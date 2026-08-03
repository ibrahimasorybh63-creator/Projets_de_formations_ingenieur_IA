# ProjetSQL — Gestion de Boutique (Flask + SQLite)

Application web de gestion d'une boutique (produits, clients, commandes), construite avec **Flask** et **SQLite**, avec un tableau de bord affichant des statistiques de vente.

## Contenu

- `schema.sql` — définition des 4 tables : `clients`, `produits`, `commandes`, `details_comm` (table de jonction avec clé primaire composite), avec clés étrangères en cascade.
- `seed.py` — remplit la base `boutique.db` avec un jeu de données de démonstration (20 produits répartis en 5 catégories, 15 clients basés en Guinée).
- `entite.py` — classes `Produit`, `Clients`, `Commandes` : CRUD complet (ajout, modification, suppression), plus des fonctions utilitaires pour lister les données, calculer les statistiques globales (`get_stats`) et déterminer les produits les plus achetés.
- `app.py` — application Flask : routes pour l'accueil (tableau de bord), la gestion des produits, des clients et des commandes (ajout, modification, suppression), avec rendu de templates Jinja2.
- `templates/` — pages HTML (dont `main.html`, le tableau de bord).
- `static/` — fichiers JS et images du frontend.

## Installation et lancement

```bash
cd projetSQL
pip install flask

# Créer la base à partir du schéma (une seule fois)
sqlite3 boutique.db < schema.sql

# Remplir la base avec des données de démonstration
python seed.py

# Lancer l'application
python app.py
```

L'application sera accessible sur `http://127.0.0.1:5000`.

## Fonctionnalités

- Tableau de bord : nombre de clients, produits, commandes, chiffre d'affaires total, produits les plus vendus.
- Gestion des produits : liste, ajout, modification du prix, suppression.
- Gestion des clients : liste, ajout, modification, suppression.
- Gestion des commandes : création (avec plusieurs produits et quantités), modification, suppression, affichage groupé par commande.

## Concepts mis en œuvre

- SQL : jointures multi-tables, clés étrangères (`PRAGMA foreign_keys`), requêtes paramétrées.
- Python : classes avec méthodes d'instance et méthodes statiques, connexion/curseur SQLite.
- Flask : routage GET/POST, formulaires, redirections, templates Jinja2.

## Auteur

**Ibrahima (Bah Ibrahima Sory)** — Étudiant en Prépa Ingénieur (L1) à BEM Conakry, Guinée
