import subprocess as sub
import optparse
import re

usage = """
-----------------------------------------------------------------------------------------------------
'USAGE'
python macchanger.py -i <interface> -m <choose_mac_address>				 										
python macchanger.py --interface <interface> --mac <choose_mac_address>   							
-----------------------------------------------------------------------------------------------------      
'NOTES'							 																			
1. A mac address starts with 00:...																					 																							
2. If you used this program with 'python3' you can get an error. This program is need to 'python'.
   But don't worry. Just check it anyway. Because this error is not really error. Just a bug.		
-----------------------------------------------------------------------------------------------------      
"""
print(usage)

def get_user_input():
	obj = optparse.OptionParser()
	obj.add_option("-i", "--interface", dest = "interface", help = "Choose your interface")
	obj.add_option("-m", "--mac", dest = "mac_address", help = "Choose your new MAC")
	return obj.parse_args()

def change_mac_address(iface, mac_addr):
	sub.call(["ifconfig", iface, "down"])
	sub.call(["ifconfig", iface, "hw", "ether", mac_addr])
	sub.call(["ifconfig", iface, "up"])

def control_new_mac(interface):
	ifconfig = sub.check_output(["ifconfig", interface])
	new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))
	if new_mac:
		return new_mac.group(0)
	else:
		return None
try:
	(usr_input, arguments) = get_user_input()
	change_mac_address(usr_input.interface, usr_input.mac_address)
	last_mac = control_new_mac(str(usr_input.interface))

	if last_mac == usr_input.mac_address:
		print("[*] Your new MAC address is ready! Please check it.")
	else:
		print("[!] Err! Please check it.")
except TypeError:
	print("[!] Please follow the usage instructions above. ")
