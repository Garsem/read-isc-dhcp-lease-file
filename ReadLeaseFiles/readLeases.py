import re
from datetime import datetime


class DHCP_Lease_Read:

  def __init__(self, DHCP_LEASE_FILE, MAC_ADDRESS_FILE):
    self.DHCP_LEASE_FILE = DHCP_LEASE_FILE
    self.MAC_ADDRESS_FILE = MAC_ADDRESS_FILE

  def printDHCPLeaseFiles(self):
    print(self.DHCP_LEASE_FILE, self.MAC_ADDRESS_FILE)

  def extractDateAndTime(self, DateAndTime: list, leaseStart: bool = True):
    if leaseStart == True:
      currDate, currTime = DateAndTime[0]
      newDate = ['Start-Datum', currDate]
      newTime = ['Start-Zeit', currTime]
    else:
      currDate, currTime = DateAndTime[0]
      newDate = ['End-Datum', currDate]
      newTime = ['End-Zeit', currTime]

    return newDate + newTime

  def nearest(self, items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

  def removeTimeFromLeases(self, lst: list):
    find_remove_Time_And_Date = re.compile(r'\{\n\s\sstarts[\sa-z\/0-9\:]+;[\sa-z\/0-9\:]+;[\sa-z\/0-9\:]+;')
    ListWithoutTimeAndDate = []
    for item in lst:
      remove_Time_And_Date = re.sub(find_remove_Time_And_Date, '{', item)
      ListWithoutTimeAndDate.append(remove_Time_And_Date)

    return ListWithoutTimeAndDate

  def getNewestLeases(self, lst: list):
    find_Start_Date_and_Time = re.compile(r'starts\s\d\s([0-9\/]+\s[0-9\:]+)')
    IP_Addresses = []
    today = datetime.today()
    strToday = today.strftime("%Y/%m/%d %H:%M:%S")
    print(strToday)
    for items in lst:
      Start_Date_and_Time = find_Start_Date_and_Time.findall(items)
      if Start_Date_and_Time[0] <= strToday:
        IP_Addresses.append(items)

  def SortOutDuplicates(self, lst: list):
    print(len(lst))
    IP_Addresses = []
    index = 0
    print(len(IP_Addresses))
    for items in lst:
      if len(IP_Addresses) < 1:
        IP_Addresses.append(items)
        print(IP_Addresses)
      elif items[0] not in [IP_Addresses[0] for itemb in lst]:
        IP_Addresses.append(items)

    print(IP_Addresses)
    # for IP_Address in IP_Addresses:
    #   # print(IP_Address)
    #   print(items[0], IP_Address[0])
    #   if items[0] == IP_Address[0]:
    #     print("Hallo break")
    #     break
    #   else:
    #     print("Hallo Append")
    #     IP_Addresses.append(items)
    #     continue

    # IP_Addresses.insert(len(IP_Addresses), items)
    # print(items)

    # print(items[0], IP_Address[0])
    # print(IP_Address[len(IP_Addresses)])
    # if items[0] in IP_Address[0]:
    #   print(items[0], IP_Addresses[0])
    #   print(IP_Addresses)
    #   continue
    # else:
    #   IP_Addresses.append(items)

    # print(len(IP_Addresses))
    # elif items[0] is IP_Addresses[0]:
    #   continue
    # else:
    #   continue

    # print(len(IP_Addresses))
    # print(IP_Addresses)

  def listToDict(self, lst):
    op = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return op

  def ReadDHCPLeaseFile(self):
    print("Hallo")
    # Get all active IP-Adresses
    find_all_active_leases = re.compile(r'[a-z]+\s[\.\d]+\s+\{[\n\s\w\/\:\;]+?active[\n\s\w\/\:\;\"\\\|\-\=\.\~\[]+[\n\s\w\/\:\;\"\\\|\-\=\.\~\[]+?\}')
    find_ip_addresses = re.compile(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
    find_Start_Date_and_Time = re.compile(r'starts\s\d\s([0-9\/]+)\s([0-9\:]+)')
    find_End_Date_and_Time = re.compile(r'ends\s\d\s([0-9\/]+)\s([0-9\:]+)')
    find_Mac_Address = re.compile(r'hardware\sethernet\s([0-9a-f\:]+)')
    find_Vendor_Class_Indentifier = re.compile(r'set\svendor\-class\-identifier\s=\s\"([0-9A-Za-z\s\-\.]+)')
    find_Client_Hostname = re.compile(r'set\svendor\-class\-identifier\s=\s\"([0-9A-Za-z\s\-\.]+)')

    with open(self.DHCP_LEASE_FILE, 'r') as f:
      DHCP_LEASES = f.read()

    all_active_leases = find_all_active_leases.findall(DHCP_LEASES)

    all_active_leases.sort()

    with open('leases_with_dublicates.txt', 'w') as f:
      for item in all_active_leases:
        f.write(item + "\n")

    active_leases_without_date = self.removeTimeFromLeases(all_active_leases)
    # print(active_leases_without_date)

    print(len(list(set(active_leases_without_date))))
    currentLeases = list(set(active_leases_without_date))
    currentLeases.sort()
    with open('leases_without_dublicates.txt', 'w') as f:
      for item in currentLeases:
        f.write(item + "\n")
    # for item in currentLeases:
    #   print(item)

    # define list
    # l = ['Hardik', 'Rohit', 'Rahul', 'Virat', 'Pant']
    #
    # i = 0
    # while i < len(l):
    #
    #   # replace hardik with shardul
    #   if l[i] == 'Hardik':
    #     l[i] = 'Shardul'
    #
    #   # replace pant with ishan
    #   if l[i] == 'Pant':
    #     l[i] = 'Ishan'
    #
    #   i += 1
    #
    # # print list
    # print(l)

    # print(currentLeases)
    #
    # for item1 in currentLeases:
    #   for item2 in all_active_leases:
    #     if item1[0] == item2[0]:
    #       item1 = item2

    # for item2, item in all_active_leases, currentLeases:
    #   print(item, item2)
    # if item[0] == item2:
    #   item = item2
    # else:
    #   continue
    #
    # print(item)

    # print(all_active_leases)

    # self.SortOutDuplicates(all_active_leases)

    active_leases = []
    filter_active_leases = []
    dict_active_leases = {}

    for ms in all_active_leases:
      ip_addresses = find_ip_addresses.findall(ms)
      Start_Date_and_Time = find_Start_Date_and_Time.findall(ms)
      End_Date_and_Time = find_End_Date_and_Time.findall(ms)
      Mac_Address = find_Mac_Address.findall(ms)
      Client_Hostname = find_Client_Hostname.findall(ms)
      if not Client_Hostname:
        Client_Hostname = ['No-Hostname']
      Vendor_Class_Indentifier = find_Vendor_Class_Indentifier.findall(ms)
      if not Vendor_Class_Indentifier:
        Vendor_Class_Indentifier = ["No-Vendor-Class"]
      current_leases = ip_addresses + Start_Date_and_Time + End_Date_and_Time + Mac_Address + Client_Hostname + Vendor_Class_Indentifier
      filter_active_leases.append(current_leases)

    self.SortOutDuplicates(filter_active_leases)
    # self.getNewestLeases(all_active_leases)

    for ms in all_active_leases:
      ip_addresses = find_ip_addresses.findall(ms)
      ip_addresses.insert(0, 'IP-Address')
      Start_Date_and_Time = self.extractDateAndTime(find_Start_Date_and_Time.findall(ms))
      End_Date_and_Time = self.extractDateAndTime(find_End_Date_and_Time.findall(ms), False)
      Mac_Address = find_Mac_Address.findall(ms)
      Mac_Address.insert(0, 'MAC-Address')
      Client_Hostname = find_Client_Hostname.findall(ms)
      if not Client_Hostname:
        Client_Hostname = ['No-Hostname']
        Client_Hostname.insert(0, 'Client-Hostname')
      else:
        Client_Hostname.insert(0, 'Client-Hostname')
      Vendor_Class_Indentifier = find_Vendor_Class_Indentifier.findall(ms)
      if not Vendor_Class_Indentifier:
        Vendor_Class_Indentifier = ["No-Vendor-Class"]
        Vendor_Class_Indentifier.insert(0, 'Vendor-Class')
      else:
        Vendor_Class_Indentifier.insert(0, 'Vendor-Class')
      current_leases = ip_addresses + Start_Date_and_Time + End_Date_and_Time + Mac_Address + Client_Hostname + Vendor_Class_Indentifier
      active_leases.append(current_leases)
      # print(active_leases)

    # print(active_leases)

    # for index, leases in enumerate(active_leases):
    #   if index <= len(active_leases):
    #     dict_active_leases['index' + str(index)] = self.listToDict(leases)
    # leases.insert(0, 'index' + str(index))
    # dict_active_leases.update(self.listToDict(leases))

    # print(dict_active_leases)
    # print(all_active_leases)
