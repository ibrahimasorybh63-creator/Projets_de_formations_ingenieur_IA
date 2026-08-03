# Calculatrice

Calculatrice réalisée en deux versions : une en ligne de commande (Python) et une interface web (HTML/CSS/JS).

## Contenu

- `calculatrice.py` — version terminal. Menu avec addition, soustraction, multiplication, division (avec gestion de la division par 0), puissance et racine carrée.
- `calculatrice.html` — version web, calculatrice scientifique inspirée de l'app Windows (mémoire M+/M-/MS/MR, parenthèses, puissance, log, ln, factorielle, etc.), stylée avec Bootstrap et animée en JavaScript pur (pas de framework).

## Lancer la version Python

```bash
cd calculatrice
python calculatrice.py
```

## Lancer la version web

Ouvrir simplement `calculatrice.html` dans un navigateur.

## Concepts mis en œuvre

- Python : fonctions, gestion d'exceptions (`ValueError`), boucle de menu interactif.
- JS : manipulation du DOM, `addEventListener`, gestion d'état (opérande / opérateur en attente).

## Auteur

**Ibrahima (Bah Ibrahima Sory)** — Étudiant en Prépa Ingénieur (L1) à BEM Conakry, Guinée
