import getpass
import netmiko
import time
import sys
import logging
from netmiko import ConnectHandler

# gets connection information from user
WLCName = raw_input("Controller DNS name: ")
username = raw_input("username: ")
password = getpass.getpass()

# creates Netmiko connection profile
wlc = {'device_type': 'cisco_wlc',
    'host': WLCName,
    'username': username,
    'password': password,
    'global_delay_factor': 2
}
print "Connecting to " + WLCName
net_connect = ConnectHandler(**wlc)
print "Succesfully Connected to " + WLCName
print "getting " + WLCName + " Controller Version and Model"
# Get Controller Software Version
sysinfo = net_connect.send_command("show sysinfo")
PVIndexBeg = sysinfo.find("Product Version", 0, len(sysinfo))
PVIndexEnd = PVIndexBeg + 59
# Get Controller Product ID
ProdID = net_connect.send_command("show inventory")
PIDIndexBeg = ProdID.find("PID:", 0, len(ProdID))
PIDIndexEnd = PIDIndexBeg + 18
# Get Controller Field Recovery Software Version if 5508 or 2504
if ("5508" or "2504") in ProdID:
    Recoverysysinfo = net_connect.send_command("show sysinfo")
    RecoverIndexBeg = Recoverysysinfo.find("Field Recovery", 0, len(Recoverysysinfo))
    RecoverIndexEnd = RecoverIndexBeg + 59
#print Results
print "-----------------------------------------------"
print " "
print (sysinfo[PVIndexBeg:PVIndexEnd])
if ("5508" or "2504") in ProdID:
    print (Recoverysysinfo[RecoverIndexBeg:RecoverIndexEnd])
print (ProdID[PIDIndexBeg:PIDIndexEnd])
print " "
print "-----------------------------------------------"
sysinfo = net_connect.send_command("q")
time.sleep(3)
print "Disconnecting"
net_connect.disconnect()
