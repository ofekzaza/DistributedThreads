import json
import socket
import _thread

class DThread():
    answer = None
    s: socket
    port: int

    def __init__(self, port = 9999):
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # creating the socket
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # added in order to fix the bug the may accure
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.s.bind(('', int(self.port)))
        #_thread.start_new_thread(self.constructSockets, ())

    def constructSockets(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # creating the socket
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # added in order to fix the bug the may accure
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.s.bind(('', int(self.port)))

    def run(self, target : int,  code: str): # code is in c!
        dic ={}
        dic['Name'] = str(target)
        dic['Code'] = code
        self.s.sendto(json.dumps(dic).encode('ascii'), ('<broadcast>', self.port))
        self.listen()

    def execute(self, target, code: str): # code is in c!
        _thread.start_new_thread(self.run, (target, code))

    def listen(self):
        while 1:
            data, address = self.s.recvfrom(1024)
            if(data is not None):
                data = str(data, 'utf-8')
                try:
                    jsonObject = json.loads(data)
                except Exception:
                    print()
                if("master" == jsonObject["name"]):
                    self.answer = jsonObject["answer"]
                    return

    def haveAnswer(self):
        if(self.answer == None):
            return False
        return True

    def getAnswer(self):
        return self.answer