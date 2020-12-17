// CppClient.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "pch.h"
#include "framework.h"
#include "CppClient.h"
#include "../MsgServer/Msg.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

void ProcessMessages()
{
    while (true)
    {
        if (Message::m_ClientID == 0) {
            break;
        }
        Message m = Message::Send(M_BROKER, M_GETDATA);
        switch (m.m_Header.m_Type)
        {
        case M_DATA:
        {
            cout << "\nMessage from User" << m.m_Header.m_From << ": " << m.m_Data << endl;
            break;
        }
        case M_CONFIRM:
        {
            Message::m_ClientID = 0;
            cout << "Disconnect successful";
            break;
        }

        default:
        {
            Sleep(100);
            break;
        }
        }
    }
}

void Interface()
{    
    int action;
    cout    << "1. Connect\n"
            << "2. Write private message\n"
            << "3. Write global message\n"
            << "0. Exit\n";

    cout << "\nChoose your Fighter: ";
    cin >> action;

    switch (action)
    {
    case 1: 
    {

        AfxSocketInit();
        Message m = Message::Send(M_BROKER, M_INIT);
        thread t(ProcessMessages);
        t.detach();
        cout << "Welcome to the club, User" << m.m_Header.m_To << endl;
        break;
    }
    case 2:
    {
        if (!Message::m_ClientID) {
            cout << "Please, connect to server" << endl;
            break;
        }
        string message;
        int recievierId;
        cout << "Write Buddie`s ID:";
        cin.ignore(256, '\n');
        cin >> recievierId;
        cin.ignore(256, '\n');
        cout << "\nWrite message to Buddie:\n" << recievierId;
        getline(cin, message, '\n');
        Message m = Message::Send(recievierId, M_DATA, message);
  
        break;
    }
    case 3:
    {
        if (!Message::m_ClientID) {
            cout << "Please, connect to server" << endl;
            break;
        }
        string message;
        cout << "Write message to Buddies:";
        cin.ignore(256, '\n');
        getline(cin, message, '\n');
        Message m = Message::Send(M_ALL, M_DATA, message);

        break;
    }
    case 0:
    {
        cout << "Goodbye, Buddie\n";
        Message m = Message::Send(M_BROKER, M_EXIT);
        
        return;
    }
    default:

        cout << "Try again";
        break;
    }
    
}

// The one and only application object
void Client()
{
    while (true)
    {
        Interface();
    }
}

CWinApp theApp;

using namespace std;

int main()
{
    int nRetCode = 0;

    HMODULE hModule = ::GetModuleHandle(nullptr);

    if (hModule != nullptr)
    {
        // initialize MFC and print and error on failure
        if (!AfxWinInit(hModule, nullptr, ::GetCommandLine(), 0))
        {
            // TODO: code your application's behavior here.
            wprintf(L"Fatal Error: MFC initialization failed\n");
            nRetCode = 1;
        }
        else
        {
            Client();
        }
    }
    else
    {
        // TODO: change error code to suit your needs
        wprintf(L"Fatal Error: GetModuleHandle failed\n");
        nRetCode = 1;
    }

    return nRetCode;
}
