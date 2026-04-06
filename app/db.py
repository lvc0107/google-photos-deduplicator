import sqlite3

conn = sqlite3.connect("photos.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS processed (
    id TEXT PRIMARY KEY,
    phash TEXT,
    embedding BLOB
)
""")

def save(photo_id, phash, emb):
    cur.execute(
        "INSERT OR REPLACE INTO processed VALUES (?, ?, ?)",
        (photo_id, str(phash), emb.numpy().tobytes())
    )
    conn.commit()

def exists(photo_id):
    cur.execute("SELECT 1 FROM processed WHERE id=?", (photo_id,))
    return cur.fetchone() is not None
