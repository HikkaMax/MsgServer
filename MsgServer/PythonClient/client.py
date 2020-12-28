import threading
from msg import *


def ProcessMessages():
	while True:
		if Message.ClientID == 0 :
			break
		m = Message.SendMessage(M_BROKER, M_GETDATA)
		if m.Header.Type == M_DATA:
			print("\nMessage from User " +  str(m.Header.From))
			print(m.Data)
		else:
			time.sleep(1)


def Client():
	Message.SendMessage(M_BROKER, M_INIT)
	t = threading.Thread(target=ProcessMessages)
	t.start()

while True:
	print("\n1. Connect\n2. Write private message\n3. Write global message\n0. Exit\n")
	print("\nChoose your Fighter:")
	actionId = int(input())
	if (actionId == 1):
		Client()
		print("Welcome to the club, User " + str(Message.ClientID))
	elif (actionId == 2):
		if (Message.ClientID == 0):
			print("Please, connect to server")
			continue
		print("Write Buddie`s ID:")
		recieverId = int(input())
		print("\nWrite message to Buddie:\n")
		Message.SendMessage(recieverId, M_DATA, input())
	elif (actionId == 3):
		if(Message.ClientID == 0):
			print("Please, connect to server")
			continue
		print("Write message to Buddies:")
		Message.SendMessage(M_ALL, M_DATA, input())
	elif (actionId == 0):
		print("Goodbye, Buddie\n")
		if (Message.ClientID != 0):
			Message.SendMessage(M_BROKER, M_EXIT)
	else:
		print("Action Unknown")
