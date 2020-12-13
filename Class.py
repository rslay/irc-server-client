import socket
import sys
import time

from .utils import log


class IRC_client:
    irc = socket.socket()

    def __init__(self, uname, client_socket, client_address):
        # Define the socket
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = client_socket

        self.username_header = uname['header']
        self.raw_username = uname['data']
        self.username = self.raw_username.decode('utf-8')

        self.ip = client_address[0]
        self.port = client_address[1]
        self.address = f'{self.ip}:{self.port}'


    def send(self, channel, msg):
        # Transfer data
        self.irc.send(bytes("PRIVMSG " + channel + " " + msg + "\n", "UTF-8"))

    def connect(self, server, port, channel, botnick, botpass, botnickpass):
        # Connect to the server
        log(f"Connecting to: {server}", "CONNECT")
        self.irc.connect((server, port))

        # Perform user authentication
        self.irc.send(bytes("USER " + botnick + " " + botnick +" " + botnick + " :python\n", "UTF-8"))
        self.irc.send(bytes("NICK " + botnick + "\n", "UTF-8"))
        self.irc.send(bytes("NICKSERV IDENTIFY " + botnickpass + " " + botpass + "\n", "UTF-8"))
        time.sleep(5)

        # join the channel
        self.irc.send(bytes("JOIN " + channel + "\n", "UTF-8"))

    def get_response(self):
        time.sleep(1)
        # Get the response
        resp = self.irc.recv(2040).decode("UTF-8")

        if resp.find('PING') != -1:
            self.irc.send(bytes('PONG ' + resp.split().decode("UTF-8") [1] + '\r\n', "UTF-8")) 

        return resp
