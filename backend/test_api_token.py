import requests

token = "ec60fe3830eadee146549ee45c4d111a4ffee5561"
header = {"Authorization": f"Token {token}"}
res = requests.get("http://127.0.0.1:8000/api/tasks/", headers=header)
print(f"Status: {res.status_code}")
print(f"Data: {res.text}")
