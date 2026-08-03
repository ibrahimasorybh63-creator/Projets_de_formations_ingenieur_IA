# Gestionnaire de Tâches

Petit gestionnaire de tâches en ligne de commande, avec sauvegarde persistante dans un fichier texte.

## Contenu

- `gestache.py` — script principal. Charge les tâches existantes depuis `text.txt` au démarrage (ou démarre avec une liste vide si le fichier n'existe pas), puis propose un menu pour :
  1. Ajouter une tâche
  2. Valider une tâche (ajoute le tag `[FAIT]`)
  3. Supprimer une tâche
  0. Quitter

Chaque action déclenche une sauvegarde automatique dans `text.txt`.

## Lancer le projet

```bash
cd gestionnaire_taches
python gestache.py
```

## Concepts mis en œuvre

- Lecture/écriture de fichiers (`open`, gestion de `FileNotFoundError`)
- Manipulation de listes (ajout, indexation, `pop`)
- Boucle de menu interactif avec `input`

## Auteur

**Ibrahima (Bah Ibrahima Sory)** — Étudiant en Prépa Ingénieur (L1) à BEM Conakry, Guinée
