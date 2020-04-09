""" Used for adhoc testing.  in time can create formal tests. """

import logging
import test.basic_api
import time

IP_ADDRESS = '192.168.10.35'
PORT = 5004
logging.basicConfig(filename='autonomic_mms_debugging.log', level=logging.DEBUG,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(funcName)s():%(message)s')
_LOGGER = logging.getLogger(__name__)


def test1():
    x = mms.Autonomic(IP_ADDRESS, PORT)
    x.connect()


# Run test 4...
test1()
