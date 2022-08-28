import os
from .readLeases import DHCP_Lease_Read

dirname = os.path.dirname(__file__)
dhcpdLeases = os.path.join(dirname, '../Lease_and_MAC-Adress_Files/dhcpd.leases')
ouiFile = os.path.join(dirname, '../Lease_and_MAC-Adress_Files/oui.txt')

def exportReadLeases():
  DHCP_Leases = DHCP_Lease_Read(dhcpdLeases, ouiFile)
  return DHCP_Leases.ReadDHCPLeaseFile()