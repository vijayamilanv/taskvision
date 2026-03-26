import requests
import json

API_URL = "http://localhost:8000/api"
TOKEN = "025b214c0dfc5159067404e5a09197cfcafce0bf" 

headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

print("--- FETCHING PROJECTS ---")
res = requests.get(f"{API_URL}/projects/", headers=headers)
print(f"Status: {res.status_code}")
data = res.json()
print(json.dumps(data, indent=2))
