"""
Autonomic Mirage Media Server interface (used by eSeries AMPS and Media Streamers)

Base on code from Russound RNT.
Copyright (c) 2014 Neil Lathwood <https://github.com/laf/ http://www.lathwood.co.uk/>

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.  Please see LICENSE.txt at the top level of
the source code distribution for details.

The Autonomic Mirage Media Server IP protocol is documented in mcs_3.0_IP_Control_Protocol.pdf
which are stored in the source code repo.
"""
import telnetlib
import logging
import time

_LOGGER = logging.getLogger(__name__)
# Recommendation is that this should be at leat 100ms delay to ensure subsequent commands
# are processed correctly (pg 35 on russound-rs-232-V01_00_01.pdf).
COMMAND_DELAY = 0.1
# For an external system this is the required value (pg 28 of cav6.6_rnet_protocol_v1.01.00.pdf)
KEYPAD_CODE = '70'


class Autonomic:
    """ Implements a python API for selected commands to the Autonomic Mirage system using TCP protocol.
    """

    def __init__(self, host, port):
        """Initialize the Autonomic device."""
        self._host = host
        self._port = port

    def telnet_request(cls, telnet, command, all_lines=False):
        """Execute `command` and return the response."""
        _LOGGER.debug("Sending: %s", command)
        telnet.write(command.encode("ASCII") + b"\r")
        lines = []
        while True:
            line = telnet.read_until(b"\r", timeout=0.2)
            if not line:
                break
            lines.append(line.decode("ASCII").strip())
            _LOGGER.debug("Received: %s", line)

        if all_lines:
            return lines
        return lines[0] if lines else ""

    def telnet_command(self, command):
        """Establish a telnet connection and sends `command`."""
        telnet = telnetlib.Telnet(self._host, self._port)
        _LOGGER.debug("Sending: %s", command)
        telnet.write(command.encode("ASCII") + b"\r")
        telnet.read_very_eager()  # skip response
        telnet.close()
