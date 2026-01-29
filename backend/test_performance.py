import requests
import time
import csv

# -------------------------------
# Liste de mots à tester
# -------------------------------
QUERIES = [
    "amour",
    "vie",
    "mort",
    "temps",
    "homme",
    "femme",
    "nuit",
    "soleil",
    "roi",
    "cœur"
]

API_SIMPLE = "http://127.0.0.1:5000/api/search?query="
API_REGEX = "http://127.0.0.1:5000/api/search-regex?pattern="

# -------------------------------
# Fonction de test
# -------------------------------
def test_query(query, endpoint):
    """Mesure le temps de réponse et le nombre de résultats."""
    url = endpoint + query

    t0 = time.time()
    response = requests.get(url)
    t1 = time.time()

    elapsed = (t1 - t0) * 1000  # en millisecondes

    data = response.json()

    # Format % selon le type de résultat
    if isinstance(data, dict) and "results" in data:
        count = len(data["results"])
    else:
        count = len(data)

    return elapsed, count

# -------------------------------
# Lancement des tests
# -------------------------------
rows = []

for q in QUERIES:
    print(f"Test : {q}")

    # --- Test recherche simple ---
    t_simple, n_simple = test_query(q, API_SIMPLE)

    # --- Test recherche RegEx (pattern exact mot) ---
    t_regex, n_regex = test_query(q, API_REGEX)

    rows.append([q, t_simple, n_simple, t_regex, n_regex])

# -------------------------------
# Sauvegarde dans un CSV
# -------------------------------
with open("test_results.csv", "w", newline="", encoding="utf8") as f:
    writer = csv.writer(f)
    writer.writerow(["Query", "TimeSimple(ms)", "CountSimple", "TimeRegex(ms)", "CountRegex"])
    writer.writerows(rows)

print("\nTests terminés ! Résultats dans test_results.csv")
