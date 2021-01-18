# -*- coding: utf-8 -*-

import os, sys, re, codecs, binascii, cgi, cgitb, datetime, pickle
from msg import *
import json

cgitb.enable()
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())


class Messenger:
    def __init__(self, q):
        self.q = q
        Message.ClientID = int(q.getvalue('ClientID', 0))
        if Message.ClientID == 0:
            Message.SendMessage(M_BROKER, M_INIT)

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
                print("Content-type: application-json; charset=utf-8\n\n")
                r = {'msg': m.Data}
                print(json.dumps(r))
        else:
            self.ResultText = "You are not authorized."

    def Connect(self):
        Message.SendMessage(M_BROKER, M_INIT)
        print("Content-type: application-json; charset=utf-8\n\n")
        r = {'ClientID': Message.ClientID}
        print(json.dumps(r))

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

main()
