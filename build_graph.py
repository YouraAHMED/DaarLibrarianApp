import json
from collections import defaultdict
import itertools

INDEXES_FILE = "data/indexes.json"
OUTPUT_GRAPH = "data/jaccard_graph.json"

# Seuil Jaccard : tu peux augmenter à 0.15 ou 0.2 pour encore moins de liens
THRESHOLD = 0.1

def main():
    print("Chargement des index...")
    with open(INDEXES_FILE, "r", encoding="utf8") as f:
        indexes = json.load(f)

    # doc_words[book_id] = set(mots du livre)
    doc_words = {}
    doc_sizes = {}

    for book_id, word_counts in indexes.items():
        words = set(word_counts.keys())
        doc_words[book_id] = words
        doc_sizes[book_id] = len(words)

    print("Construction de l'index inversé (mot → livres)...")
    inverted = defaultdict(list)  # mot -> [livre1, livre2, ...]

    for book_id, words in doc_words.items():
        for w in words:
            inverted[w].append(book_id)

    print("Calcul des intersections (paires de livres qui partagent au moins 1 mot)...")
    intersections = defaultdict(int)  # (idA, idB) -> |A ∩ B|

    count_words = 0
    for w, docs in inverted.items():
        count_words += 1
        if count_words % 1000 == 0:
            print(f"{count_words} mots traités...")

        if len(docs) < 2:
            continue  # un seul livre, aucune paire

        # Pour chaque paire de livres contenant ce mot
        for idA, idB in itertools.combinations(docs, 2):
            if idA > idB:
                idA, idB = idB, idA
            intersections[(idA, idB)] += 1

    print("Calcul des similarités de Jaccard et construction du graphe...")
    graph = defaultdict(dict)

    for (idA, idB), inter in intersections.items():
        sizeA = doc_sizes[idA]
        sizeB = doc_sizes[idB]
        union = sizeA + sizeB - inter

        if union == 0:
            continue

        score = inter / union

        if score >= THRESHOLD:
            graph[idA][idB] = score
            graph[idB][idA] = score

    nb_edges = sum(len(neigh) for neigh in graph.values())
    print(f"Nombre total de liens retenus : {nb_edges}")

    with open(OUTPUT_GRAPH, "w", encoding="utf8") as f:
        json.dump(graph, f, indent=2)

    print(f"Graphe Jaccard sauvegardé dans {OUTPUT_GRAPH}")

if __name__ == "__main__":
    main()
