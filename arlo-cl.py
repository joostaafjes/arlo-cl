# arlo-cl.py / Arlo Command Line 
# Send Commands to your Arlo Environment via the command line
# Michael Urspringer / v0.1

import sys
import argparse
from arlo import Arlo

import configparser

try:
    # Initialize config file
    config = configparser.ConfigParser()
    config.read("arlo-cl.cfg")

    # Credentials for Arlo
    USERNAME = config.get("CREDENTIALS","USERNAME")
    PASSWORD = config.get("CREDENTIALS","PASSWORD")

    # Check command line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['list-devices', 'list-modes', 'get-deviceid', 'get-uniqueid'])
    parser.add_argument('--devicetype', '-t', choices=['basestation', 'arlobridge', 'camera', 'lights', 'siren'], help='the type of the device, if empty: all devicetypes')
    parser.add_argument('--devicename', '-n', help='the name of the device, only devices of type "basestation" or "arlobridge" are allowed')
    args = parser.parse_args()

    #print("~ Command: {}".format(args.command))
    #print("~ Device Type: {}".format(args.devicetype))

    command=args.command
    devicetype=args.devicetype
    devicename=args.devicename

    # Instantiating the Arlo object automatically calls Login(), which returns an oAuth token that gets cached.
    # Subsequent successful calls to login will update the oAuth token.
    arlo = Arlo(USERNAME, PASSWORD)
    # At this point you're logged into Arlo.

    #############################
    if command == 'list-devices':
    #############################
        # List all devices
        # Get the list of devices and filter on device type.
        # This will return an array which includes all of the devices's associated metadata.
        devices = arlo.GetDevices(devicetype)
        #print ("Device Name : Device Type : Device ID : Unique ID")
        for key in devices:
            print (key['deviceName']," : ", key['deviceType']," : ", key['deviceId']," : ", key['uniqueId'])
    #############################
    elif command == 'list-modes':
    #############################
        # List all modes for a specific device
        modes=arlo.GetAutomationDefinitions()
        #print (modes)
        for id in modes:
            #print (modes[id]['modes'])
            for mode in modes[id]['modes']:
                print(id," : ",mode['name']," : ",mode['id']," : ",mode['type'])
            print("----------------------------------")
    #############################
    elif command == 'get-deviceid':
    #############################
        # Get the Device ID of the device "devicename"
        devices = arlo.GetDevices(devicetype)
        for key in devices:
            if key['deviceName'] == devicename:
                print (key['deviceId'])
    #############################
    elif command == 'get-uniqueid':
    #############################
        # Get the Unique ID of the device "devicename"
        devices = arlo.GetDevices(devicetype)
        for key in devices:
            if key['deviceName'] == devicename:
                print (key['uniqueId'])
    else:
        # Should not happen ...
        print("This should not happen")

except Exception as e:
    print(e)