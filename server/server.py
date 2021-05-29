from logging import basicConfig, info
from select import select

from .ServerSocket import ServerSocket
from .consts import ServerConsts, PacketDataConsts
from .packet_data import PacketData


class Server:
    def __init__(self, address=ServerConsts.DEFAULT_SERVER_ADDR, port=ServerConsts.DEFAULT_PORT):
        basicConfig(filename='server.log', filemode='w', format='%(name)s - %(levelname) - %(message)s')

        self.address = address
        self.port = port

        self.server = ServerSocket(bind_addr=bind_addr, bind_port=bind_port)

        self.sockets_list = [server.connection()]
        self.clients = dict()

        info(f'Listening on {bind_addr}:{bind_port}')

    def run(self):
        self.server.connection().listen()

        while True:
            # select(rlist, wlist, xlist)
            #   rlist - sockets for accepting incoming data
            #   wlist - sockets to send data into
            #   xlist - sockets to be monitored for exceptions
            # read_sockets = sockets for accepting incoming data
            # write_sockets = sockets ready for data to be sent through
            # exception_sockets = sockets that have exceptions
            read_sockets, write_sockets, exception_sockets = select(sockets_list, [], sockets_list)

            for socket in read_sockets:
                # Accept new connections
                if socket == server.connection():
                    client_socket, client_addr = socket.accept()

                    user_name = self.receive(client_socket, ServerConsts.USER_NAME_MAX_SIZE)
                    client_socket.send(ServerConsts.NEW_USER_HELLO_MSG.format(user_name=user_name,
                                                                              num_of_users_online=len(
                                                                                  sockets_list) - 1))
                    self.sockets_list.append(client_socket)
                    self.clients[client_socket] = user_name

                    info(f'New connection from: {user_name}')

                else:
                    received_data = receive_msg(socket)
                    if received_data.msg_data is False:
                        info(f'Closed connection from: {clients[socket]}')
                        self.sockets_list.remove(socket)
                        del self.clients[socket]
                    self.send_msg_to_recipient(data=received_data, clients=clients)

    @staticmethod
    def _receive(connection, msg_len: int) -> str:
        return connection.recv(msg_len).decode('utf-8')

    def receive_msg(self, client_sock):
        try:
            header_len = int(self._receive(client_sock, PacketDataConsts.HEADER_SIZE_FIELD))
            header_data = self._receive(client_sock, header_len)

            if not len(header_data):
                return False

            packet_data = PacketData(header_data=header_data)
            packet_data.msg = self._receive(client_sock, packet_data.msg_len)
            return packet_data
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def _send(sock, msg: str):
        sock.sendall(msg)

    def send_msg_to_recipient(self, data: PacketData, clients: dict):
        recipient_name = data.recp_name
        for sock, name in clients.items():
            if name == recipient_name:
                self._send(sock, data.build_msg())
                info(f'Message sent from {data.sender_name} to {data.recp_name}')