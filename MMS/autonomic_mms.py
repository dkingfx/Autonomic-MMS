import telnetlib∏
import time

HOST = ("192.168.20.35")
PORT = ("5004")

command = b" "

tn = telnetlib.Telnet(HOST, PORT)
tn.write(command + b"\n")
ret1 = tn.read_eager()
print(ret1)
tn.write(b"play\n")
ret2 = tn.read_until(b"Ok", timeout = 5)
print(ret2)
tn.write(command + b"\n")

print("Success!")
tn.close()