"""Autonomic MMS Controls

Interaction mostly through the telnet and control classes.
"""
import telnetlib
import asyncio
import time
import asyncio
import json
import logging
from asyncio import Condition, Lock
from enum import Enum
from typing import Any, Dict, List, Union


HOST = ("192.168.10.35")
PORT = ("5004")

command = b"Play"

tn = telnetlib.Telnet(HOST, PORT)
tn.write(command + b"\n")
ret1 = tn.read_eager()
print(ret1)
tn.write(b"\n")
ret2 = tn.read_until(b"Ok", timeout=5)
print(ret2)
tn.write(command + b"\n")

print("Success!")
tn.close()
'''
Note: Basic test to stablish a connection and send command. The above code connects to the Mirage Media Server 
and sends the Play command. The server receives the command and the current song or radio streams starts playing. 
'''

class ControlOverPort23:
    """Connect to MMS via port 23"""
    class systemCommands(Enum):
        """Valid port 23 commands"""
        UPTIME = 'Uptime'
        REBOOT = 'Reboot'
        SHUTDOWN = 'Shutdown'

class ControlOverPort5004:
    """Connect to MMS via port 5004"""
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

class controlOverPort5006:
    """Connect to MMS via port 5006"""
    class MRADControlCommands(Enum):
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
      
