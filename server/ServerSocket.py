from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


class ServerSocket:
    def __init__(self, bind_addr: str = '127.0.0.1', bind_port: int = 55555):
        self.bind_addr = bind_addr
        self.bind_port = bind_port
        self._socket = None

    @property
    def connection(self):
        if self._socket:
            return self._socket
        else:
            self._socket = socket(AF_INET, SOCK_STREAM)
            self._socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            self._socket.bind((self.bind_addr, self.bind_port))


