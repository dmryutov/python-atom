import requests

for i in range(5):
    response = requests.get('http://127.0.0.1:8080')
    print(response.status_code)
    print(response.text)