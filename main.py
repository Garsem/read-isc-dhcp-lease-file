#!/usr/bin/env python
import json
from datetime import datetime

class Lease:
    def __init__(self, ip, state, startTime, isOld, endTime, MAC, hostname, classIdentifier, manufacturer):
        self.ip = ip
        self.state = state
        self.startTime = startTime
        self.isOld = isOld
        self.endTime = endTime
        self.MAC = MAC
        self.hostname = hostname
        self.classIdentifier = classIdentifier
        self.manufacturer = manufacturer

class Manufacturer:
    def __init__(self, hex, name):
        self.hex = hex
        self.name = name

leases = list()
manufacturers = list()

def run():
    value = input("Please enter the path to your file: ")
    f = open(value, "r")
    f2 = open("oui.txt", "r", encoding="utf-8")

    generateManafacturers(f2.read().split("\n"))
    generateLeases(f.read().split("\n"))
    findOldLeases()
    outputJSON()

def generateManafacturers(lines):
    for line in lines:
        if "(hex)" in line:
            hexCode = line.split("\t\t")[0].split(" ")[0].replace("-",":")
            name = line.split("\t\t")[1]
            manufacturers.append(Manufacturer(hexCode, name))

def generateLeases(lines):
    ip = ""
    startTime = ""
    state = ""
    endTime = ""
    mac = ""
    hostname = ""
    classIdentifier = ""
    manufacturer = ""

    for line in lines:
        if "lease" in line and "#" not in line:
            ip = line.split(" ")[1]
        if "starts" in line:
            if "epoch" in line:
                startTime = int(line.split(" ")[4].replace(";",""))
            else:
                startTime = datetime.strptime((line.split(" ")[4] + " " + line.split(" ")[5]).replace(";", ""),"%Y/%m/%d %H:%M:%S")
        if "state" in line and "next" not in line and "rewind" not in line:
            state = line.split(" ")[4].replace(";", "")
        if "ends" in line:
            if "epoch" in line:
                endTime = int(line.split(" ")[4].replace(";",""))
            else:
                endTime = datetime.strptime((line.split(" ")[4] + " " + line.split(" ")[5]).replace(";", ""),"%Y/%m/%d %H:%M:%S")
        if "hardware" in line:
            mac = line.split(" ")[4].replace(";", "")
            for man in manufacturers:
                if mac[:8].upper() == man.hex:
                    manufacturer = man.name
                    break

        if "hostname" in line:
            hostname = line.split(" ")[3].replace(";", "").replace('"', "")
        if "class-identifier" in line:
            classIdentifier = line.split("=")[1].replace('"', "").replace(";","")
        
        if ip != "" and startTime != "" and state != "" and endTime != "" and mac != "" and classIdentifier != "":
            if state == "active":
                if hostname == "":
                    hostname = "No hostname"

                if manufacturer == "":
                    manufacturer = "No manufacturer"
                leases.append(Lease(ip, state, startTime, False, endTime, mac, hostname, classIdentifier, manufacturer))
            ip = ""
            startTime = ""
            state = ""
            endTime = ""
            mac = ""
            hostname = ""
            classIdentifier = ""
            manufacturer = ""

def findOldLeases():
    for i in range(len(leases)):
        if not leases[i].isOld:
            for j in range(i, len(leases)):
                if not leases[j].isOld:
                    if leases[i].ip == leases[j].ip and i != j:
                        if leases[i].startTime < leases[j].startTime:
                            leases[i].isOld = True
                        else:
                            leases[j].isOld = True

def outputJSON():
    jsonString = "["
    for lease in leases:
        if not lease.isOld:
            if not isinstance(lease.startTime, int):
                lease.startTime = str(lease.startTime)
                lease.endTime = str(lease.endTime)
            jsonString = jsonString + json.dumps(lease.__dict__) + ","

    jsonString = jsonString.rstrip(jsonString[-1])
    jsonString = jsonString + "]"
    print(jsonString)

run()
