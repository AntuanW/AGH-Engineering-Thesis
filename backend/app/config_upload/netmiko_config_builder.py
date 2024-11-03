class NetmikoConfigBuilder:
    def get_config(self, device_running_config: list[str]) -> list[str]:
        return [line for line in device_running_config if line != '!']

    def get_device_type(self):
        return "cisco_ios"

    def get_host(self):
        return "192.168.1.1"

    def get_username(self):
        return "admin"

    def get_password(self):
        return "password"
