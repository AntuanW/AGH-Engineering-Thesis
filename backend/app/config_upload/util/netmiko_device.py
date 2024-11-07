from netmiko import ConnectHandler


class NetmikoDevice:
    def __init__(self, device_type: str, host: str, username: str, password: str, config: list[str]):
        self.device_type = device_type
        self.host = host
        self.username = username
        self.password = password
        self.config = config
        self.connection = None

    def connect(self):
        self.connection = ConnectHandler(
            device_type=self.device_type,
            host=self.host,
            username=self.username,
            password=self.password
        )

    def disconnect(self):
        if self.connection:
            self.connection.disconnect()
            self.connection = None

    def send_config_commands(self):
        self.connection.send_config_set(self.config)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
