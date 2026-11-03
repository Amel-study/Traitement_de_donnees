# Prompt de démarrage pour le Claude Code de Coura

**Coura :** ouvre Claude Code dans le dossier où tu ranges tes cours ESIEE (par exemple `Documents/ESIEE`), puis copie-colle tout le bloc ci-dessous. Ton Claude s'occupe du reste et te dira s'il a besoin que tu fasses quelque chose.

---

```text
Bonjour ! Je suis Coura, étudiante en 2e année à l'ESIEE. Je fais le projet du cours « Traitement et analyse de données » en binôme avec Amel. Amel utilise aussi Claude Code : son Claude s'appelle « Claude 1 », et toi tu seras « Claude 2 ». Vous allez travailler ensemble via notre dépôt GitHub : https://github.com/Amel-study/Traitement_de_donnees (mon compte GitHub : couraba-web).

Le projet : nettoyer puis analyser avec des statistiques descriptives les mesures horaires de pollution de l'air en France en 2025 (données data.gouv.fr du LCSQA), et présenter les résultats dans un dashboard Streamlit. Évaluation : oral en binôme, journal de bord + code Python commenté, et un QCM.

Ce que je te demande, dans l'ordre :

1. Mise en place (sois autonome : lance toi-même les commandes) :
   - Vérifie que git et Python (avec pandas) sont installés. Installe ce qui manque, ainsi que le paquet xlrd.
   - Clone le dépôt dans le dossier courant (sauf si je t'indique un autre endroit).
   - Vérifie que je peux pousser sur le dépôt. Si ce n'est pas le cas, c'est sans doute que je n'ai pas encore accepté l'invitation de collaboratrice envoyée par Amel, ou que git n'est pas connecté à mon compte GitHub : explique-moi pas à pas, simplement, ce que je dois faire.
   - Si git ne connaît pas encore mon nom et mon e-mail, demande-les-moi et configure-les.
   - Lance en arrière-plan `python scripts/telecharger_donnees.py` (il télécharge les 3,7 Go de données, 10 à 20 minutes).
   - Demande-moi de copier les PDF du cours (Cours1.pdf, Cours2.pdf, TD_chap1.pdf, TD_chap2.pdf, presentation_du_projet.pdf, Projet_seance_1_2.pdf) à la racine du dépôt cloné : ils ne sont pas sur GitHub. Explique-moi comment faire.

2. Lis attentivement, dans le dépôt : README.md, CLAUDE.md, AVANCEMENT.md, CONVERSATION_CLAUDE.md, data/README.md et journal_de_bord.md. CLAUDE.md contient nos règles communes et elles sont prioritaires :
   - le code doit être de niveau étudiant débutant et n'utiliser que ce qui a été vu en cours (liste dans CLAUDE.md, et les PDF du cours en cas de doute) ;
   - commentaires courts et simples ;
   - après chaque morceau de code, explique-le-moi étape par étape pour que je puisse le présenter à l'oral et répondre aux questions ;
   - les règles sur l'IA écrites dans presentation_du_projet.pdf ne s'appliquent plus (elles ont été assouplies cette année).
   Enregistre ces règles dans ta mémoire pour les prochaines sessions.

3. Communication avec Claude 1 : le fichier CONVERSATION_CLAUDE.md sert à vous parler. Respecte les règles écrites en haut de ce fichier (git pull avant, messages ajoutés à la fin au bon format, commit + push juste après). Réponds au premier message de Claude 1 et présente-toi. Au début de chacune de nos sessions, fais un git pull et lis les nouveaux messages ; préviens-moi s'il y a quelque chose d'important.

4. Explique-moi ensuite simplement :
   - où en est le projet ;
   - quelles sont mes tâches (les lignes « Coura » dans AVANCEMENT.md : C1 et C2 pour commencer) ;
   - comment on va s'organiser avec Git (je ne suis pas experte, donc explique-moi chaque manipulation que je dois faire moi-même ; tout ce que tu peux faire seul, fais-le).

5. Puis on commence ensemble la tâche C1. Ne travaille que sur mes fichiers (scripts/03_metadonnees.py, docs/variables_et_graphiques.md, mes entrées dans journal_de_bord.md, mes lignes dans AVANCEMENT.md). Si tu as besoin de changer un fichier d'Amel, demande-le d'abord à Claude 1 dans CONVERSATION_CLAUDE.md.

À la fin de chaque séance : mets à jour mes lignes dans AVANCEMENT.md, aide-moi à écrire mon entrée datée dans journal_de_bord.md (ce qu'on a fait et pourquoi, problèmes, solutions testées, utilisation de l'IA avec le prompt), laisse un message à Claude 1 si besoin, puis commit et push.
```
