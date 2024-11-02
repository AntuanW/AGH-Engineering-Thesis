class NetmikoConfigBuilder:
    def get_config(self, device_running_config: list[str]) -> list[str]:
        print(device_running_config)
        return [line for line in device_running_config if line != '!']

