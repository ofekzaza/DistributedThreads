import json
import socket
import _thread

class WThread:
    s: socket
    port: int
    jsonObject: str
    name: str
    code: str
    answer: str

    def __init__(self, name, port = 9999):
        self.port = port
        self.name = name
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # creating the socket
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # added in order to fix the bug the may accure
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.s.bind(('', int(self.port)))
        _thread.start_new_thread(self.execute,())

    def execute(self):
        self.listen()
        self.returnAnswer()

    def listen(self):
        while 1:
            data, address = self.s.recvfrom(1024)
            if(data != None):
                data = str(data, 'utf-8')
                try:
                    self.jsonObject = json.loads(data)
                except Exception:
                    print()
                if(self.name == self.jsonObject["Name"]):
                    self.code = self.jsonObject["Code"]

    def returnAnswer(self):
        dic = {}
        dic["Name"] = self.name
        dic["Answer"] = self.answer
        self.s.sendto(json.dumps(dic).encode('ascii'), ('<broadcast>', self.port))
