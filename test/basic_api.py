"""
Russound RNT interface (used by models CAS44, CAA66, CAM6.6, CAV6.6)

Copyright (c) 2014 Neil Lathwood <https://github.com/laf/ http://www.lathwood.co.uk/>

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.  Please see LICENSE.txt at the top level of
the source code distribution for details.

The Russound RNET protocol is documented in cav6.6_rnet_protocol_v1.01.00.pdf, and russound-rs-232-V01_00_01.pdf
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
    """ Implements a python API for selected commands to the Russound system using the RNET protocol.
    The class is designed to maintain a connection to the Russound controller, and reads the controller state
    directly from using RNET"""

    _sem_comm = 0

    def __init__(self, host, port):
        """ Initialise Russound class """

        self._host = host
        self._port = int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Use this to keep track of when the last send command was sent
        self._last_send = time.time()
        # Used to ensure only one thread sends commands to the Russound
        self.lock = threading.Lock()

    def connect(self):
        send_msg = self.create_send_message("Ping")
        self.send_data(send_msg)
        self.get_response_message()  # Clear response buffer

    def is_connected(self):
        """ Check we are connected """

        try:  # Will throw an expcetion if sock is not connected hence the try catch.
            return self.sock.getpeername() != ''
        except:
            return False

    def set_volume(self, controller, volume):
        """ Set volume for zone to specific value.
        Divide the volume by 2 to translate to a range (0..50) as expected by Russound (Even thought the
        keypads show 0..100).
        """

        _LOGGER.debug(
            "Begin - controller= %s, zone= %s, change volume to %s", controller, volume)
        send_msg = self.create_send_message("SetVolume",
                                            controller, volume // 2)
        try:
            self.lock.acquire()
            self.send_data(send_msg)
            _LOGGER.debug("Zone %s - sent message %s", send_msg)
            self.get_response_message()  # Clear response buffer
        finally:
            self.lock.release()
            _LOGGER.debug(
                "End - controller %s, zone %s, volume set to %s.\n", controller, zone, volume)

    def toggle_mute(self, controller):
        """ Toggle mute on/off for a zone
        Note: Not tested (acambitsis) """

        send_msg = self.create_send_message("Mute",
                                            controller)
        self.send_data(send_msg)
        self.get_response_message()  # Clear response buffer

    def create_send_message(self, string_message, controller, zone=None, parameter=None):
        """ Creates a message from a string, substituting the necessary parameters,
        that is ready to send to the socket """

        # RNET requires controller value to be zero based
        cc = hex(int(controller) - 1).replace('0x', '')
        if zone is not None:
            # RNET requires zone value to be zero based
            zz = hex(int(zone) - 1).replace('0x', '')
        else:
            zz = ''
        if parameter is not None:
            pr = hex(int(parameter)).replace('0x', '')
        else:
            pr = ''

        string_message = string_message.replace(
            '@cc', cc)  # Replace controller parameter
        string_message = string_message.replace(
            '@zz', zz)  # Replace zone parameter
        string_message = string_message.replace(
            '@kk', KEYPAD_CODE)  # Replace keypad parameter
        # Replace specific parameter to message
        string_message = string_message.replace('@pr', pr)

        # Split message into an array for each "byte" and add the checksum and end of message bytes
        send_msg = string_message.split()
        send_msg = self.calc_checksum(send_msg)
        return send_msg

    def create_response_signature(self, string_message, zone):
        """ Basic helper function to keep code clean for defining a response message signature """

    def send_data(self, data, delay=COMMAND_DELAY):
        """ Send data to connected gateway """

        time_since_last_send = time.time() - self._last_send
        delay = max(0, delay - time_since_last_send)
        time.sleep(delay)  # Ensure minim recommended delay since last send

        for item in data:
            data = bytes.fromhex(str(item.zfill(2)))
            try:
                self.sock.send(data)
            except ConnectionResetError as msg:
                _LOGGER.error("Error trying to connect to Russound controller. "
                              "Check that no other device or system is using the port that "
                              "you are trying to connect to. Try resetting the bridge you are using to connect.")
                _LOGGER.error(msg)
        self._last_send = time.time()

    def get_response_message(self, resp_msg_signature=None, delay=COMMAND_DELAY):
        """ Receive data from connected gateway and if required seach and return a stream that starts at the required
        response message signature.  The reason we couple the search for the response signature here is that given the
        RNET protocol and TCP comms, we dont have an easy way of knowign that we have received the response.  We want to
        minimise the time spent reading the socket (to reduce user lag), hence we use the message response signature
        at this point to determine when to stop reading."""

        # Set intial value to none (assume no response found)
        matching_message = None
        if resp_msg_signature is None:
            # If we are not looking for a specific response do a single read to clear the buffer
            no_of_socket_reads = 1
        else:
            # Try 10x (= approx 1s at default)if we are looking for a specific response
            no_of_socket_reads = 10

        # Insert recommended delay to ensure command is processed correctly
        time.sleep(delay)
        # Needed to prevent request for waiting indefinitely
        self.sock.setblocking(0)

        data = B''
        for i in range(0, no_of_socket_reads):
            try:
                # Receive what has been sent
                data += self.sock.recv(4096)
                _LOGGER.debug('i= %s; len= %s data= %s', i, len(
                    data), '[{}]'.format(', '.join(hex(x) for x in data)))
            except BlockingIOError:  # Expected outcome if there is not data
                _LOGGER.debug('Passed=%s', i)
                pass
            except ConnectionResetError as msg:
                _LOGGER.error("Error trying to connect to Russound controller. Check that no other device or system "
                              "is using the port that you are trying to connect to. "
                              "Try resetting the bridge you are using to connect.")
                _LOGGER.error(msg)
            # Check if we have our message.  If so break out else keep looping.
            if resp_msg_signature is not None:  # If we are looking for a specific response
                matching_message, data = self.find_signature(
                    data, resp_msg_signature)
            if matching_message is not None:  # Required response found
                _LOGGER.debug("Number of reads=%s", i + 1)
                break
            time.sleep(delay)  # Wait before reading again - default of 100ms
        return matching_message

    def __exit__(self, exception_type, exception_value, traceback):
        """ Close connection to gateway """
        try:
            self.sock.close()
            _LOGGER.info("Closed connection to Russound on %s:%s",
                         self._host, self._port)
        except socket.error as msg:
            _LOGGER.error("Couldn't disconnect")
            _LOGGER.error(msg)
