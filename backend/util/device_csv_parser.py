"""
This script takes a CSV file exported from the device feature sheet inserts it into the database.
https://docs.google.com/spreadsheets/d/1NQD9FikpNQElF-OhCDCEOAs8r089ZF-20Y2Koz7Q-C0
The database should be manually cleared before this operation.
"""

import  csv, pathlib, re
from app.models.device import InterfaceType, Interface



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
    for device in dr:
        ifaces = device["interfaces"].split(",")
        ifaces = [x.strip() for x in ifaces if x != ""]
        print(ifaces)
        ifaces = parse_ifaces(ifaces.copy())
        print(ifaces)




