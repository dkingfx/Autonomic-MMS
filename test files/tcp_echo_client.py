import asyncio


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '192.168.10.35', 5006)

    print(f'Send: {message!r}')
    writer.write(message + b"\n")

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    print("Connection Closed")
    writer.close()

asyncio.run(tcp_echo_client(b'Ping'))
