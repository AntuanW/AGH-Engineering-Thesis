import netmiko
import time
import getpass

R1_IP = '172.17.184.10'
R1_PORT = 2001
MODE_TS = 'generic_termserver_telnet'
MODE_DIRECT = 'cisco_ios'
CONN_MODE = MODE_TS

def connect(ip, pt, uname, upass):
    retval = netmiko.ConnectHandler(
        ip=ip, port=pt, username=uname, password=upass,
        device_type=CONN_MODE,
        global_delay_factor=3.0 if CONN_MODE==MODE_TS else 1.0 )
    if CONN_MODE == MODE_TS:
        retval.write_channel('\r')
        time.sleep(1)
        retval.write_channel('\r')
        time.sleep(1)
        print(retval.read_channel())
        netmiko.redispatch(retval,device_type=MODE_DIRECT)
    else:
        retval.write_channel('\r')
        time.sleep(1)
        print(retval.read_channel())
    return retval

def create_loopbacks(lnum):
    for n in range(lnum):
        yield f'interface loopback{n}'
        yield f'description Loop{n}'

def delete_loopbacks(lnum):
    for n in range(lnum):
        yield f'no interface loopback{n}'



print( f'Connecting to lab 4.51/rack01 (IP: {R1_IP}, port: {R1_PORT})' )
uname=input('login: ')
upass=getpass.getpass('password: ')

cli_R1 = connect(R1_IP, R1_PORT, uname, upass)
if not cli_R1.check_enable_mode(): cli_R1.enable()

print( 'List of interfaces:' )
retval = cli_R1.send_command('show ip interface brief\n')
print( retval )

print( 'Interface descriptions:' )
retval = cli_R1.send_command('show interface description')
print( retval )

# Lepiej posłużyć się jedną długą listą, niż w pętli tworzyć pojedyncze interfejsy
# Powód: szczególnie przy zdalnym połączeniu przez VPN do TS i dalej do konsoli zdarzają się timeouty
print( 'Adding 20 loopbacks...' )
loop_commands = list(create_loopbacks(20))
print(loop_commands)
print( cli_R1.send_config_set(loop_commands) )

print( 'List of interfaces:' )
retval = cli_R1.send_command('show ip interface brief')
print( retval )

print( 'Interface descriptions:' )
retval = cli_R1.send_command('show interface description')
print( retval )

print( 'Deleting loopbacks...' )
loop_commands = list(delete_loopbacks(20))
print(loop_commands)
print( cli_R1.send_config_set(loop_commands) )

print( 'Closing connection' )
cli_R1.disconnect()