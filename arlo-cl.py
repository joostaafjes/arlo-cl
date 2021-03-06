#!/usr/bin/env python3

# arlo-cl.py / Arlo Command Line 
# Send Commands to your Arlo Environment via the command line
# https://github.com/jeffreydwalter/arlo
# Michael Urspringer / v0.3

from arlo import Arlo
import sys
import os
import errno
import argparse
import configparser
import base64



def getDeviceFromName(name,devices):
    for device in devices:
        if device['deviceName'] == name and device['deviceType'] != "siren":
            return(device)
    return("")


try:

    # Check command line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['list-devices', 'list-modes', 'get-deviceid', 'get-uniqueid', 'set-mode', 'set-brightness'])
    parser.add_argument('--devicetype', '-t', choices=['basestation', 'arlobridge', 'camera', 'lights', 'siren'], help='the type of the device, if empty: all devicetypes')
    parser.add_argument('--devicename', '-n', help='the name of the device, only devices of type "basestation" or "arlobridge" are allowed')
    parser.add_argument('--mode', '-m', choices=['aktiviert', 'deaktiviert', 'aktiviert_tag','aktiviert_ohne_terrasse', 'garten', 'garten_hinten'], help='the mode which should be set')
    parser.add_argument('--brightness', '-b', default='0', choices=['-2', '-1', '0', '1', '2'], help='the brightness value which should be set')
    parser.add_argument('--configfile', '-c', default='./arlo-cl.cfg', help='Path to config file, use ./arlo-cl.cfg if empty')
    args = parser.parse_args()

    command=args.command
    devicetype=args.devicetype
    devicename=args.devicename
    mode=args.mode
    brightness=args.brightness
    configfile=args.configfile
  
    # Initialize config file
    if not os.path.isfile(configfile):
        print("Error: Config file "+configfile+" not found" )
        sys.exit(errno.ENOENT)
    config = configparser.ConfigParser()
    config.read(configfile)

    # Credentials for Arlo
    USERNAME = config.get("CREDENTIALS","USERNAME")
    PASSWORD = str(base64.b64encode(config.get("CREDENTIALS","PASSWORD").encode("utf-8")), "utf-8")

    # Base Station (currently only one base station supported!)
    BASESTATIONNAME = config.get("BASESTATION","NAME")

    # Instantiating the Arlo object automatically calls Login(), which returns an oAuth token that gets cached.
    # Subsequent successful calls to login will update the oAuth token.
    arlo = Arlo(USERNAME, PASSWORD)
    # At this point you're logged into Arlo.
    
    # Get all device objects
    devices = arlo.GetDevices(devicetype)

    # Get base station object
    basestation = getDeviceFromName(BASESTATIONNAME,devices)

    if command == 'list-devices':
        # List all devices
        # Get the list of devices and filter on device type.
        # This will return an array which includes all of the devices's associated metadata.
        for device in devices:
            print (device['deviceName']," : ", device['deviceType']," : ", device['deviceId']," : ", device['uniqueId'])

    elif command == 'list-modes':
        # List all modes for a specific device
        modes=arlo.GetAutomationDefinitions()
        for id in modes:
            for mode in modes[id]['modes']:
                print(id," : ",mode['name']," : ",mode['id']," : ",mode['type'])
            print("----------------------------------")

    elif command == 'get-deviceid':
        # Get the Device ID of the device "devicename"
        for key in devices:
            if key['deviceName'] == devicename:
                print (key['deviceId'])

    elif command == 'get-uniqueid':
        # Get the Unique ID of the device "devicename"
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

    elif command == 'set-brightness':
        camera = getDeviceFromName(devicename,devices)
        if camera == '':
            raise Exception("Camera "+devicename+" not found")
        arlo.AdjustBrightness(basestation, camera, int(brightness))

    else:
        # Should not happen ...
        print("This should not happen")

    # Logout of Arlo session
    arlo.Logout()

except Exception as e:
    print(e)