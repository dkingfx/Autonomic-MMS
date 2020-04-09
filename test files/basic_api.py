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

    _sem_comm = 0

    def __init__(self, host=("192.168.10.35"), port=(5004)):
        """ Initialise Autonomic class """

        self._host = host
        self._port = int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Use this to keep track of when the last send command was sent
        self._last_send = time.time()
        # Used to ensure only one thread sends commands to the Russound
        self.lock = threading.Lock()

    def connect(self):

        try:
            self.sock.connect((self._host, self._port))
            _LOGGER.info(
                "Successfully connected to Russound on %s:%s", self._host, self._port)
            return True
        except socket.error as msg:
            _LOGGER.error("Error trying to connect to Russound controller.")
            _LOGGER.error(msg)
            return False

    def is_connected(self):
        """ Check we are connected """

        try:  # Will throw an expcetion if sock is not connected hence the try catch.
            return self.sock.getpeername() != ''
        except:
            return False


    def __exit__(self, exception_type, exception_value, traceback):
        """ Close connection to gateway """
        try:
            self.sock.close()
            _LOGGER.info("Closed connection to Russound on %s:%s",
                         self._host, self._port)
        except socket.error as msg:
            _LOGGER.error("Couldn't disconnect")
            _LOGGER.error(msg)
