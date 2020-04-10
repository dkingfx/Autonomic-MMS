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

import logging
import time
import socket
import threading

_LOGGER = logging.getLogger(__name__)
# Recommendation is that this should be at leat 100ms delay to ensure subsequent commands
# are processed correctly (pg 35 on russound-rs-232-V01_00_01.pdf).
COMMAND_DELAY = 0.1
# For an external system this is the required value (pg 28 of cav6.6_rnet_protocol_v1.01.00.pdf)
KEYPAD_CODE = '70'


class Autonomic:
    """ Implements a python API for selected commands to the Autonomic Mirage system using TCP protocol.
    """

    _sem_comm = 0

    def __init__(self, host, port):
        """ Initialise Autonomic class """

        self._host = host
        self._port = int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Used to ensure only one thread sends commands to the Russound
        self.lock = threading.Lock()

    def send_command(self, message):
        """ Send data to connected gateway """

        try:

            # Send data
            message = b'Play'
            print('sending {!r}'.format(message))
            self.sock.sendall(message + b"\n")

            # Look for the response
            amount_received = 0
            amount_expected = len(message)

            while amount_received < amount_expected:
                data = self.sock.recv(1024)
                amount_received += len(data)
                print('received {!r}'.format(data))

        finally:
            print('closing socket')
            self.sock.close()
