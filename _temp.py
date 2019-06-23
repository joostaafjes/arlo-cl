# arlo-cl.py / Arlo Command Line 
# Send Commands to your Arlo Environment via the command line
# https://github.com/jeffreydwalter/arlo
# Michael Urspringer / v0.1

from arlo import Arlo
import sys
import argparse
import configparser

def getDeviceFromName(name,devices):
    for device in devices:
        if device['deviceName'] == name and device['deviceType'] != "siren":
            return(device)
    return("")

try:
    # Initialize config file
    config = configparser.ConfigParser()
    config.read("arlo-cl.cfg")

    # Credentials for Arlo
    USERNAME = config.get("CREDENTIALS","USERNAME")
    PASSWORD = config.get("CREDENTIALS","PASSWORD")

    # Check command line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['aktiviert', 'deaktiviert', 'garten', 'garten_hinten'])
    args = parser.parse_args()
    command=args.command
 
    # Instantiating the Arlo object automatically calls Login(), which returns an oAuth token that gets cached.
    # Subsequent successful calls to login will update the oAuth token.
    arlo = Arlo(USERNAME, PASSWORD)
    # At this point you're logged into Arlo.

    # Get all devices
    devices = arlo.GetDevices('')

    if command == 'deaktiviert':
        device = getDeviceFromName("Home",devices)
        arlo.Disarm(device)
        device = getDeviceFromName("Bridge_AZMichael",devices)
        arlo.Disarm(device)
        device = getDeviceFromName("Bridge_AZSabine",devices)
        arlo.Disarm(device)

    elif command == 'aktiviert':
        device = getDeviceFromName("Home",devices)
        arlo.Arm(device)
        device = getDeviceFromName("Bridge_AZMichael",devices)
        arlo.Arm(device)
        device = getDeviceFromName("Bridge_AZSabine",devices)
        arlo.Arm(device)

    elif command == 'garten':
        device = getDeviceFromName("Home",devices)
        arlo.CustomMode(device,"mode5")  # Garten_Alle
        device = getDeviceFromName("Bridge_AZMichael",devices)
        arlo.CustomMode(device,"mode4")  # Garten
        device = getDeviceFromName("Bridge_AZSabine",devices)
        arlo.Arm(device)

    elif command == 'garten_hinten':
        device = getDeviceFromName("Home",devices)
        arlo.CustomMode(device,"mode4")  # Garten_2
        device = getDeviceFromName("Bridge_AZMichael",devices)
        arlo.Disarm(device)
        device = getDeviceFromName("Bridge_AZSabine",devices)
        arlo.Arm(device)

except Exception as e:
    print(e)