import getpass
import netmiko
import time
import sys
import logging
from netmiko import ConnectHandler

# gets connection information from user
WLCName = raw_input("Controller DNS name: ")
APPattern = raw_input("Enter AP Search Pattern: ")
username = raw_input("username: ")
password = getpass.getpass()

# creates Netmiko connection profile
wlc = {'device_type': 'cisco_wlc',
    'host': WLCName,
    'username': username,
    'password': password,
    'global_delay_factor': 2
}
print "-----------------------------------------------"
print "Connecting to " + WLCName
net_connect = ConnectHandler(**wlc)
print "Succesfully Connected to " + WLCName
print "Sending command show ap summary " + APPattern
output = net_connect.send_command("show ap summary " + APPattern)
print output
time.sleep(3)
print "Disconnecting"
net_connect.disconnect()
print "-----------------------------------------------"
