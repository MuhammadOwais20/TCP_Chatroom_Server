import socket
import threading

nick = input("Choose nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5555))


def recieve():
    while True:
        try:
            msg = client.recv(1024).decode('ascii')
            if msg == "Choose Nickname":
                client.send(nick.encode('ascii'))
            else:
                print(msg)
        except:
            print("An error occurred...")
            client.close()
            break


def write():
    while True:
        msg_input = input("")
        if msg_input.strip().lower() == "exit":
            client.send("exit".encode('ascii'))
            client.close()
            break
        msg = f'{nick}: {msg_input}'
        client.send(msg.encode('ascii'))


recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
