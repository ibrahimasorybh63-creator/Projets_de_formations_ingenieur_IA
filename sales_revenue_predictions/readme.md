# Sales Revenue Prediction - V2

Premier projet de Machine Learning utilisant **Scikit-learn**.

## Objectif

Prédire le revenu (`revenue`) généré par une commande à partir de ses caractéristiques :

* informations produit
* informations client
* informations géographiques
* méthode de paiement
* caractéristiques de la commande

L'objectif est de construire un modèle capable d'estimer le revenu d'une nouvelle commande.

---

## Technologies utilisées

* Python
* Pandas
* NumPy
* Scikit-learn

---

## Ce projet contient

### Analyse et nettoyage des données

* Chargement du dataset CSV
* Suppression des doublons
* Normalisation des valeurs textuelles :

  * catégories produits
  * régions
  * moyens de paiement
  * genre client
  * type client
* Correction des erreurs de saisie grâce à des dictionnaires de mapping
* Traitement des valeurs aberrantes :

  * âge client
  * quantité commandée
  * prix unitaire
  * délai de livraison

Les valeurs incohérentes sont remplacées par des valeurs manquantes (`NaN`) afin d'être traitées lors du préprocessing.

---

## Préparation des données

Séparation des variables :

### Variables explicatives (`features`)

* `product_category`
* `region`
* `payment_method`
* `quantity`
* `unit_price`
* `discount`
* `delivery_days`
* `customer_age`
* `customer_gender`
* `customer_type`

### Variable cible (`target`)

* `revenue`

Division du dataset :

* 80% entraînement
* 20% test

avec un `random_state=42` pour garantir la reproductibilité.

---

## Préprocessing avec Scikit-learn Pipeline

Contrairement à la V1, le traitement des données est maintenant intégré dans un pipeline complet.

### Variables numériques

Pipeline utilisé :

* `SimpleImputer`

  * remplacement des valeurs manquantes par la médiane
* `StandardScaler`

  * standardisation des variables numériques

Variables concernées :

* quantité
* prix unitaire
* remise
* délai de livraison
* âge client

---

### Variables catégorielles

Pipeline utilisé :

* `SimpleImputer`

  * remplacement par la valeur la plus fréquente
* `OneHotEncoder`

  * transformation des catégories en variables numériques
  * suppression de la première catégorie (`drop='first'`)
  * gestion des nouvelles catégories (`handle_unknown='ignore'`)

Variables concernées :

* catégorie produit
* région
* méthode de paiement
* genre client
* type client

---

## Modèle utilisé

Modèle de régression :

**Linear Regression**

Architecture :

```
Données brutes
      ↓
ColumnTransformer
      ↓
Préprocessing numérique + catégoriel
      ↓
Régression linéaire
      ↓
Prédiction du revenu
```

Le modèle complet est encapsulé dans un `Pipeline Scikit-learn`.

---

## Évaluation du modèle

Les performances sont mesurées avec :

### MAE (Mean Absolute Error)

Mesure l'erreur moyenne absolue entre les revenus réels et prédits.

### RMSE (Root Mean Squared Error)

Pénalise davantage les grandes erreurs de prédiction.

### R² Score

Mesure la capacité du modèle à expliquer la variation du revenu.

---

## Prédiction sur de nouvelles commandes

Le modèle peut recevoir de nouvelles données sous forme de DataFrame et produire automatiquement une estimation du revenu.

Le pipeline applique automatiquement :

* le nettoyage nécessaire
* l'encodage
* la normalisation
* la prédiction

---

## Améliorations apportées depuis la V1

### V1

* Prétraitement manuel avec Pandas
* Risque de data leakage
* Pas d'utilisation avancée de Scikit-learn

### V2

* Utilisation de `Pipeline`
* Utilisation de `ColumnTransformer`
* Gestion automatique des valeurs manquantes
* Encodage automatique des variables catégorielles
* Séparation claire entre préparation des données et entraînement
* Meilleure reproductibilité du modèle

---

## Limites actuelles

* Le modèle utilisé est uniquement une régression linéaire.
* Aucun test avec des modèles plus complexes :

  * Random Forest
  * Gradient Boosting
  * XGBoost
* Pas encore d'optimisation des hyperparamètres.
* Pas d'analyse approfondie de l'importance des variables.
* Le feature engineering reste limité.

---

## Prochaines améliorations possibles (V3)

* Comparaison de plusieurs modèles de régression.
* Utilisation de `GridSearchCV` ou `RandomizedSearchCV`.
* Analyse des coefficients et importance des variables.
* Ajout d'une validation croisée.
* Déploiement du modèle avec une API Flask/FastAPI.
