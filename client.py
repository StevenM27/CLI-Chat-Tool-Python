import socket
import threading
import json

host = "127.0.0.1"
port = 12345
name = input("Enter your name: ")

in_chat_room = False

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((host, port))

c.send(name.encode())

# Thread function for receiving messages
def receive():
    while in_chat_room:
        message = c.recv(1024).decode()
        print(message)

# Thread function for sending messages
def send():
    while True:
        message = input('')
        if message.lower() == "quit":
            break
        message = "{}: {}".format(name, message)
        c.send(message.encode())

    in_chat_room = False

tr = threading.Thread(target=receive)
tr.start()
ts = threading.Thread(target=send)
ts.start()

# Main thread loop
while True:

    if not in_chat_room:
        print("You can create a new chat room or join an existing chat room.")
        print("Choose the number corresponding to the desired action:")
        print("1. List all chat rooms")
        print("2. Create a new chat room")
        print("3. Join an existing chat room")
        choice = input("Enter your option: ")

        if choice == "1":
            c.send("/option 1".encode())
            data = json.loads(c.recv(1024).decode())
            if not data:
                print("No chat rooms to show!")
                continue
            else:
                print("Chat Room #, Chat Room Name")
                for row in data:
                    print(str(row.first), str(row.second))
                
                continue

        elif choice == "2":
            c.send("/option 2".encode())
            chat_room_id = input("Enter new chat room ID: ")
            data = json.loads(c.recv(1024).decode())
            if data:
                if chat_room_id in data.keys():
                    print("Chat room number", chat_room_id, "already exists.")
                    c.send("/cancel".encode())
                    continue
            
            chat_room_name = input("Enter new chat room name: ")

            c.send("/create".encode())
            c.send(chat_room_id.encode())
            c.send(chat_room_name.encode())

            in_chat_room = True
            continue

        elif choice == "3":
            c.send("/option 3")
            chat_room_id = input("Enter chat room ID: ")
            data = json.loads(c.recv(1024).decode())
            if data:
                if chat_room_id in data.keys():
                    c.send(chat_room_id.encode())
                    response = c.recv(1024).decode()
                    print(str(response))
                    continue
            
            c.send("/cancel".encode())
            print("Chat room", chat_room_id, "does not exist.")
            continue

        else:
            print("Invalid response!")
            continue