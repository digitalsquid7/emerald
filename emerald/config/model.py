class EmailConfig:
    def __init__(self, host, port, from_address, use_ssl):
        self.host = host
        self.port = port
        self.from_address = from_address
        self.use_ssl = use_ssl
