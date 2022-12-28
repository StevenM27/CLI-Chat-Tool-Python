import socket
import threading
import json

host = "127.0.0.1"
port = 12345
name = input("Enter your name: ")

lock = threading.Lock()

in_chat_room = threading.Event()
in_chat_room.clear()

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((host, port))

c.send(name.encode())

# Thread function for receiving messages
def receive(event, lock):
    while True:
        if event.is_set():
            message = c.recv(1024).decode()
            if message == "/quit":
                lock.acquire()
                print("You have left the server.")
                event.clear()
                message = ""
                lock.release()
                continue
            print(message)

# Thread function for sending messages
def send(event, lock):
    while True:
        if event.is_set():
            message = input('')
            if message.lower() == "quit":
                lock.acquire()
                event.clear()
                c.send("/quit".encode())
                message = ""
                lock.release()
                continue
            c.send(message.encode())
            message = ""
            continue

tr = threading.Thread(target=receive, args=(in_chat_room,lock,))
ts = threading.Thread(target=send, args=(in_chat_room,lock,))
tr.start()
ts.start()

# Main thread loop
while True:

    if not in_chat_room.is_set():

        lock.acquire()

        print("You can create a new chat room or join an existing chat room.")
        print("Choose the number corresponding to the desired action:")
        print("1. List all chat rooms")
        print("2. Create a new chat room")
        print("3. Join an existing chat room")
        choice = input("Enter your option: ")
        print()

        if choice == "1":
            c.send("/option 1".encode())
            data = json.loads(c.recv(1024).decode())
            if not data:
                print("No chat rooms to show!")
                print()
                data = ""
                lock.release()
                continue
            else:
                print("Chat Room #, Chat Room Name")
                for id in data:
                    print(str(id) + ",",  str(data[id]))
                print()
                data = ""
                lock.release()
                continue

        elif choice == "2":
            c.send("/option 2".encode())
            chat_room_id = input("Enter new chat room ID: ")
            print()
            data = json.loads(c.recv(1024).decode())
            if data:
                if chat_room_id in data.keys():
                    print("Chat room number", chat_room_id, "already exists.")
                    print()
                    c.send("/cancel".encode())
                    data = ""
                    lock.release()
                    continue
            
            data = ""
            chat_room_name = input("Enter new chat room name: ")
            print()

            c.send("/create".encode())
            c.send(chat_room_id.encode())
            c.send(chat_room_name.encode())

            server_response = c.recv(1024).decode()
            print(server_response)
            print()

            in_chat_room.set()
            lock.release()
            continue

        elif choice == "3":
            c.send("/option 3".encode())
            chat_room_id = input("Enter chat room ID: ")
            data = json.loads(c.recv(1024).decode())
            if data:
                if chat_room_id in data.keys():
                    c.send(chat_room_id.encode())
                    response = c.recv(1024).decode()
                    print(str(response))
                    print()
                    in_chat_room.set()
                    data = ""
                    lock.release()
                    continue
            
            c.send("/cancel".encode())
            print("Chat room", chat_room_id, "does not exist.")
            print()
            lock.release()
            continue

        else:
            print("Invalid response!")
            lock.release()
            continue