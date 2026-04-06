import imagehash

def compute_hashes(img):
    return {
        "phash": imagehash.phash(img),
        "dhash": imagehash.dhash(img)
    }

def is_similar(h1, h2, threshold=5):
    return abs(h1 - h2) <= threshold
