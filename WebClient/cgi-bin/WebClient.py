# -*- coding: utf-8 -*-

import os, sys, re, codecs, binascii, cgi, cgitb, datetime, pickle
from msg import *

cgitb.enable()
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

class Messenger:
	def __init__(self, q):
		self.q = q
		self.MessageText = ''

	def PrintPage(self):
		print(f"""Content-type: text/html; charset=utf-8

<html><head><title>Messages</title></head>
<body>
<form action=/cgi-bin/WebClient.py name=msgform>
<input type=hidden name=ClientID value="{Message.ClientID}">
<input type=hidden name=type value="send">
<div style =" background-color: white;
    		  width: 100px;
    		  height: 30px;
			  display: flex;
              flex-direction: column;
              justify-content: center;
			  border-radius: 5px;
			  margin-bottom: 20px;
    		  text-align: center;">
			  <span>Ваш ID = {Message.ClientID}</span></div>
<input type=text name=message value="{self.MessageText}"><br>
<input type=button value="Connect" onclick="document.forms.msgform.type.value='connect'; document.forms.msgform.submit();>
<input type=submit value="Send">
<input type=button value="Get" onclick="document.forms.msgform.type.value='get'; document.forms.msgform.submit();">
</form>
</body></html>
	""")


	def MsgSend(self):
		if Message.ClientID != 0:
			Message.SendMessage(M_ALL, M_DATA, self.q.getvalue('message'))
		else:
			self.MessageText = "You are not authorized."


	def MsgGet(self):
		if Message.ClientID != 0:
			m = Message.SendMessage(M_BROKER, M_GETDATA)
			if m.Header.Type == M_DATA:
				self.MessageText = m.Data
		else:
			self.MessageText = "You are not authorized."

	def Connect(self):
		Message.ClientID = int(q.getvalue('ClientID', 0))
		if Message.ClientID == 0:
			Message.SendMessage(M_BROKER, M_INIT)

def main():
	q = cgi.FieldStorage()
	m = Messenger(q)

	MENU = {
		'send':	m.MsgSend,
		'get':  m.MsgGet,
		'connect': m.Connect
	}
    

	try:
		MENU[q.getvalue('type')]()
	except Exception as e:
		pass

	m.PrintPage()
        
main()
