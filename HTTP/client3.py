import urllib.parse
import urllib.request

url = 'http://localhost:8080/cgi-bin/WebClient.py'
ua = 'Mozilla/7000.0 (Windows XXL)'

values = {
		'field1':'value1',
		'field2':'value2',
	}

forminfo = urllib.parse.urlencode(values)
print(forminfo)

#headers = {'User-agent': ua}
#req = urllib.request.Request(url, forminfo, headers)

with urllib.request.urlopen(url) as res:
	print(res.read().decode())