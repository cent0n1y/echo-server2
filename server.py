import socket
import threading
import sys

CHAT_VIEWER = True
SERVER_IS_ON = True
SOCK_LISTENING = True
BROADCAST_MESSAGE = b'online'
CLIENTS_LIST = []


class AdminThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
import logging

logging.basicConfig(filename="client.log", level=logging.INFO)


def set_host():
    while True:
        print('Type HOST below or write "def" for default HOST')
        try:
            msg = input()
            if msg == "def":
                host = '127.0.0.1'
            else:
                host = msg
            break
        except:
            log = 'You enter not supported HOST, please try again'
            logging.error(log)
            print(log)
    return host


def set_port():
    while True:
        print('Type PORT below or write "def" for default PORT')
        try:
            msg = input()
            if msg == "def":
                port = 9090
                break
            elif msg is not int:
                print('You enter not supported PORT, please try again')
            else:
                port = msg
                break
        except:
            log = 'You enter not supported PORT, please try again'
            logging.error(log)
            print(log)
    return port


def set_login():
    while True:
        print('Type your login')
        try:
            msg = input()
            if type(msg) is not str:
                print("not str")
                print('You enter not supported login, please try again')
            else:
                login = msg
                break
        except:
            log = 'You enter not supported login, please try again'
            logging.error(log)
            print(log)
    return login


def set_passwd():
    while True:
        print('Type your password')
        try:
            msg = input()
            if type(msg) is not str:
                print('You enter not supported password, please try again')
            else:
                passwd = msg
                break
        except:
            log = 'You enter not supported login, please try again'
            logging.error(log)
            print(log)
    return passwd


LOGIN = set_login()
PASSWD = set_passwd()
HOST = set_host()
PORT = set_port()

sock = socket.socket()
try:
    sock.connect((HOST, PORT))
    data = ''
    print('Write your message below:')

    while True:
        msg = input()
        if msg == 'exit':
            break
        data += msg
        log = "Current message: %s\n You can continue write messages, or write 'exit' for sending message" % data
        logging.info(log)
        print(log)

    try:
        data = "%s:%s:%s" % (LOGIN, PASSWD, data)
        sock.send(data.encode())
        log = 'Your message was sent successfully'
        logging.info(log)
        print(log)
    except Exception as ex:
        logging.error(ex)
        print(ex)

    try:
        msg = sock.recv(1024).decode()
        log = '\nYou have receive new message: \n%s' % msg
        logging.info(log)
        print(log)
    except Exception as ex:
        logging.error(ex)
        print(ex)

    sock.close()


except Exception as ex:
    log = "Failed to connect to server\nException is: %s" % ex
    logging.error(log)
    print(log)

    def run(self):
        global CHAT_VIEWER
        global SERVER_IS_ON
        global SOCK_LISTENING
        while True:
            admin_panel = ("===\n"
                           "Type 'chat' for chat viewing\n"
                           "Type 'pause' to pause port listening\n"
                           "Type 'shutdown' for stopping server\n"
                           "===")
            print(admin_panel)
            command = input("Command:\n")
            if command == 'chat':
                if CHAT_VIEWER:
                    CHAT_VIEWER = False
                    print("Chat view:", CHAT_VIEWER)
                else:
                    CHAT_VIEWER = True
                    print("Chat view:", CHAT_VIEWER)
            elif command == 'pause':
                if SOCK_LISTENING:
                    SOCK_LISTENING = False
                    print("Port listening:", SOCK_LISTENING)
                else:
                    SOCK_LISTENING = True
                    print("Port listening:", SOCK_LISTENING)
            elif command == 'shutdown':
                SERVER_IS_ON = False
                print("Shutting down")
                sys.exit(1)
            else:
                print("Unknown command, enter a correct one")
                print(admin_panel)


class ClientThread(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.daemon = True
        self.conn = conn
        self.addr = addr

    def run(self):
        global BROADCAST_MESSAGE
        global CLIENTS_LIST
        text = "Connection from %s:%s" % (self.addr[0], self.addr[1])
        print(text)
        try:
            while True:
                if not SERVER_IS_ON:
                    print("Trying to exit")
                    break
                data = self.conn.recv(1024)
                if not data:
                    break
                msg = data.decode()
                BROADCAST_MESSAGE = data
                for client in CLIENTS_LIST:
                    client.send(BROADCAST_MESSAGE)
                if CHAT_VIEWER:
                    print(msg)
        except:
            client_socket = "%s:%s" % (self.addr[0], self.addr[1])
            print("Client", client_socket, "disconnected")
        self.conn.close()
        CLIENTS_LIST.remove(self.conn)


AdminThread().start()
sock = socket.socket()
sock.bind(('localhost', 9090))

while True:
    if not SERVER_IS_ON:
        print("Trying to exit")
        break
    sock.listen(0)
    conn, addr = sock.accept()
    CLIENTS_LIST.append(conn)
    ClientThread(conn, addr).start()
