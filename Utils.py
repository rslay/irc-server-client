import os

CONSTANTS = {
    "MAX_CONNECTIONS": 6,
    "LISTEN_PORT": 8888,   # An arbitrary random port above 1000 to avoid needing elevated privileges
    "HOSTNAME": "0.0.0.0",  # 0.0.0.0 for all interfaces
    "HEADER_LENGTH": 256
}

connected = []

def clear():
    if os.name == 'nt': # Windows
        os.system("cls")
    else: # Every other OS type
        os.system("clear")

def init_msg(ip, port, version):
    clear()
    print(r'''
 ___ ____   ____    ____ _   _    _  _____   _
|_ _|  _ \ / ___|  / ___| | | |  / \|_   _| | |
 | || |_) | |     | |   | |_| | / _ \ | |   |_|
 | ||  _ <| |___  | |___|  _  |/ ___ \| |    _
|___|_| \_\\____|  \____|_| |_/_/   \_\_|   |_|
''')

    print('IRC Server running!')
    print(f'IP: {ip}:{port} | {version}\n')


def log(message, log_type=None):
    if not log_type:
        log_type = "INFO"

    print(f"[{log_type}] {message}")

