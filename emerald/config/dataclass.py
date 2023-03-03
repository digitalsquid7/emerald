from dataclasses import dataclass


@dataclass
class EmailConfig:
    host: str
    port: int
    from_address: str
    use_ssl: bool


@dataclass
class DatabaseConfig:
    connection_string: str


@dataclass
class AssetConfig:
    html_path: str
    notification_file: str


@dataclass
class Config:
    email: EmailConfig
    database: DatabaseConfig
    asset: AssetConfig
