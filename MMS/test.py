import asyncio

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message + b'\n')
        print('Data sent')

    def data_received(self, data):
        print('Data received:'()

loop = asyncio.get_event_loop()
message = b'stop'
coro = loop.create_connection(lambda: EchoClientProtocol(message, loop),
                              '192.168.20.35', 5004)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()