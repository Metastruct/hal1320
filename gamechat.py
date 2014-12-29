import socket
import threading
import SocketServer

from willie.module import commands

HOST, PORT = "0.0.0.0", 37477
server = None
_willie = None

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        response = "{}: {}".format(cur_thread.name, data)

        print "[GAME] Recieved: {}".format(response)
        _willie.msg('#ingame', response)
        
        self.request.sendall(response)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        #response = sock.recv(1024)
        #print "[GAME] Received: {}".format(response)
    finally:
        sock.close()

def start():
    try:
        global server
        server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
    
        server_thread.start()
        print "[GAME] Server loop running in thread:", server_thread.name

        return True
    except Exception, e:
        print "[GAME] Failed to start server:", e
        return False

def stop():
    try:
        server.shutdown()
        return True
    except Exception, e:
        print "[GAME] Failed to stop server:", e
        return False

def setup(willie):
    # Allows us to send messages from outside bot commands
    global _willie
    _willie = willie
    willie.join('#ingame')

    start()

    # To send something
    # client(ip, port, "Hello World 1")

def shutdown(willie):
    stop()

@commands('startserver')
def startserver(bot, trigger):
    if (trigger.admin):
        if (start()):
            bot.say('[GAME] Server started.')
        else:
            bot.say('[GAME] Server failed to start.')

@commands('stopserver')
def stopserver(bot, trigger):
    if (trigger.admin):
        if (stop()) :
            bot.say('[GAME] Server stopped.')
        else:
            bot.say('[GAME] Server failed to stop.')