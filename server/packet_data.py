class PacketData:
    def __init__(self, header_data):
        self._header_data = header_data
        self.sender_name = None
        self.recp_name = None
        self.msg_len = None
        self.msg_data = None
        self.parse()

    def parse(self):
        sender_name_len = self._header_data[:].strip
        self.sender_name = self._header_data[2:2 + sender_name_len].strip

        recp_name_len = self._header_data[2 + sender_name_len:2].strip
        self.recp_name = self._header_data[2:2 + recp_name_len].strip

        self.msg_len = self._header_data[recp_name_len + 2:].strip

    def set_msg_data(self, msg_data):
        self.msg_data = msg_data

    def build_msg(self):
        header = len(self.sender_name) + self.sender_name + len(self.recp_name) + self.recp_name
        return f'{len(header)} + {header} + {self.msg_data}'
