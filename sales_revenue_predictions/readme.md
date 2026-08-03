# Sales Revenue Prediction - V1

Premier projet de Machine Learning utilisant Scikit-learn.

## Objectif

Prédire le revenu d'une commande à partir de ses caractéristiques.

## Ce projet contient

- Analyse exploratoire des données (EDA)
- Nettoyage des données
- Traitement des valeurs manquantes
- Détection des valeurs aberrantes (IQR)
- Encodage des variables catégorielles
- Feature engineering (encodage cyclique des mois)
- Régression linéaire
- Évaluation du modèle (MAE, RMSE, R²)

## Limites de cette version

- Le prétraitement est réalisé manuellement avec Pandas.
- Certaines transformations sont effectuées avant le train/test split, ce qui peut entraîner du data leakage.
- Le projet n'utilise pas encore les composants avancés de Scikit-learn (Pipeline, ColumnTransformer, SimpleImputer, OneHotEncoder).

Une V2 corrigera ces points en utilisant un pipeline Scikit-learn complet.
