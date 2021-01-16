# -*- coding: utf-8 -*-

import os, sys, re, codecs, binascii, cgi, cgitb, datetime, pickle
from msg import *

cgitb.enable()
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())


class Messenger:
    def __init__(self, q):
        self.q = q
        Message.ClientID = int(q.getvalue('ClientID', 0))
        if Message.ClientID == 0:
            Message.SendMessage(M_BROKER, M_INIT)
        self.MessageText = ''
        self.ReceiverId = 0
        self.ResultText = ''

    def PrintPage(self):
        print(f"""Content-type: text/html; charset=utf-8

<html>
<head>
<title>Messages</title>
</head>
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
<span>Введите сообщение</span><input type=text name=message value="{self.MessageText}"><br>
<span>Введите ID пользователя</span><input type=text name=receiverId value="{self.ReceiverId}"><br>

<input type=button value="Connect" onclick="document.forms.msgform.type.value='connect'; document.forms.msgform.submit();">
<input type=submit value="Send message" onclick="document.forms.msgform.type.value='sendmsg'; document.forms.msgform.submit();">
<input type=submit value="History" onclick="document.forms.msgform.type.value='history'; document.forms.msgform.submit();">
<input type=button value="Get" onclick="document.forms.msgform.type.value='get'; document.forms.msgform.submit();">
<script type="text/JavaScript">
</script>
<br><span>{self.ResultText}</span>
</form>
</body></html>
    """)

    def MsgSend(self):
        if Message.ClientID != 0:
            if int(self.q.getvalue('receiverId')) == 0:
                Message.SendMessage(M_ALL, M_DATA, self.q.getvalue('message'))
            else:
                Message.SendMessage(int(self.q.getvalue('receiverId')), M_DATA , self.q.getvalue('message'))
        else:
            self.ResultText = "You are not authorized."

    def MsgGet(self):
        if Message.ClientID != 0:
            m = Message.SendMessage(M_BROKER, M_GETDATA)
            if m.Header.Type == M_DATA:
                self.ResultText = m.Data
        else:
            self.ResultText = "You are not authorized."

    def Connect(self):
        Message.SendMessage(M_BROKER, M_INIT)

    def History(self):
        Message.SendMessage(M_BROKER, M_HISTORY)


def main():
    q = cgi.FieldStorage()
    m = Messenger(q)

    MENU = {
        'sendmsg': m.MsgSend,
        'get': m.MsgGet,
        'connect': m.Connect,
        'history': m.History
    }

    try:
        MENU[q.getvalue('type')]()
    except Exception as e:
        pass
    m.PrintPage()


main()
