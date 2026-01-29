import json

GRAPH_FILE = "data/jaccard_graph.json"
OUTPUT_PR = "data/pagerank.json"

def compute_pagerank(graph, d=0.85, iterations=30):
    books = list(graph.keys())
    n = len(books)

    # Initialisation uniforme
    PR = {b: 1/n for b in books}

    for _ in range(iterations):
        new_PR = {}
        for b in books:
            # somme du PageRank des voisins
            rank_sum = sum(
                PR[neighbor] / len(graph[neighbor])
                for neighbor in graph[b]
            )
            # Formule PageRank
            new_PR[b] = (1 - d) / n + d * rank_sum

        PR = new_PR

    return PR

def main():
    print("Chargement du graphe Jaccard...")
    with open(GRAPH_FILE, "r") as f:
        graph = json.load(f)

    print("Calcul du PageRank...")
    PR = compute_pagerank(graph)

    print("Sauvegarde du PageRank...")
    with open(OUTPUT_PR, "w") as f:
        json.dump(PR, f, indent=2)

    print("PageRank terminé ! Fichier généré : data/pagerank.json")

if __name__ == "__main__":
    main()
