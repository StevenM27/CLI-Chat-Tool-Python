import socket
import threading

host = "127.0.0.1"
port = 12345
name = input("Enter your name: ")

in_chat_room = False

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((host, port))

# Thread function for receiving messages
def receive():
    pass

# Thread function for sending messages
def send():
    pass

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

        if choice == 1:
            c.send("/option 1".encode())
            data = c.recv(1024)
            if not data:
                print("No chat rooms to show!")
                continue
            else:
                print("Chat Room #, Chat Room Name")
                for row in data:
                    print(str(row.first), str(row.second))
                
                continue

        elif choice == 2:
            c.send("/option 2".encode())
            chat_room_number = input("Enter new chat room number: ")
            data = c.recv(1024)
            if data:

        elif choice == 3:
            pass
        else:
            print("Invalid response!")
            continue