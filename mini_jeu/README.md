# Mini Jeu de Combat

Premier prototype d'un jeu de combat 1v1 au tour par tour en Python — la version simplifiée ayant servi de base au projet plus abouti [`rpg_game`](../rpg_game).

## Contenu

- `mini_jeu.py` — deux joueurs (`Player`) démarrent avec 20 points de vie et s'affrontent tour par tour. À partir du tour 2, chaque joueur peut choisir entre attaque normale, attaque spéciale ou soin ; au premier tour, seule l'attaque normale est disponible. Le combat s'arrête dès qu'un joueur tombe à 0 PV ou moins.

## Lancer le projet

```bash
cd mini_jeu
python mini_jeu.py
```

## Concepts mis en œuvre

- Programmation orientée objet (classe `Player`)
- `random.choice` pour la variation des dégâts/soins
- Boucle de jeu tour par tour avec menus conditionnels

## Auteur

**Ibrahima (Bah Ibrahima Sory)** — Étudiant en Prépa Ingénieur (L1) à BEM Conakry, Guinée
