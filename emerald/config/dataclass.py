class EmailConfig:
    def __init__(self, host: str, port: int, from_address: str, use_ssl: bool):
        self.host = host
        self.port = port
        self.from_address = from_address
        self.use_ssl = use_ssl


class DatabaseConfig:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string


class AssetConfig:
    def __init__(self, html_path: str, notification_file: str):
        self.html_path = html_path
        self.notification_file = notification_file


class Config:
    def __init__(self, email: EmailConfig, database: DatabaseConfig, asset: AssetConfig):
        self.email = email
        self.database = database
        self.asset = asset
