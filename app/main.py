import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
from tqdm import tqdm

from app.google_client import fetch_photos, download, delete
from app.hashing import compute_hashes
from app.embedding import get_embedding
from app.deduplicator import group_by_hash, refine

load_dotenv()

DRY_RUN = os.getenv("DRY_RUN", "true") == "true"
THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.95))

def pick_best(group):
    return sorted(group, key=lambda x: int(x.get("mediaMetadata", {}).get("width", 0)), reverse=True)[0]

def main():
    photos = fetch_photos()

    processed = []

    for p in tqdm(photos):
        try:
            img = Image.open(BytesIO(download(p)))

            hashes = compute_hashes(img)
            emb = get_embedding(img)

            p["phash"] = hashes["phash"]
            p["emb"] = emb

            processed.append(p)

        except Exception:
            continue

    groups = group_by_hash(processed)
    groups = refine(groups, THRESHOLD)

    duplicates = [g for g in groups if len(g) > 1]

    to_delete = []

    for group in duplicates:
        best = pick_best(group)
        for p in group:
            if p["id"] != best["id"]:
                to_delete.append(p["id"])

    print(f"Found {len(to_delete)} duplicates")

    if not DRY_RUN:
        delete(to_delete)

if __name__ == "__main__":
    main()
