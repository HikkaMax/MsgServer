import http.client

port = 8080
host = 'localhost'
path = '/cgi-bin/WebClient.py'

client = http.client.HTTPConnection(f"{host}:{port}")
client.request("GET", path)

with client.getresponse() as res:
	print(res.status)
	print(res.read().decode())