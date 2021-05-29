"""
Const file for server code
"""


class ServerConsts:
    USER_NAME_MAX_SIZE = 6
    NEW_USER_HELLO_MSG: 'Hello {username}, Welcome to the chat room, there are currently {num_of_users_online} users ' \
                        'online '


class PacketDataConsts:
    HEADER_SIZE_FIELD = 2
