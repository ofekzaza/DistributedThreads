import json
import dThread
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # creating the soc
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # added in order to fix the bug the may accure
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('', int(9999)))

thread = dThread.DThread()

thread.execute(1, "1")

data, addr = s.recvfrom(1024)

print(str(data, 'utf-8'))

j = json.loads(data)

print(j["Name"] + j["Code"])