# arlo-cl

command line tool to control Arlo cameras. Based on Python library https://github.com/jeffreydwalter/arlo

Uses the following Python modules:
* requests
* monotonic
* sseclient

## Purpose

This tool is specially adapted to my own environment where I am using some predefined modes to switch on / off different my different Arlo cams.

the script currently support these modes (which youmost likely need to adapt to your environment ...)

Mode | Purpose
--- | ---
aktiviert | Activate (Arm) all cams
deaktiviert | Deactivate (Disarm) all cams
aktiviert_tag | Set several custom modes for my different cams with different sensitivity during the day
aktiviert_ohne_terrasse | Only activate some of my cams
garten | Only activate some of my cams
garten_hinten | Only activate some of my cams

## Config

The script is looking for a config file where you define the user and password for your Arlo account and the name of your base station (currently only one base station is supported).  See "arlo-cl.cfg.sample" as a sample of how the file looks like.

I am using an additional account I created just to be used with this script so it does not interfere with my normal Arlo account I am using e.g. in the Arlo app.

The config file is named "arlo-cl.cfg" and needs to be put in the same directory as "arlo-cl.py". You can also specifiy a different name and path for that file by adding the "--configfile" switch.


## Usage:

```text
usage: arlo-cl.py [-h]
                  [--devicetype {basestation,arlobridge,camera,lights,siren}]
                  [--devicename DEVICENAME]
                  [--mode {aktiviert,deaktiviert,aktiviert_tag,aktiviert_ohne_terrasse,garten,garten_hinten}]
                  [--brightness {-2,-1,0,1,2}] [--configfile CONFIGFILE]
                  {list-devices,list-modes,get-deviceid,get-uniqueid,set-mode,set-brightness}
```

## Samples:

### List all known devices:

```text
arlo-cl.py list-devices
```
Output:

```text
<DEVICENAME>  :  <DEVICETYPE>  :  <DEVICEID>  :  <UNIQUE_DEVICEID>
```

### List only camera devices:

```text
arlo-cl.py list-devices --devicetype camera
```
Output:

```text
<DEVICENAME>  :  <DEVICETYPE>  :  <DEVICEID>  :  <UNIQUE_DEVICEID>
```

### List modes of devices

```text
arlo-cl.py list-modes
```
Output:

```text
<UNIQUE_DEVICEID>  :  <MODE_NAME>  :  <MODE_ID>  :  <MODE_TYPE> 
```

### Get Unique ID of a device named "Garten_1":

```text
arlo-cl.py get-uniqueid --devicename Garten_1
```
Output:

```text
<UNIQUE_DEVICEID>
```

### Set mode to "aktiviert" (arm all devices, see above)

```text
arlo-cl.py set_mode aktiviert
```

### Set brightness value for camera "CamName" to "+2"

```text
arlo-cl.py set-brightness --devicename CamName --brightness +2
```

