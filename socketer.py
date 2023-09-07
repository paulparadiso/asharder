import socket
import threading

class Socketer:

    def __init__(self, r_port, s_port, on_message):
        self.receive_port = r_port
        self.send_port = s_port
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket.bind(('localhost', self.receive_port))
        self.on_message = on_message

    def run(self):
        while 1:
            data = self.receive_socket.recv(1024)
            self.on_message(data)

    def start(self):
        t1 = threading.Thread(target=self.run)
        t1.start()

