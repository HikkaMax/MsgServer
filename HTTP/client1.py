import socket

port = 8080
host = '127.0.0.1'
path = '/cgi-bin/WebClient.py'
path = '/'
ua = 'Mozilla/7000.0 (Windows XXL)'


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.sendall(f"""GET {path} HTTP/1.0
User-Agent: {ua}

""".encode())

r = b''
while True:
	data = s.recv(1024)
	if not data:
		break
	r += data
	print('.')

print(r.decode())