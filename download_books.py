import os
import requests
from bs4 import BeautifulSoup
import re

ROOT = "data/books"
os.makedirs(ROOT, exist_ok=True)

MIN_WORDS = 10000
MAX_BOOKS = 2000  
HEADERS = {"User-Agent": "Mozilla/5.0"}

LANG_SOURCES = {
    "en": "https://www.gutenberg.org/browse/languages/en",
    "fr": "https://www.gutenberg.org/browse/languages/fr",
}

def get_last_index():
    """Trouve le dernier numéro de fichier déjà téléchargé."""
    files = sorted(os.listdir(ROOT))
    if not files:
        return 0
    last = files[-1].replace(".txt", "")
    return int(last)

def get_existing_ids():
    """Récupère tous les IDs Gutenberg déjà présents dans le dossier."""
    ids = set()
    for file in os.listdir(ROOT):
        path = os.path.join(ROOT, file)
        try:
            with open(path, "r", encoding="utf8") as f:
                first_line = f.readline()
                match = re.search(r"ID:(\d+)", first_line)
                if match:
                    ids.add(match.group(1))
        except:
            pass
    return ids

def get_book_links(url):
    print(f"Fetching list from {url}...")
    html = requests.get(url, headers=HEADERS).text
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", href=re.compile(r"^/ebooks/\d+$"))
    return {re.search(r"/ebooks/(\d+)", a["href"]).group(1) for a in links}

def download_book(book_id, idx):
    urls = [
        f"https://www.gutenberg.org/files/{book_id}/{book_id}.txt",
        f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt",
        f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt",
    ]

    for url in urls:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=8)
            if resp.status_code == 200:
                text = resp.text
                if len(text.split()) >= MIN_WORDS:
                    filename = f"{ROOT}/{idx:04d}.txt"
                    with open(filename, "w", encoding="utf8") as f:
                        f.write(f"ID:{book_id}\n")  # on enregistre l'ID
                        f.write(text)
                    print(f"Saved #{book_id} → {filename} ({len(text.split())} words)")
                    return True
        except:
            pass
    return False

def main():
    last_idx = get_last_index()
    existing_ids = get_existing_ids()

    print(f"Already downloaded: {last_idx} books")
    print(f"Existing Gutenberg IDs: {len(existing_ids)}")

    all_ids = set()
    for lang, url in LANG_SOURCES.items():
        ids = get_book_links(url)
        all_ids.update(ids)

    print(f"\nTotal available IDs: {len(all_ids)}")

    new_ids = [bid for bid in all_ids if bid not in existing_ids]

    print(f"\nNew IDs to download: {len(new_ids)}")

    idx = last_idx + 1

    for book_id in new_ids:
        if idx > MAX_BOOKS:
            break
        if download_book(book_id, idx):
            idx += 1

    print("\nDONE! Total downloaded:", idx - 1)

if __name__ == "__main__":
    main()
