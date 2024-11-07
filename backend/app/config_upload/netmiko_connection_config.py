class NetmikoConnectionConfig:
    def get_config(self, device_running_config: list[str]) -> list[str]:
        return [line for line in device_running_config if line != '!']

    def get_device_type(self):
        #return "cisco_ios"
        pass

    def get_host(self):
        #return "192.168.1.1"
        pass

    def get_username(self):
        #return "admin"
        pass

    def get_password(self):
        #return "password"
        pass
