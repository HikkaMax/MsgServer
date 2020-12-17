import requests
import json


def DoRequest(method, cmd="", data=""):
	try:
		url = 'http://localhost:8080/cgi-bin/APIClient.py'
		header = {"Content-type": 'application-json'}
		res = method(url+cmd, headers=header, data=json.dumps(data))
		if res.status_code == 200:
			print(res.content.decode())
			return json.loads(res.content)
	except Exception as ex:
		print(ex)


def GetList():
	res = DoRequest(requests.get)
	print(res)
	for i, title in res['ids']:
		print(f"{i}: {title}")
		
		
		
		
GetList()