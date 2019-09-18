#!/usr/bin/env python3
import http.server
import socketserver
import threading

def simple_server(port):
    print("serving at port", port)
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    server_thread = threading.Thread(target=httpd.serve_forever,daemon= True)
    server_thread.start()
    return server_thread, httpd

def main():
    print('starting the server')
    thread, server = simple_server(8080)
    print('this line is after the server started')

    input('==press enter to stop the server==')
    # server.shutdown()
    # thread.join()

    print('server shutdown')
    input('==press enter to exit==')


if __name__ == '__main__':
    main()