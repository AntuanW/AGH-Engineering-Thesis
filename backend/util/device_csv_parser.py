"""
This script takes a CSV file exported from the device feature sheet inserts it into the database.
https://docs.google.com/spreadsheets/d/1NQD9FikpNQElF-OhCDCEOAs8r089ZF-20Y2Koz7Q-C0
The database should be manually cleared before this operation.
"""

import  csv, pathlib
from app.models.device import Interface, DeviceModel
from app.repository.device_repository import DeviceRepository
from app.running_config.util.device_config_types import DeviceType


def parse_ifaces(interface_names: list[str]):
    parsed_ifaces = []
    for iface_name in interface_names:
        if (dash_count := iface_name.count("-")) == 0 or dash_count >= 2:
            parsed_ifaces.append(Interface(iface_name))
            continue

        start_str, end_str = iface_name.split("-")
        start = Interface(start_str)
        # this enables a notation like Gi0/1/0-7
        end_port = int(end_str.split("/")[-1])
        for i in range(start.port_number(), end_port + 1):
            parsed_ifaces.append(Interface(type=start.type, value=start.prefix() + str(i)))

    return parsed_ifaces


filename = pathlib.Path(__file__).parent.joinpath("devices.csv")
with open(filename) as file:
    dr = csv.DictReader(file)
    models = []

    for device in dr:
        ifaces = device["interfaces"].split(",")
        ifaces = [x.strip() for x in ifaces if x != ""]
        ifaces = parse_ifaces(ifaces.copy())

        device_model = DeviceModel(
            name=device["name"],
            rack_id=device["rack_id"],
            device_type=DeviceType(device["device_type"]),
            interfaces=ifaces,
            commands=[]
        )
        models.append(device_model)

    print("Inserting to database...")
    repo = DeviceRepository()
    for device in models:
        print(f"{device.name:10}{device.interfaces}")
        repo.insert(device)




