import socket

from _thread import *
import threading

host = "127.0.0.1"
port = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

lock = threading.Lock()

chat_rooms = {}
chat_rooms[101] = []

#thread function
def threaded(c):
    while True:

        data = c.recv(1024)
        if not data:
            print("Bye")

            lock.release()
            break
    
        data = data[::-1]
        c.send(data)
    
    c.close()


def Main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket bound to port", port)

    s.listen(5)
    print("socket is listening")

    while True:
        c, addr = s.accept()

        lock.acquire()
        print("Connected to :", addr[0], ':', addr[1])

        start_new_thread(threaded, (c,))
    
    s.close()


if __name__ == "__main__":
    Main()


