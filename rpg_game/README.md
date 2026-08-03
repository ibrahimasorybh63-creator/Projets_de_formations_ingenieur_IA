# RPG Game — Jeu de Combat au Tour par Tour

Projet phare du dépôt : un jeu de combat 1v1 en Python, jouable dans le terminal, avec 4 classes de personnages jouables ayant chacune ses propres compétences, cooldowns et gestion de mana.

## Contenu

- `player.py` — classe de base `Player` (PV, mana, armure, effets temporaires : poison, brûlure, froid) avec la logique commune de dégâts et d'affichage d'état.
- `assassin.py`, `barbare.py`, `chevalier.py`, `mage.py` — sous-classes héritant de `Player`, chacune avec ses propres attaques et compétences spéciales.
- `combat_manager.py` — point d'entrée du jeu : création des deux joueurs, choix des classes, et classe `CombatManager` qui orchestre le déroulement des tours jusqu'à la victoire de l'un des joueurs.
- `rpg_project.py` — première version / brouillon regroupant plusieurs classes de combattants dans un seul fichier (version antérieure au découpage en modules séparés).

## Classes jouables

| Classe | Style de jeu |
|---|---|
| **Assassin** | Faibles dégâts mais réguliers ; poison, double frappe et camouflage |
| **Barbare** | Dégâts très élevés, défense faible ; mode rage |
| **Chevalier** | Faibles dégâts, mais peut se défendre, se soigner et contre-attaquer |
| **Mage** | Profil équilibré, dégâts élémentaires (feu, glace, foudre), vol de mana, armure magique temporaire |

## Lancer le jeu

```bash
cd rpg_game
python combat_manager.py
```

## Concepts mis en œuvre

- Héritage (`Player` → 4 sous-classes) et polymorphisme
- Gestion de cooldowns et de ressources (mana)
- Effets de statut temporaires (poison, brûlure, froid)
- Orchestration de la boucle de jeu via une classe dédiée (`CombatManager`)

## Auteur

**Ibrahima (Bah Ibrahima Sory)** — Étudiant en Prépa Ingénieur (L1) à BEM Conakry, Guinée
