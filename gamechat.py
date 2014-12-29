import socket
import threading
import SocketServer

from willie.module import commands

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        response = "{}: {}".format(cur_thread.name, data)

        self.request.sendall(response)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        print "Received: {}".format(response)
    finally:
        sock.close()

def start():
    HOST, PORT = "0.0.0.0", 37477

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name

def stop():
    server.shutdown()

def setup(willie):
    start()

    # To send something
    # client(ip, port, "Hello World 1")

def shutdown(willie):
    stop()

@commands('startserver')
def startserver(bot, trigger):
    start()
    bot.say('Server started.')

@commands('stopserver')
def stopserver(bot, trigger):
    stop()
    bot.say('Server stopped.')