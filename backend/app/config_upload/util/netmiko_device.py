from netmiko import ConnectHandler
import netmiko
import time


class NetmikoDevice:
    def __init__(self, device_type: str, ip: str, port: int, config: list[str]):
        # self.ip_address = None
        self.device_type = device_type
        self.ip = ip
        self.port = port
        self.config = config
        self.connection = None

    def send_config(self):
        # print(self.ip_address)
        print("send_cofig dupa dupa dupa")
        print(self.device_type)
        print(self.ip)
        print(self.port)

        self.connection = ConnectHandler(
            device_type=self.device_type,
            ip=self.ip,
            port=self.port,
            global_delay_factor=3.0,
            username='admin',
            password='admin'
        )

        time.sleep(1)
        read_channel = self.connection.read_channel()

        if read_channel.find("[yes/no]"):
            self.connection.write_channel('no\r')
            time.sleep(1)
        netmiko.redispatch(self.connection, device_type='cisco_ios')

        if not self.connection.check_enable_mode():
            self.connection.enable()
        self.connection.send_config_set(self.config)
        self.connection.disconnect()
    #
    # def disconnect(self):
    #     if self.connection:
    #         self.connection.disconnect()
    #         self.connection = None
    #
    # def send_config_commands(self):
    #     self.connection.send_config_set(self.config)
    #
    # def __enter__(self):
    #     self.connect()
    #     return self
    #
    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     self.disconnect()
