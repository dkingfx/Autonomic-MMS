""" Used for adhoc testing.  in time can create formal tests. """

import logging
import basic_api
import time

IP_ADDRESS = '192.168.10.35'
PORT = 5004
logging.basicConfig(filename='autonomic_mms_debugging.log', level=logging.DEBUG,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(funcName)s():%(message)s')
_LOGGER = logging.getLogger(__name__)


def test1():
    x = basic_api.Autonomic(IP_ADDRESS, PORT)
    x.send_command("command")


# Run test 1...
test1()
