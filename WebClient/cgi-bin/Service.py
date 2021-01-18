# -*- coding: utf-8 -*-

import os, sys, re, codecs, binascii, cgi, cgitb, datetime, pickle
from msg import *
import requests
import json
import threading

cgitb.enable()
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
ClientID: int = 0


def DoRequest(method, cmd="", data=None):
    if data is None:
        data = {}
    try:
        url = 'http://localhost:8080/cgi-bin/WebServer.py'
        res = method(url + cmd, data=data)
        if res.status_code == 200:
            return json.loads(res.content)
    except Exception as ex:
        print(ex)


def Connect():
    q = '?type=connect'
    res = DoRequest(requests.get, q)
    return res['ClientID']


def MsgGet():
    q = '?type=get&ClientID=' + str(ClientID)
    res = DoRequest(requests.get, q)
    return res['msg']


def MsgSend(receiverId, message):
    q = f"""?type=sendmsg"""
    params = {
        "ClientID": str(ClientID),
        "message": message,
        "receiverId": str(receiverId)
    }
    res = DoRequest(requests.post, q, params)


def History():
    q = f"""?type=history&ClientID={str(ClientID)}"""
    res = DoRequest(requests.get, q)
    return res


def ProcessMessages():
    while True:
        try:
            print(MsgGet())
        except Exception:
            pass

        time.sleep(1000)


while True:
    print(
        "\n1.Connect to Server \n2.Send global message(only if connected) \n3.Send message to certain user(only if connected) \n4.Get history.\n")
    actionId = int(input())
    if (actionId == 1):
        ClientID = Connect()
        print(ClientID)
        t = threading.Thread(target=ProcessMessages)
        t.start()
    elif (actionId == 2):
        print("Write your message:")
        MsgSend(0, input())
    elif (actionId == 3):
        print("Write reсiever ID:")
        recieverId = int(input())
        print("Write message")
        MsgSend(recieverId, input())
    elif (actionId == 4):
        print(History())
    elif (actionId == 5):
        print(MsgGet())
    else:
        print("Action Unknown")
