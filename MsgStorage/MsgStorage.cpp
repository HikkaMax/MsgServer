// MsgStorage.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//

#include "pch.h"
#include "framework.h"
#include "MsgStorage.h"
#include "../MsgServer/Msg.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

void ProcessMessages()
{
    while (true)
    {
        Message m = Message::Send(M_BROKER, M_GETDATA);
        switch (m.m_Header.m_Type)
        {
        case M_DATA:
        {
            ofstream fout(std::to_string(m.m_Header.m_To) + ".txt", std::ios::app);
            fout << "Message from:" << m.m_Header.m_From << endl;
            fout << m.m_Data << endl;
            fout << "----------------" << endl;
            fout.close();
            break;
        }
        case M_HISTORY:
        {
            ifstream fin(std::to_string(m.m_Header.m_From) + ".txt");
            string file_contents{ istreambuf_iterator<char>(fin), istreambuf_iterator<char>() };
            if (!file_contents.empty()) {
                Message::Send(m.m_Header.m_From, M_DATA, file_contents);
            }
            else {
                cout << "User " << m.m_Header.m_From << " asked for chat history" << endl;
                Message::Send(m.m_Header.m_From, M_DATA, "Your history is empty"); 
            }
            fin.close();
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

void Database()
{
    cout << "You are a database" << endl;
    AfxSocketInit();
    Message m = Message::Send(M_BROKER, M_DATABASE_CONNECTION);
    thread t(ProcessMessages);
    t.detach();
    cout << "Your ID is: " << m.m_ClientID<< endl;
    while (true) {

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
            Database();
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
