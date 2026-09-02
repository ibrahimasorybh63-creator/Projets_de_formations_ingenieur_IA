# ProjetSQL — Gestion de Boutique & Système de Recommandation

Application web de gestion d'une boutique construite avec **Flask** et **SQLite**.  
Le projet comprend une interface **admin**, une interface **client** et un premier système de **recommandation de produits** basé sur plusieurs approches.

## Contenu

- `schema.sql` — définition des tables :
  - `clients` — gestion des utilisateurs et authentification
  - `produits` — catalogue des produits, catégories, prix et promotions
  - `commandes` — commandes des clients
  - `details_comm` — détail des produits commandés
  - `recommandations_produits` — stockage des scores de recommandation issus du baseline

- `seed.py` — remplit la base `boutique.db` avec un jeu de données de démonstration comprenant des produits et des clients.

- `entite.py` — contient les classes métier (`Produit`, `Clients`, `Commandes`) ainsi que les fonctions liées aux statistiques et aux systèmes de recommandation.

- `app.py` — application Flask :
  - **Admin** : tableau de bord, gestion des produits, clients et commandes
  - **Client** : catalogue, recherche, panier, commandes et recommandations

- `setup/recommendations/` — fonctions dédiées aux systèmes de recommandation.

- `templates/` — pages HTML de l'administration et de la boutique.

- `static/` — fichiers JavaScript et ressources du frontend.

## Installation et lancement

```bash
cd projetSQL
pip install flask werkzeug numpy scikit-learn

#Créer la base à partir du schéma et remplir la base avec les données de démonstration
python setup.py

# Lancer l'application
python app.py
```

L'application sera accessible sur :

`http://127.0.0.1:5000`

## Fonctionnalités

### Côté admin

- Tableau de bord avec statistiques de vente
- Gestion des produits
- Modification et suppression des produits
- Gestion des clients
- Gestion des commandes
- Gestion dynamique des lignes de commande
- Prise en compte des prix promotionnels

### Côté client

- Inscription et connexion
- Authentification par session
- Catalogue des produits
- Filtrage par catégorie
- Recherche par nom
- Filtre des promotions
- Ajout et modification du panier
- Suppression de produits du panier
- Validation de commande
- Affichage de recommandations

## Système de recommandation

Le projet explore progressivement différentes approches de recommandation.

### 1. Baseline — popularité

Une première recommandation basée sur les produits les plus achetés est utilisée comme **baseline**.

Le score d'un produit est calculé à partir de sa quantité vendue sur une fenêtre temporelle donnée :

```text
score(produit) =
quantité vendue du produit /
quantité totale vendue
```

Les scores sont recalculés après une nouvelle commande et les produits sont classés afin d'obtenir un **Top-K**.

### 2. Content-based

Une approche basée sur le contenu des produits est également développée.

Les produits sont représentés à partir de leur **description textuelle**, puis une mesure de similarité permet d'identifier les produits proches.

Le système peut ensuite utiliser l'historique d'achat du client pour rechercher des produits similaires à ceux qu'il a déjà achetés.

### 3. Collaborative filtering

Le filtrage collaboratif a été implémenté afin de personnaliser les recommandations à partir des comportements d’achat des utilisateurs.

Cette approche analyse les historiques de commandes pour identifier les utilisateurs ayant des comportements similaires, puis recommande à un utilisateur des produits achetés par ces utilisateurs similaires mais qu’il n’a pas encore achetés.

## Concepts mis en œuvre

### SQL

- Jointures multi-tables
- Agrégations (`SUM`, `GROUP BY`, `ORDER BY`)
- Sous-requêtes
- Requêtes paramétrées
- Clés étrangères
- `ON DELETE CASCADE`
- Contraintes `UNIQUE` et `NOT NULL`
- Tables de liaison

### Python

- Programmation orientée objet
- Classes et méthodes
- Gestion des connexions SQLite
- Manipulation de listes et dictionnaires
- Calculs avec NumPy

### Machine Learning

- Représentation vectorielle des données textuelles
- TF-IDF
- Similarité cosinus
- Classement par score
- Top-K
- Filtrage basé sur le contenu
- Exploration du filtrage collaboratif

### Flask

- Routage GET/POST
- Sessions
- Templates Jinja2
- JSON et requêtes AJAX
- Séparation des responsabilités entre routes et fonctions métier

### Frontend

- JavaScript vanilla
- `fetch`
- Manipulation du DOM
- Tailwind CSS
- Interface responsive

## Architecture générale du système de recommandation

```text
Données de la boutique
        ↓
Historique / informations produits
        ↓
Transformation en données calculables
        ↓
Méthode de recommandation
        ↓
Calcul des scores
        ↓
Classement décroissant
        ↓
Top-K
        ↓
Affichage dans la boutique
```

## Auteur

**Ibrahima Sory Bah** — Étudiant en Prépa Ingénieur (L1) à BEM Conakry, Guinée
