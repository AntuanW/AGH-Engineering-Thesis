import netmiko
import time
import getpass

R1_IP = '172.17.145.30'
R1_PORT = 2009
R2_IP = '172.17.145.20'
R2_PORT = 2002

MODE_TS = 'generic_termserver_telnet'
MODE_DIRECT = 'cisco_ios'
CONN_MODE = MODE_TS

def connect(ip, pt, uname, upass):
    handler = netmiko.ConnectHandler(
        ip=ip, port=pt, username=uname, password=upass,
        device_type=CONN_MODE,
        global_delay_factor=3.0)
    time.sleep(1)
    read_channel = handler.read_channel()

    if read_channel.find("[yes/no]"):
        handler.write_channel('no\r')
        time.sleep(1)
    netmiko.redispatch(handler,device_type=MODE_DIRECT)
    return handler

def create_loopbacks(lnum):
    for n in range(lnum):
        yield f'interface loopback{n}'
        yield f'description Loop{n}'

def delete_loopbacks(lnum):
    for n in range(lnum):
        yield f'no interface loopback{n}'


with open('run_config.txt', 'r') as file:
    configs = file.readlines()


print( f'Connecting to lab 4.51/rack01 (IP: {R1_IP}, port: {R1_PORT})' )
# uname=input('login: ')
# upass=getpass.getpass('password: ')
uname='admin'
upass='admin'
cli_R1 = connect(R1_IP, R1_PORT, uname, upass)
if not cli_R1.check_enable_mode(): cli_R1.enable()



# print(cli_R1.send_config_set(configs))

print(cli_R1.send_command("show ip int brief"))

cli_R1.disconnect()