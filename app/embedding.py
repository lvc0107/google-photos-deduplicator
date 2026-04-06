import torch
import clip
from PIL import Image

device = "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def get_embedding(img: Image.Image):
    image = preprocess(img).unsqueeze(0).to(device)
    with torch.no_grad():
        emb = model.encode_image(image)
    return emb / emb.norm(dim=-1, keepdim=True)

def cosine_similarity(a, b):
    return (a @ b.T).item()
