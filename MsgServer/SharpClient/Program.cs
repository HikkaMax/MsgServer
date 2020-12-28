using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using System.Net;
using System.Net.Sockets;

namespace SharpClient
{
    class Program
    {

        public static int m_ClientId = 0;
        static void ProcessMessage()
        {
            while (true)
            {
                if (m_ClientId == 0)
                {
                    break;
                }

                Message message = SendMessage(Convert.ToUInt32(Members.M_BROKER), Convert.ToUInt32(Messages.M_GETDATA));
                switch (message.m_Header.m_Type)
                {
                    case (uint)Messages.M_DATA:
                        {
                            Console.WriteLine("Message from:" + message.m_Header.m_From);
                            Console.WriteLine(message.m_Data);
                            break;
                        }
                    default:
                        {
                            Thread.Sleep(100);
                            break;
                        }
                }
            }
        }

        static Message SendMessage(uint To, uint MType, string Data = "")
        {
            IPEndPoint endPoint = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 12345);
            Socket s = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            s.Connect(endPoint);
            if (!s.Connected)
            {
                Console.WriteLine("Not connected");
                throw new Exception("Ошибка при подключении");
            }
            Message m = new Message(To, Convert.ToUInt32(m_ClientId), MType, Data);
            m.Send(s);
            m.Recieve(s);
            if (m.m_Header.m_Type == Convert.ToUInt32(Messages.M_INIT) && m_ClientId == 0)
            {
                m_ClientId = Convert.ToInt32(m.m_Header.m_To);
            }

            if (m.m_Header.m_Type == Convert.ToUInt32(Messages.M_EXIT))
            {
                m_ClientId = 0;
            }

            return m;
        }

        static void Main(string[] args)
        {
            while (true)
            {
                Thread t = new Thread(Program.ProcessMessage); ;
                Console.WriteLine("1. Connect\n 2. Write private message\n 3. Write global message\n 0. Exit\n");
                Console.WriteLine("\nChoose your Fighter: ");
                int action = Convert.ToInt32(Console.ReadLine());
                switch (action)
                {
                    case 1:
                        {
                            Message message = SendMessage(Convert.ToUInt32(Members.M_BROKER), Convert.ToUInt32(Messages.M_INIT));
                            Console.WriteLine("Welcome to the club, User" + m_ClientId);
                            t.Start();
                            break;
                        }
                    case 2:
                        {
                            Console.WriteLine("Write message to Buddies: ");
                            if (m_ClientId != 0)
                            {
                                SendMessage(Convert.ToUInt32(Members.M_ALL), Convert.ToUInt32(Messages.M_DATA), Console.ReadLine());
                            }
                            else
                            {
                                Console.WriteLine("Please, connect to server");
                            }
                            break;
                        }
                    case 3:
                        {
                            if (m_ClientId != 0)
                            {
                                Console.WriteLine("Write Buddie`s ID:");
                                uint userId = Convert.ToUInt32(Console.ReadLine());

                                Console.WriteLine("\nWrite message to Buddie:\n");
                                SendMessage(userId, Convert.ToUInt32(Messages.M_DATA), Console.ReadLine());
                            }
                            else
                            {
                                Console.WriteLine("Please, connect to server");
                            }
                            break;
                        }
                    case 0:
                        {
                            Console.WriteLine("Goodbye, Buddie\n");
                            SendMessage(Convert.ToUInt32(Members.M_BROKER), Convert.ToUInt32(Messages.M_EXIT));
                            break;
                        }
                }
            }
        }
    }
}
