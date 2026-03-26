import requests

login_url = "http://127.0.0.1:8000/api/auth/login/"
data = {
    "username": "po@taskvision.com",
    "password": "password123"
}

try:
    response = requests.post(login_url, json=data, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
