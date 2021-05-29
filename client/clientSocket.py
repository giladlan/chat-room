from socket import socket, AF_INET, SOCK_STREAM


class ClientSocket:
    def __init__(self, server_addr, server_port):
        self.server_addr = server_addr
        self.server_port = server_port
        self._socket = socket(AF_INET, SOCK_STREAM)

    def connect(self):
        self._socket.connect((self.server_addr, self.server_port))

    @property
    def connection(self):
        if self._socket:
            return self._socket
        else:
            self.connect()
            return self._socket
