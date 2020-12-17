import requests


url = 'http://localhost:8080/'

res = requests.get(url)
print(res.status_code)
print(res.content)
