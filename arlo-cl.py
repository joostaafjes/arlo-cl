# arlo-cl.py / Arlo Command Line 
# Send Commands to your Arlo Environment via the command line
# https://github.com/jeffreydwalter/arlo
# Michael Urspringer / v0.1

from arlo import Arlo
import sys
import os
import errno
import argparse
import configparser


def getDeviceFromName(name,devices):
    for device in devices:
        if device['deviceName'] == name and device['deviceType'] != "siren":
            return(device)
    return("")


try:

    # Check command line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['list-devices', 'list-modes', 'get-deviceid', 'get-uniqueid', 'set-mode'])
    parser.add_argument('--devicetype', '-t', choices=['basestation', 'arlobridge', 'camera', 'lights', 'siren'], help='the type of the device, if empty: all devicetypes')
    parser.add_argument('--devicename', '-n', help='the name of the device, only devices of type "basestation" or "arlobridge" are allowed')
    parser.add_argument('--mode', '-m', choices=['aktiviert', 'deaktiviert', 'aktiviert_tag','aktiviert_ohne_terrasse', 'garten', 'garten_hinten'], help='the mode which should be set')
    parser.add_argument('--configfile', '-c', default='./arlo-cl.cfg', help='Path to config file, use ./arlo-cl.cfg if empty')
    args = parser.parse_args()

    command=args.command
    devicetype=args.devicetype
    devicename=args.devicename
    mode=args.mode
    configfile=args.configfile
  
    # Initialize config file
    if not os.path.isfile(configfile):
        print("Error: Config file "+configfile+" not found" )
        sys.exit(errno.ENOENT)
    config = configparser.ConfigParser()
    config.read(configfile)

    # Credentials for Arlo
    USERNAME = config.get("CREDENTIALS","USERNAME")
    PASSWORD = config.get("CREDENTIALS","PASSWORD")

    # Instantiating the Arlo object automatically calls Login(), which returns an oAuth token that gets cached.
    # Subsequent successful calls to login will update the oAuth token.
    arlo = Arlo(USERNAME, PASSWORD)
    # At this point you're logged into Arlo.
    
    # Get all devices
    devices = arlo.GetDevices('')

    if command == 'list-devices':
        # List all devices
        # Get the list of devices and filter on device type.
        # This will return an array which includes all of the devices's associated metadata.
        devices = arlo.GetDevices(devicetype)
        #print ("Device Name : Device Type : Device ID : Unique ID")
        for key in devices:
            print (key['deviceName']," : ", key['deviceType']," : ", key['deviceId']," : ", key['uniqueId'])

    elif command == 'list-modes':
        # List all modes for a specific device
        modes=arlo.GetAutomationDefinitions()
        #print (modes)
        for id in modes:
            #print (modes[id]['modes'])
            for mode in modes[id]['modes']:
                print(id," : ",mode['name']," : ",mode['id']," : ",mode['type'])
            print("----------------------------------")

    elif command == 'get-deviceid':
        # Get the Device ID of the device "devicename"
        devices = arlo.GetDevices(devicetype)
        for key in devices:
            if key['deviceName'] == devicename:
                print (key['deviceId'])

    elif command == 'get-uniqueid':
        # Get the Unique ID of the device "devicename"
        devices = arlo.GetDevices(devicetype)
        for key in devices:
            if key['deviceName'] == devicename:
                print (key['uniqueId'])

    elif command == 'set-mode' and mode == 'deaktiviert':
        device = getDeviceFromName("Home",devices)
        arlo.Disarm(device)
        device = getDeviceFromName("Bridge_AZMichael",devices)
        arlo.Disarm(device)
        device = getDeviceFromName("Bridge_AZSabine",devices)
        arlo.Disarm(device)

    elif command == 'set-mode' and mode == 'aktiviert':
        device = getDeviceFromName("Home",devices)
        arlo.Arm(device)
        device = getDeviceFromName("Bridge_AZMichael",devices)
        arlo.Arm(device)
        device = getDeviceFromName("Bridge_AZSabine",devices)
        arlo.Arm(device)

    elif command == 'set-mode' and mode == 'aktiviert_tag':
        device = getDeviceFromName("Home",devices)
        arlo.CustomMode(device,"mode6")  # Aktiviert_Tag
        device = getDeviceFromName("Bridge_AZMichael",devices)
        arlo.CustomMode(device,"mode8")  # Aktiviert_Tag
        device = getDeviceFromName("Bridge_AZSabine",devices)
        arlo.CustomMode(device,"mode2")  # Aktiviert_Tag

    elif command == 'set-mode' and mode == 'aktiviert_ohne_terrasse':
        device = getDeviceFromName("Home",devices)
        arlo.CustomMode(device,"mode5")  # Garten_Alle
        device = getDeviceFromName("Bridge_AZMichael",devices)
        arlo.CustomMode(device,"mode6")  # OhneTerrasse 
        device = getDeviceFromName("Bridge_AZSabine",devices)
        arlo.Arm(device)


    elif command == 'set-mode' and mode == 'garten':
        device = getDeviceFromName("Home",devices)
        arlo.CustomMode(device,"mode5")  # Garten_Alle
        device = getDeviceFromName("Bridge_AZMichael",devices)
        arlo.CustomMode(device,"mode4")  # Garten
        device = getDeviceFromName("Bridge_AZSabine",devices)
        arlo.Arm(device)

    elif command == 'set-mode' and mode == 'garten_hinten':
        device = getDeviceFromName("Home",devices)
        arlo.CustomMode(device,"mode4")  # Garten_2
        device = getDeviceFromName("Bridge_AZMichael",devices)
        arlo.Disarm(device)
        device = getDeviceFromName("Bridge_AZSabine",devices)
        arlo.Arm(device)

    else:
        # Should not happen ...
        print("This should not happen")

except Exception as e:
    print(e)