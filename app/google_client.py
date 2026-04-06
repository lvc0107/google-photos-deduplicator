import requests
import os

BASE_URL = "https://photoslibrary.googleapis.com/v1"

def get_headers():
    return {
        "Authorization": f"Bearer {get_access_token()}"
    }

def get_access_token():
    r = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "refresh_token": os.getenv("REFRESH_TOKEN"),
            "grant_type": "refresh_token",
        }
    )
    return r.json()["access_token"]

def fetch_photos():
    photos = []
    url = f"{BASE_URL}/mediaItems?pageSize=100"

    while url:
        r = requests.get(url, headers=get_headers()).json()
        items = r.get("mediaItems", [])
        photos.extend(items)
        token = r.get("nextPageToken")
        if token:
            url = f"{BASE_URL}/mediaItems?pageToken={token}"
        else:
            url = None

    return photos

def download(photo):
    url = photo["baseUrl"] + "=w1024"
    return requests.get(url).content

def delete(photo_ids):
    requests.post(
        f"{BASE_URL}/mediaItems:batchRemove",
        headers=get_headers(),
        json={"mediaItemIds": photo_ids}
    )
