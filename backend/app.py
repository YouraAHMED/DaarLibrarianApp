from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import re
import json
from collections import Counter

app = Flask(__name__)
CORS(app)

# ============================================================
# 📂 Chemins des fichiers
# ============================================================

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "../data"))

BOOKS_DIR = os.path.join(DATA_DIR, "books")
INDEXES_FILE = os.path.join(DATA_DIR, "indexes.json")
JACCARD_FILE = os.path.join(DATA_DIR, "jaccard_graph.json")
PAGERANK_FILE = os.path.join(DATA_DIR, "pagerank.json")

# ============================================================
# 📥 Chargement des données (une seule fois)
# ============================================================

def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r", encoding="utf8") as f:
            return json.load(f)
    return default

INDEXES = load_json(INDEXES_FILE, {})
JACCARD_GRAPH = load_json(JACCARD_FILE, {})
PAGERANK = load_json(PAGERANK_FILE, {})

# Renvoie le pagerank d’un livre, ou 0.0 s'il n’existe pas
def get_pagerank(book_id):
    return float(PAGERANK.get(book_id, 0.0))

# ============================================================
# 🔧 Nettoyage texte
# ============================================================

def clean_text(text: str):
    """Nettoie le texte en mots (a-z + accents), minuscules, longueur > 2."""
    text = text.lower()
    text = re.sub(r"[^a-zàâçéèêëîïôûùüÿñæœ]+", " ", text)
    return [w for w in text.split() if len(w) > 2]

# ============================================================
# 📘 API : détail d’un livre
# ============================================================

@app.route("/api/book/<book_id>")
def get_book(book_id):
    path = os.path.join(BOOKS_DIR, f"{book_id}.txt")

    if not os.path.exists(path):
        return jsonify({"error": "Book not found"}), 404

    with open(path, "r", encoding="utf8", errors="ignore") as f:
        text = f.read()

    words = clean_text(text)
    return jsonify({
        "id": book_id,
        "title": f"Livre {book_id}",
        "word_count": len(words),
        "excerpt": text[:300].replace("\n", " "),
        "top_words": Counter(words).most_common(10),
        "pagerank": get_pagerank(book_id)
    })

# ============================================================
# 🔎 API : recherche simple (index inversé)
# ============================================================

@app.route("/api/search")
def search():
    query = request.args.get("query", "").strip().lower()

    if query == "":
        return jsonify({"results": [], "suggestions": []}), 200

    results = []

    # Récupération des résultats directs
    for book_id, index in INDEXES.items():
        occ = index.get(query)
        if occ:
            pr = get_pagerank(book_id)
            score = occ * 0.7 + pr * 0.3
            results.append({
                "id": book_id,
                "occurrences": occ,
                "pagerank": pr,
                "score": score
            })

    # tri
    results.sort(key=lambda x: x["score"], reverse=True)

    # --------------- Suggestions automatiques (Jaccard + PR) ---------------
    suggestions = []
    if results:
        top_ids = [r["id"] for r in results[:3]]
        suggestion_scores = {}

        for bid in top_ids:
            for nid, jscore in JACCARD_GRAPH.get(bid, {}).items():
                if nid not in top_ids:
                    suggestion_scores[nid] = max(jscore, suggestion_scores.get(nid, 0))

        for nid, js in suggestion_scores.items():
            suggestions.append({
                "id": nid,
                "jaccard": js,
                "pagerank": get_pagerank(nid),
            })

        suggestions.sort(key=lambda x: x["jaccard"], reverse=True)
        suggestions = suggestions[:10]

    return jsonify({
        "results": results,
        "suggestions": suggestions
    })

# ============================================================
# 🧩 API : recherche RegEx (index)
# ============================================================

@app.route("/api/search-regex")
def search_regex():
    pattern = request.args.get("pattern", "").strip()

    if not pattern:
        return jsonify([]), 200

    # Vérification RegEx
    try:
        regex = re.compile(pattern, re.IGNORECASE)
    except re.error:
        return jsonify({"error": "Invalid regex pattern"}), 400

    results = []

    for book_id, index in INDEXES.items():
        for word, occ in index.items():
            if regex.search(word):
                results.append({
                    "id": book_id,
                    "word": word,
                    "occurrences": occ,
                    "pagerank": get_pagerank(book_id),
                })
                break

    results.sort(key=lambda x: x["occurrences"], reverse=True)
    return jsonify(results)

# ============================================================
# 📚 API : liste des livres
# ============================================================

@app.route("/api/books")
def list_books():
    books = [
        {
            "id": book_id,
            "word_count": sum(index.values()),
            "pagerank": get_pagerank(book_id)
        }
        for book_id, index in INDEXES.items()
    ]

    books.sort(key=lambda x: int(x["id"]))
    return jsonify(books)

# ============================================================
# 🔗 API : suggestions pour un livre
# ============================================================

@app.route("/api/suggestions/<book_id>")
def suggestions(book_id):

    if book_id not in JACCARD_GRAPH:
        return jsonify([]), 200

    suggestions = []
    for other_id, jscore in JACCARD_GRAPH[book_id].items():
        suggestions.append({
            "id": other_id,
            "score": jscore,
            "pagerank": get_pagerank(other_id)
        })

    suggestions.sort(key=lambda x: x["score"], reverse=True)
    return jsonify(suggestions[:10])

# ============================================================
# 📊 API : stats globales (NOUVEAU)
# ============================================================

@app.route("/api/stats")
def stats():
    return jsonify({
        "books": len(INDEXES),
        "graph_nodes": len(JACCARD_GRAPH),
        "graph_edges": sum(len(v) for v in JACCARD_GRAPH.values()),
        "max_pagerank": max(PAGERANK.values()) if PAGERANK else 0,
    })

# ============================================================
# 🚀 Lancer le serveur
# ============================================================

if __name__ == "__main__":
    app.run(debug=True, port=5000)
