import unittest
from bson import ObjectId

from app.config_upload.netmiko_config_builder import NetmikoConfigBuilder
from app.repository.topology_repository import TopologyRepository


class TestNetmikoConfigBuilder(unittest.TestCase):
    def test_get_commands(self):
        topology_repository = TopologyRepository()
        topology_id = '671e6c7c15f4350cff3d7770'
        topology = topology_repository.find_one({"_id": ObjectId(topology_id)})

        netmiko_config_builder: NetmikoConfigBuilder = NetmikoConfigBuilder()
        config_0 = netmiko_config_builder.get_config(topology['topology'][0]['dev_running_config'])

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
        netmiko_config_builder: NetmikoConfigBuilder = NetmikoConfigBuilder()
        device_type = netmiko_config_builder.get_device_type()
        assert device_type == "cisco_ios", f"Device type is not cisco_ios: {device_type}"

    def test_get_host(self):
        netmiko_config_builder: NetmikoConfigBuilder = NetmikoConfigBuilder()
        host = netmiko_config_builder.get_host()
        assert host == "192.168.1.1", f"Wrong host: {host}"

    def test_get_username(self):
        netmiko_config_builder: NetmikoConfigBuilder = NetmikoConfigBuilder()
        username = netmiko_config_builder.get_username()
        assert username == "admin", f"Wrong username: {username}"

    def test_get_password(self):
        netmiko_config_builder: NetmikoConfigBuilder = NetmikoConfigBuilder()
        password = netmiko_config_builder.get_password()
        assert password == "password", f"Wrong password: {password}"
