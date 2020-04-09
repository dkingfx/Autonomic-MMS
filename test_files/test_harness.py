""" Used for adhoc testing.  in time can create formal tests. """

import logging
import test_files.basic_api
import time

IP_ADDRESS = '192.168.10.35'
PORT = 5004
logging.basicConfig(filename='russound_debugging.log', level=logging.DEBUG,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(funcName)s():%(message)s')
_LOGGER = logging.getLogger(__name__)


def test2():
    """ Used this approach to determine what responses are returned from Russound """
    x = russound.Autonomic(IP_ADDRESS, PORT)
    x.connect()
    controller = '1'
    zone = '1'
    sequence = []
    for i in range(0, 51):
        sequence.append(None)

    sequence[5] = ('get_power', x.create_send_message(
        "Play", controller, command))

    t = 0
    for item in sequence:
        if item is not None:
            print(round(t, 1), item[0], "...")
            x.send_data(item[1])
        else:
            response = x.receive_data0()
            print(round(t, 1), "Receiving message...", list(response))
            print(x.get_received_messages(response))
            # if len(response) > 0:
            #    print(response)
        time.sleep(0.1)
        t += 0.1


# Run test 4...
test2()
