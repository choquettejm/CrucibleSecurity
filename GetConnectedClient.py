import re
import getpass
import netmiko
import time
import sys
import logging
from netmiko import ConnectHandler

# gets connection information from user
WLCName = raw_input("Controller DNS name: ")
clientMAC = raw_input("Enter Client MAC Address (XX:XX:XX:XX:XX:XX): ")
#Checks MAC address format and errors if not correct
if re.match("[0-9a-f]{2}([:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", clientMAC.lower()):
    username = raw_input("username: ")
    password = getpass.getpass()
else:
    print(" ")
    print("That is not the correct MAC Address format.  Please try again....")
    exit()

# creates Netmiko connection profile
wlc = {'device_type': 'cisco_wlc',
    'host': WLCName,
    'username': username,
    'password': password,
    'global_delay_factor': 4
}
print(" ")
print(" ")
print("Connecting to " + WLCName + ".................................")
net_connect = ConnectHandler(**wlc)
print("Succesfully Connected to " + WLCName)
print(" ")
print("Checking for client " + clientMAC)
output = net_connect.send_command("show client summary ")
findclientmac = output.find(clientMAC)
#Checks to see if the MAC address is present
if output.find(clientMAC) != -1:
    print(" ")
    print("Device with MAC address " + clientMAC + " is connected to " + WLCName + ", getting client details.................")
    print(" ")
    clientdetail = net_connect.send_command("show client detail " + clientMAC)
    print(clientdetail)
else:
    print("Device with MAC address " + clientMAC + " is NOT found on " + WLCName)
time.sleep(3)
print("Disconnecting............................................")
net_connect.disconnect()
