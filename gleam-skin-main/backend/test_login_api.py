
import requests

session = requests.Session()
url_login = "http://localhost:8000/api/auth/login/"
data_login = {
    "username": "New User",
    "password": "password123"
}

response = session.post(url_login, json=data_login)
print(f"Login Status: {response.status_code}")
print(f"Login Response: {response.json()}")
print(f"Cookies: {session.cookies.get_dict()}")

if response.status_code == 200:
    url_user = "http://localhost:8000/api/auth/user/"
    response_user = session.get(url_user)
    print(f"User Status: {response_user.status_code}")
    print(f"User Response: {response_user.json()}")
