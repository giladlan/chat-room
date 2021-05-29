from logging import basicConfig, info
from select import select

from .ServerSocket import ServerSocket
from .consts import ServerConsts, PacketDataConsts
from .packet_data import PacketData


def receive(socket, msg_len: int) -> str:
    return socket.recv(msg_len).decode('utf-8')


def receive_msg(client_sock):
    try:
        header_len = int(receive(client_sock, PacketDataConsts.HEADER_SIZE_FIELD))
        header_data = receive(client_sock, header_len)

        if not len(header_data):
            return False

        packet_data = PacketData(header_data=header_data)
        packet_data.msg = receive(client_sock, packet_data.msg_len)
        return packet_data
    except Exception as e:
        print(e)
        return False


def send(sock, msg: str):
    sock.sendall(msg)


def send_msg_to_recipient(data: PacketData, clients: dict):
    recipient_name = data.recp_name
    for sock, name in clients.items():
        if name == recipient_name:
            send(sock, data.build_msg())
            info(f'Message sent from {data.sender_name} to {data.recp_name}')


def run_room(bind_addr, bind_port):
    # Config Logging
    basicConfig(filename='server.log', filemode='w', format='%(name)s - %(levelname) - %(message)s')

    # Start server
    server = ServerSocket(bind_addr=bind_addr, bind_port=bind_port)
    server.connection().listen()

    sockets_list = [server.connection()]
    clients = dict()

    info(f'Listening on {bind_addr}:{bind_port}')

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

                user_name = receive(client_socket, ServerConsts.USER_NAME_MAX_SIZE)
                client_socket.send(ServerConsts.NEW_USER_HELLO_MSG.format(user_name=user_name,
                                                                          num_of_users_online=len(sockets_list) - 1))
                sockets_list.append(client_socket)
                clients[client_socket] = user_name

                info(f'New connection from: {user_name}')
            else:
                received_data = receive_msg(socket)
                if received_data.msg_data is False:
                    info(f'Closed connection from: {clients[socket]}')
                    sockets_list.remove(socket)
                    del clients[socket]
                send_msg_to_recipient(data=received_data, clients=clients)

