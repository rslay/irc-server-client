CONSTANTS = {
    "MAX_CONNECTIONS": 6,
    "LISTEN_PORT": 8888,   # An arbitrary random port above 1000 to avoid needing elevated privileges
    "HOSTNAME": "0.0.0.0"  # 0.0.0.0 for all interfaces
}

connected = []


def log(message, log_type=None):
    if not log_type:
        log_type = "LOG"

    print(f"[{log_type}] {message}")

