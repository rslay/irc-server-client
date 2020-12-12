from abc import ABCMeta, abstractproperty

class Connection(metaclass=ABCMeta):
    """Base class for IRC connections."""
    transmit_encoding = "utf-8"

    @abstractproperty
    def socket(self):
        "The socket for this connection"

    def __init__(self, reactor):
        self.reactor = reactor

    def encode(self, msg):
        """Encode a message for transmission."""
        return msg.encode(self.transmit_encoding)

    