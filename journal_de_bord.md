# Journal de bord

Pour chaque séance, avec la date : ce qu'on a fait et pourquoi, les problèmes rencontrés, les solutions testées (et pourquoi certaines n'ont pas marché), l'utilisation de l'IA (prompt, pourquoi, ce qu'on en a fait).
Chacune écrit ses propres entrées, en indiquant son prénom.

---

## 24/10/2026 — Amel

**Ce qu'on a fait et pourquoi**
- Lecture des consignes du projet.
- Choix du dataset « Données temps réel de mesure des concentrations de polluants atmosphériques réglementés » (data.gouv.fr, LCSQA). Pourquoi : gros volume (un fichier par jour d'environ 50 000 lignes), données réelles et actuelles, beaucoup de choses à nettoyer.
- Téléchargement de toute l'année 2025 (365 fichiers CSV, 3,7 Go) pour pouvoir étudier les saisons, et des fichiers de métadonnées (stations, zones).

**Problèmes rencontrés**
- La page data.gouv propose 11 ressources (CSV, XML, Excel, guides européens) : il a fallu trier ce qui était utile.
- Les données sont découpées en un fichier par jour.

**Utilisation de l'IA**
- Prompt (Claude Code) : « Analyse les documents qui décrivent le projet sur lequel on doit travailler. On a choisi d'utiliser la base de données suivante : [lien]. Je voudrais que tu nous dises quels fichiers de cette base de données sont intéressants pour nous et à quoi ils correspondent. Je voudrais que tu stockes ces fichiers dans un dossier data en les renommant en fonction de leur utilité. Ne modifie pas le contenu des fichiers pour l'instant. Enfin dis-nous comment nous y prendre pour le projet. »
- Pourquoi : gagner du temps sur le tri des ressources et comprendre la structure du dataset.
- Ce qu'on en a fait : relecture des fichiers retenus et de leur description (data/README.md), vérification sur un fichier ouvert dans Python.

## 26/10/2026 — Amel

**Ce qu'on a fait et pourquoi**
- Vérification que le découpage en un fichier par jour n'est pas un problème : les 365 fichiers ont les mêmes colonnes et chaque fichier ne contient que son jour → on pourra les concaténer.
- Compréhension du rôle des fichiers de métadonnées (stations, zones) et de la façon de les relier aux mesures (`code site` ↔ `NatlStationCode`, `code zas` ↔ `ZoneCode`).

**Problème identifié et solution prévue**
- 17,6 millions de lignes : trop pour être chargées d'un coup. Solution prévue : lire les fichiers un par un dans une boucle, les nettoyer et les réduire à une moyenne journalière avant de les concaténer.

## 03/11/2026 — Amel

- Mise en place du dépôt GitHub pour travailler à deux, d'un fichier d'avancement et d'une répartition des tâches avec Coura.
