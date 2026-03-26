import requests

login_url = "http://127.0.0.1:8000/api/auth/login/"
data = {"username": "po@example.com", "password": "123456"}
res = requests.post(login_url, json=data)
print(res.json()['token'])
