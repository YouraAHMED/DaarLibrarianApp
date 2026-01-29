import os
import json
import re
from collections import Counter

BOOKS_DIR = "data/books"
OUTPUT_FILE = "data/indexes.json"

def clean_text(text):
    text = text.lower()
    # garder seulement lettres (avec accents) et espaces
    text = re.sub(r"[^a-zàâçéèêëîïôûùüÿñœæ]+", " ", text)
    words = [w for w in text.split() if len(w) > 2]  # enlever mots trop courts
    return words

def index_book(filepath):
    with open(filepath, "r", encoding="utf8", errors="ignore") as f:
        text = f.read()

    words = clean_text(text)
    counter = Counter(words)

    return dict(counter)

def main():
    indexes = {}
    files = sorted(os.listdir(BOOKS_DIR))

    print(f"Found {len(files)} books. Starting indexation...\n")

    for filename in files:
        book_id = filename.replace(".txt", "")
        path = os.path.join(BOOKS_DIR, filename)

        print(f"Indexing {filename} ...")
        indexes[book_id] = index_book(path)

  
    with open(OUTPUT_FILE, "w", encoding="utf8") as f:
        json.dump(indexes, f, indent=2, ensure_ascii=False)

    print("\nDONE!")
    print(f"Indexes saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
