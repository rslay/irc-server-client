import socket
import sys
import time
from threading import Thread

from .utils import log
from .utils import CONSTANTS as const, connected


class IRC_connection:
    def __init__(self, user, host, nick):
        self.user = None
        self.host = client_address  # Client's hostname / ip.
        self.nick = None  # Client's currently registered nickname
        self.send_queue = []  # Messages to send to client (strings)
        self.channels = {}  # Channels the client is in

    def __repr__(self):
        return f"<{self.__class__.__name__} user={user} host={host}>"

    __str__ = __repr__


def start_server():
    """
    Creates a socket that listens for multiple connections and starts a thread
    that waits for data, then the messages, and displays it.
    """
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    log("Socket created")

    try:
        soc.bind((
            const["HOSTNAME"], const["LISTEN_PORT"]
        ))
    except:
        log(f"Bind failed. {str(sys.exc_info())}", "ERROR")
        sys.exit(-1)

    soc.listen(const.MAX_CONNECTIONS) # queue up to MAX_CONNECTIONS requests
    log("Socket now listening")

    # infinite loop - do not reset for every requests
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])

        log(f"Connected with {ip}:{port}", "CONNECT")

        try:
            Thread(target=client_thread, args=(connection, ip, port)).start()
        except:
            log(f"Thread did not start. {traceback.print_exc()}", "ERROR")

    soc.close()

def client_thread(connection, ip, port, max_buffer_size = 5120):
    is_active = True
    while is_active:
        client_input = receive_input(connection, max_buffer_size)
        if "--QUIT--" in client_input:
            log(f"Client is requesting to quit", "CONNECT")
            connection.close()
            log(f"Connection {ip}:{port} closed", "CONNECT")
            is_active = False
        else:
            log(f"Processed result: {client_input}", "MESSAGE")
            connection.sendall("-".encode("utf8"))


start_server()