import unittest
from bson import ObjectId

from app.config_upload.netmiko_connection_config import NetmikoConnectionConfig
from app.repository.topology_repository import TopologyRepository


class TestNetmikoConfigBuilder(unittest.TestCase):
    def test_get_commands(self):
        topology_repository = TopologyRepository()
        topology_id = '671e6c7c15f4350cff3d7770'
        topology = topology_repository.find_one({"_id": ObjectId(topology_id)})

        netmiko_connection_config: NetmikoConnectionConfig = NetmikoConnectionConfig()
        config_0 = netmiko_connection_config.get_config(topology['topology'][0]['dev_running_config'])

        expected_config_0 = [
            "version 15.4",
            "no service timestamps log datetime msec",
            "no service timestamps debug datetime msec",
            "no service password-encryption",
            "hostname Router",
            "ip cef",
            "no ipv6 cef",
            "spanning-tree mode pvst",
            "interface GigabitEthernet0/0/0",
            "ip address 13.0.0.1 255.255.255.252",
            "duplex auto",
            "speed auto",
            "interface GigabitEthernet0/0/1",
            "ip address 11.0.0.2 255.255.255.252",
            "duplex auto",
            "speed auto",
            "interface GigabitEthernet0/0/2",
            "no ip address",
            "duplex auto",
            "speed auto",
            "shutdown",
            "interface Vlan1",
            "no ip address",
            "shutdown",
            "ip classless",
            "ip flow-export version 9",
            "line con 0",
            "line aux 0",
            "line vty 0 4",
            "login",
            "end"
        ]
        assert config_0 == expected_config_0, f"Wrong config: {config_0}"

    def test_get_device_type(self):
        # netmiko_connection_config: NetmikoConnectionConfig = NetmikoConnectionConfig()
        # device_type = netmiko_connection_config.get_device_type()
        # assert device_type == "cisco_ios", f"Device type is not cisco_ios: {device_type}"
        pass

    def test_get_host(self):
        # netmiko_connection_config: NetmikoConnectionConfig = NetmikoConnectionConfig()
        # host = netmiko_connection_config.get_host()
        # assert host == "192.168.1.1", f"Wrong host: {host}"
        pass

    def test_get_username(self):
        # netmiko_connection_config: NetmikoConnectionConfig = NetmikoConnectionConfig()
        # username = netmiko_connection_config.get_username()
        # assert username == "admin", f"Wrong username: {username}"
        pass

    def test_get_password(self):
        # netmiko_connection_config: NetmikoConnectionConfig = NetmikoConnectionConfig()
        # password = netmiko_connection_config.get_password()
        # assert password == "password", f"Wrong password: {password}"
        pass
