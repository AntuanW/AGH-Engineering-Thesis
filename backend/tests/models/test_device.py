import pytest
from app.models.device import Interface, InterfaceType


def test_interface_initializes_correctly_with_data():
    interface = Interface(type=InterfaceType.FA, value="0/1")
    assert interface.type == InterfaceType.FA
    assert interface.value == "0/1"

def test_interface_raises_value_error_on_invalid_name():
    with pytest.raises(ValueError):
        Interface(name="InvalidName")

def test_interface_repr_returns_correct_string():
    interface = Interface(type=InterfaceType.GI, value="0/1")
    assert repr(interface) == "Interface(GigabitEthernet0/1)"

def test_interface_str_returns_correct_string():
    interface = Interface(type=InterfaceType.GI, value="0/1")
    assert str(interface) == "GigabitEthernet0/1"

def test_interface_hash_returns_correct_hash():
    interface = Interface(type=InterfaceType.GI, value="0/1")
    assert hash(interface) == hash("GigabitEthernet0/1")

def test_interface_port_number_returns_correct_value():
    interface = Interface(type=InterfaceType.GI, value="0/1/16")
    assert interface.port_number() == 16

def test_interface_prefix_returns_correct_value():
    interface = Interface(type=InterfaceType.GI, value="0/1/5")
    assert interface.prefix() == "0/1/"

def test_interface_short_name_returns_correct_value():
    interface = Interface(type=InterfaceType.GI, value="0/1/1")
    assert interface.short_name() == "Gi0/1/1"