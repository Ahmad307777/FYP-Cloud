
import requests

url = "http://localhost:8000/api/auth/register/"
data = {
    "username": "New User",
    "email": "newuser@example.com",
    "password": "password123"
}

response = requests.post(url, json=data)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
