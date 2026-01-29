# Moteur de recherche pour bibliothèque numérique

Ce projet consiste à développer un moteur de recherche textuel pour une bibliothèque numérique composée de plus de 2000 livres issus du corpus Project Gutenberg. 
Il combine des techniques classiques de recherche d’information, de similarité textuelle et d’analyse de graphes afin de proposer des résultats pertinents et des suggestions intelligentes.

---

## Objectifs du projet

Le moteur de recherche permet de :

- Rechercher un mot-clé dans l’ensemble du corpus
- Effectuer des recherches avancées à l’aide d’expressions régulières (RegEx)
- Classer les documents selon leur pertinence
- Suggérer des documents similaires à partir d’un graphe de similarité
- Proposer une interface web simple et interactive

---

## Technologies utilisées

- Python
- Flask (API et backend)
- Vue.js (interface utilisateur)
- NetworkX (manipulation de graphes)
- JSON (stockage des structures d’index)
- Project Gutenberg (corpus de données)

---

## Architecture du projet

Le projet repose sur plusieurs structures de données fondamentales :

### Index inversé

Un index inversé associe chaque mot à la liste des documents dans lesquels il apparaît, ainsi qu’à sa fréquence dans chaque document. 
Cette structure permet une recherche très rapide par mot-clé.

### Fréquences internes par document

Pour chaque document, une table locale stocke les fréquences des mots. 
Elle est utilisée pour le classement des résultats et le calcul des similarités.

### Graphe de similarité (Jaccard)

Un graphe non orienté est construit à partir du coefficient de similarité de Jaccard entre les ensembles de mots des documents. 
Il permet de proposer des suggestions de documents similaires.

### Score de centralité (PageRank)

Le PageRank est calculé sur le graphe de similarité afin de mesurer l’importance structurelle des documents dans le corpus. 
Ce score est intégré au classement final des résultats.

---

## Fonctionnalités principales

### Recherche simple par mot-clé

La recherche simple repose sur l’index inversé et permet un accès quasi instantané aux documents contenant le mot recherché. 
Le classement combine la fréquence d’apparition du mot et le score PageRank.

### Recherche avancée par expressions régulières

La recherche RegEx permet d’interroger le corpus à l’aide de motifs complexes. 
Elle offre plus de flexibilité, au prix d’un coût de calcul plus élevé.

### Suggestions de documents

À partir des documents les plus pertinents pour une requête, le moteur propose des documents similaires en exploitant le graphe de similarité Jaccard.

---

## Tests et performances

- La recherche par mot-clé s’exécute en quelques millisecondes grâce à l’index inversé
- La recherche par expressions régulières est plus coûteuse mais reste exploitable dans un contexte web
- Les suggestions basées sur le graphe améliorent la qualité des résultats proposés

---

## Données et génération des fichiers

Le dossier `data/` n’est pas inclus dans le dépôt Git. 
Il contient des données volumineuses et des fichiers générés automatiquement.

Ces fichiers peuvent être entièrement régénérés à partir des scripts fournis dans le projet.

##data/books/


Commande à exécuter :

python scripts/download_books.py

##Génération des structures d’indexation

Une fois les livres téléchargés, les structures de données peuvent être construites en exécutant :

python scripts/build_indexes.py


Ce script génère automatiquement :

l’index inversé

le graphe de similarité Jaccard

les scores PageRank

Les fichiers sont enregistrés dans le dossier data/.

##Remarque

La génération complète des données peut prendre plusieurs minutes, en particulier lors de la construction du graphe de similarité Jaccard sur un corpus volumineux.
---

## Lancement du projet

### Prérequis

- Python 3.x
- Node.js et npm
- Environnement virtuel Python

### Lancement du backend

```bash
python app.py
```

### Lancement du frontend

```bash
npm install
npm run serve
```

---

## Auteur

AHMED Youra 
Master Informatique – Science et Technologie du Logiciel 
Promotion 2025–2026
