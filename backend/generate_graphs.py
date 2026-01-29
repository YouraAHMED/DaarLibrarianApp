import pandas as pd
import matplotlib.pyplot as plt


data = {
    "Query": ["amour", "vie", "mort", "temps", "homme", "femme", "nuit", "soleil", "roi", "cœur"],
    "TimeSimple(ms)": [18.6650753, 16.109705, 15.604973, 15.44404, 15.730619, 21.567583, 15.146017, 14.895201, 14.462948, 11.422634],
    "CountSimple": [1914, 1988, 1966, 1979, 1990, 1918, 1920, 1854, 1734, 1161],
    "TimeRegex(ms)": [509.973049, 94.519854, 276.097059, 176.856279, 139.647007, 364.709377, 544.506311, 862.718344, 72.55125, 1575.015068],
    "CountRegex": [1935, 2000, 1990, 1980, 1995, 1960, 1951, 1862, 2000, 1162]
}

df = pd.DataFrame(data)


queries = df["Query"].tolist()
time_simple = df["TimeSimple(ms)"].tolist()
time_regex = df["TimeRegex(ms)"].tolist()
count_simple = df["CountSimple"].tolist()
count_regex = df["CountRegex"].tolist()


plt.figure(figsize=(10,6))
plt.plot(queries, time_simple, marker='o', linewidth=2, label="Recherche simple")
plt.plot(queries, time_regex, marker='o', linewidth=2, label="Recherche RegEx")
plt.xlabel("Mot recherché")
plt.ylabel("Temps d'exécution (ms)")
plt.title("Comparaison des temps d'exécution")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("graph_time.png")
plt.close()


plt.figure(figsize=(10,6))
plt.plot(queries, count_simple, marker='o', linewidth=2, label="Résultats simples")
plt.plot(queries, count_regex, marker='o', linewidth=2, label="Résultats RegEx")
plt.xlabel("Mot recherché")
plt.ylabel("Nombre de documents trouvés")
plt.title("Comparaison du nombre de résultats")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("graph_results.png")
plt.close()

print("✔ Graphiques générés : graph_time.png et graph_results.png")
