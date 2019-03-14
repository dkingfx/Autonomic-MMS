import asyncio

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '192.168.10.35', 5004)

    print(f'Send Command: {message!r}')
    writer.write(message + b"\n")

    data = await reader.read(100)
    print(data)

    print("Command Received!  Closing")
    writer.close()

asyncio.run(tcp_echo_client(b'stop'))
