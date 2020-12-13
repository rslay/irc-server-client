import socket
import sys
import time
import traceback
from threading import Thread

from Utils import log
from Utils import CONSTANTS as const
from Utils import connected


class IRC_connection:
    def __init__(self, user, host, nick):
        self.user = None
        self.host = host  # Client's hostname / ip
        self.nick = None  # Client's currently registered nickname
        self.send_queue = []  # Messages to send to client (strings)
        self.channels = {}  # Channels the client is in

    def __repr__(self):
        return f"<{self.__class__.__name__} user={self.user} host={self.host}>"

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

    soc.listen(const["MAX_CONNECTIONS"]) # queue up to MAX_CONNECTIONS requests
    log("Socket now listening")

    # infinite loop - open a new thread for every incoming request
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        try:
            Thread(target=client_thread, args=(connection, ip, port)).start()
        except:
            log(f"Thread did not start. {traceback.print_exc()}", "ERROR")

    soc.close()


def client_thread(connection, ip, port, max_buffer_size=5120):
    is_active = True

    log(f"Connected to {ip}:{port} in new thread", "CONNECT")

    while is_active:
        log(f"Waiting for message...", "MESSAGE")
        client_input = receive_message(connection)
        log(f"Received message", "MESSAGE")

        if client_input == False:
            log(f"Error occurred during communication with a user", "ERROR")
            connection.close()
            is_active = False
        elif client_input == None:
            pass # Nothing to do, user sent empty message
        elif "--QUIT--" in client_input:
            log(f"Client is requesting to quit", "CONNECT")
            connection.close()
            log(f"Connection {ip}:{port} closed", "CONNECT")
            is_active = False
        else:
            log(f"Broadcasting: {client_input}", "MESSAGE")
            connection.sendall(client_input.encode('utf-8'))


def receive_message(connection):
    try:
        # Receive header
        message_header = connection.recv(const["HEADER_LENGTH"]).decode('utf-8').strip()

        # If no data was received, client closed the connection
        if message_header == "":
            # log(f"Empty header", "INFO")
            return None

        # Get message length from the received header
        message_length = int(message_header)

        # log(f"Valid header, expecting message length of {message_header} bytes...", "INFO")

        # Receive all data for whole message
        request = connection.recv(message_length).decode('utf-8').strip()

        # log(f"Request received! {str(request)}", "INFO")

        return request
    except Exception as e:
        log(f"Error while receiving data: {str(e)}", "ERROR")
        return False

start_server()
