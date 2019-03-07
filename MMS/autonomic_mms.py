import telnetlib
import asyncio
import time
import asyncio
import json
import logging
from asyncio import Condition, Lock
from enum import Enum
from typing import Any, Dict, List, Union


HOST = ("192.168.20.35")
PORT = ("5004")

command = b" "

tn = telnetlib.Telnet(HOST, PORT)
tn.write(command + b"\n")
ret1 = tn.read_eager()
print(ret1)
tn.write(b"play\n")
ret2 = tn.read_until(b"Ok", timeout=5)
print(ret2)
tn.write(command + b"\n")

print("Success!")
tn.close()

<<<<<<< HEAD
class ConnectPort23:
    """Control Autonomic-MMS via port 23"""
=======
class ControlOverPort23:
    """Connect to MMS via port 23"""
>>>>>>> c70bdd0e0678c6bc42b07c8e70343ce204ba5eae
    class systemCommands(Enum):
        """Valid port 23 commands"""
        UPTIME = 'Uptime'
        BROWSECLIENT = 'BrowseClients'
        BROWSESOURCE = 'BrowseSources'
        UPDATE = 'AutoUpdate'
        REBOOT = 'Reboot'
        SHUTDOWN = 'Shutdown'

<<<<<<< HEAD
class ConnectPort5004:
    """Control Autonomic-MMS via port 5004"""
=======
class ControlOverPort5004:
    """Connect to MMS via port 5004"""
>>>>>>> c70bdd0e0678c6bc42b07c8e70343ce204ba5eae
    class controlCommands(Enum):
        """Valid port 5004 commands"""
        NOWPLAYING = 'BrowseNowPlaying'
        STREAMING = 'BrowseServiceAccounts'
        VOLUMEDOWN = 'VolumeDown'
        VOLUMEUP = 'VolumeUp'
        WAIT = 'Wait'
        SKIPNEXT = 'SkipNext'
        SKIPPREVIOUS = 'SkipPrevious'
        SETVOLUME = 'SetVolume'
        SEEK = 'Seek'
        REPEAT = 'Repeat'
        PLAYRADIO = 'PlayRadioStation'
        PLAYPAUSE = 'PlayPause'
        PLAYARTIST = 'PlayArtist'
        PLAYALL = 'PlayAllMusic'
        MUTE = 'Mute'
        JUKEBOX = 'JukeBoxMode'
        REWIND = 'Rewind'
        FASTFORWARD = 'FastForward'
        GETART = 'GetArt'
<<<<<<< HEAD
=======

class controlOverPort5006:
    """Connect to MMS via port 5006"""
    class MradControlCommands(Enum):
        """Valid port 5006 commands"""
        MRADALLOFF = 'AllOff'
        MRADBROWSEALLSOURCE = 'BrowseAllSources'
        MRADBROWSEALLZONES = 'BrowseAllZones'
        MRADBROUSESOURCE = 'BrowseSources'
        MRADBROWSEZONEGRP = 'BrowseZoneGroup'
        MRADBROWSEZONEGRPS = 'BrowseZoneGroups'
        MRADBRWOSEZONES = 'BrowseZones'
        MRADSTATUS = 'GetStatus'
        MRADMUTEALL = 'MuteAll'
        MRADPOWER = 'Power'
      
>>>>>>> c70bdd0e0678c6bc42b07c8e70343ce204ba5eae
