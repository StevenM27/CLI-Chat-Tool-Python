import socket
import threading
import json

host = "127.0.0.1"
port = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen()

lock = threading.Lock()

client_names = {}
chat_room_clients = {}
chat_room_names = {}


def send_message(c, id, message):
    for client in chat_room_clients[id]:
        message = str(client_names[c]) + ": " + str(message)
        client.send(str(message).encode())


def client_handler(c):
    lock.release()
    while True:
        client_response = ""
        client_response = str(c.recv(1024).decode())

        if client_response == "/option 1":
            # Send all chat room data
            c.send(json.dumps(chat_room_names, indent=4).encode())
            continue
        elif client_response == "/option 2":
            # Create a new chat room
            c.send(json.dumps(chat_room_names, indent=4).encode())
            client_response = str(c.recv(1024).decode())

            if client_response == "/cancel":
                continue
            elif client_response == "/create":
                chat_room_id = str(c.recv(1024).decode())
                chat_room_name = str(c.recv(1024).decode())

                chat_room_names[chat_room_id] = chat_room_name
                chat_room_clients[chat_room_id] = [c]
                continue
        elif client_response == "/option 3":
            # join an existing chat room
            c.send(json.dumps(chat_room_names, indent=4).encode())
            client_response = str(c.recv(1024).decode())

            if client_response == "/cancel":
                continue
            else:
                chat_room_clients[client_response].append(c)
                response = "Connected to chatroom " + str(client_response)
                c.send(response.encode())
                continue

        else:
            for id in chat_room_clients:
                if c in chat_room_clients[id]:
                    send_message(c, id, client_response)
                    break
            continue


while True:
    c, addr = s.accept()

    lock.acquire()

    print("Connected to :", addr[0], ':', addr[1])
    c_name = str(c.recv(1024).decode())

    print("Client name is", str(c_name))
    client_names[c] = c_name

    thread = threading.Thread(target=client_handler, args=(c,))
    thread.start()
