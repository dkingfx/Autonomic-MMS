import asyncio

HOST = ("192.168.20.35")
PORT = ("5004")

async def tcp_echo_client(loop):
    reader, writer = await asyncio.open_connection(HOST, 5004,
                                                   loop=loop)
writer = (b'play')

loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(loop))
loop.close()