import pytest
from unittest.mock import patch, MagicMock
from app.config_upload.util.netmiko_device import NetmikoDevice

@patch('app.config_upload.util.netmiko_device.ConnectHandler')
def test_connect_establishes_connection(MockConnectHandler):
    mock_connection = MagicMock()
    MockConnectHandler.return_value = mock_connection

    device = NetmikoDevice('cisco_ios', '192.168.1.1', 22, ['command1', 'command2'])
    device.connect()

    MockConnectHandler.assert_called_once_with(device_type='cisco_ios', ip='192.168.1.1', port=22)
    assert device.connection == mock_connection

@patch('app.config_upload.util.netmiko_device.ConnectHandler')
def test_disconnect_closes_connection(MockConnectHandler):
    mock_connection = MagicMock()
    MockConnectHandler.return_value = mock_connection

    device = NetmikoDevice('cisco_ios', '192.168.1.1', 22, ['command1', 'command2'])
    device.connect()
    device.disconnect()

    mock_connection.disconnect.assert_called_once()
    assert device.connection is None

@patch('app.config_upload.util.netmiko_device.ConnectHandler')
def test_send_config_commands_sends_commands(MockConnectHandler):
    mock_connection = MagicMock()
    MockConnectHandler.return_value = mock_connection

    device = NetmikoDevice('cisco_ios', '192.168.1.1', 22, ['command1', 'command2'])
    device.connect()
    device.send_config_commands()

    mock_connection.send_config_set.assert_called_once_with(['command1', 'command2'])

@patch('app.config_upload.util.netmiko_device.ConnectHandler')
def test_context_manager_works_correctly(MockConnectHandler):
    mock_connection = MagicMock()
    MockConnectHandler.return_value = mock_connection

    with NetmikoDevice('cisco_ios', '192.168.1.1', 22, ['command1', 'command2']) as device:
        assert device.connection == mock_connection

    mock_connection.disconnect.assert_called_once()
    assert device.connection is None