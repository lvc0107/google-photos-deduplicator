from collections import defaultdict
from app.embedding import cosine_similarity

def group_by_hash(photos):
    groups = defaultdict(list)
    for p in photos:
        groups[str(p["phash"])].append(p)
    return groups

def refine(groups, threshold):
    final = []

    for group in groups.values():
        if len(group) == 1:
            continue

        clusters = []
        for p in group:
            added = False
            for c in clusters:
                if cosine_similarity(p["emb"], c[0]["emb"]) > threshold:
                    c.append(p)
                    added = True
                    break
            if not added:
                clusters.append([p])

        final.extend(clusters)

    return final
