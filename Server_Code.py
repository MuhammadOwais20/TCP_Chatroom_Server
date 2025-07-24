import socket
import threading


class node(object):
    def __init__(self, client, nick, ip):
        self.client = client
        self.ipv4 = ip
        self.nickname = nick
        self.nextnode = None

    def __str__(self):
        return f'\nip: {self.ipv4},\nNickName = {self.nickname}'

    def setnextnode(self, value):
        self.nextnode = value

    def getnextnode(self):
        return self.nextnode

    def getclient(self):
        return self.client

    def getnick(self):
        return self.nickname

    def getip(self):
        return self.ipv4


class clients(object):
    def __init__(self):
        self.head = None

    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.getnextnode()

    def addclient(self, client, nick, ip):
        new_client = node(client, nick, ip)
        new_client.setnextnode(self.head)
        self.head = new_client

    def removeclient(self, client):
        current_node = self.head
        prev_node = None
        while current_node and current_node.getclient() != client:
            prev_node = current_node
            current_node = current_node.getnextnode()
        if not current_node:
            return
        if prev_node is None:
            self.head = current_node.getnextnode()
        else:
            prev_node.setnextnode(current_node.getnextnode())

    def search_client(self, client):
        current_client = self.head
        while current_client:
            if current_client.getclient() == client:
                return current_client

    def allclients(self): 
        current_client = self.head
        count = 0
        print("All Clients....")
        while current_client:
            print(current_client)
            count += 1
            current_client = current_client.getnextnode()
        print("Total number of clients:", count)


host = 'localhost'
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients_list = clients()


def broadcast(message, sender):
    for i in clients_list:
        if i.getclient() != sender:
            try:
                i.getclient().send(message)
            except:
                continue

def logmsg(dmsg):
    try:
        with open("chat.txt", "a", encoding="utf-8") as file:
            file.write(dmsg + "\n")
    except Exception as e:
        print(f"Failed to write to log: {e}")


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            decoded_msg = message.decode('ascii').strip()
            if decoded_msg.lower() == 'exit':
                current_client = clients_list.search_client(client)
                if current_client:
                    broadcast(f'{current_client.getnick()} left the chat'.encode('ascii'), client)
                    print(f'{current_client.getip()} Disconnected')
                    clients_list.removeclient(client)
                client.close()
                break
            broadcast(message, client)
            logmsg(decoded_msg)
        except Exception as e:
            current_client = clients_list.search_client(client)
            if current_client:
                broadcast(f'{current_client.getnick()} left the chat'.encode('ascii'), client)
                print(f'{current_client.getip()} Disconnected due to error: {e}')
                clients_list.removeclient(client)
            client.close()
            break


def Server():
    print(f"[SERVER RUNNING] Listening on {host}:{port}...\n")
    while True:
        client, address = server.accept()
        print(f'connected with {str(address)}')

        client.send("Choose Nickname".encode('ascii'))
        nick = client.recv(1024).decode('ascii')
        clients_list.addclient(client, nick, address)
        clients_list.allclients()
        
        broadcast(f'{nick} joined the server \n'.encode('ascii'), client)
        client.send("Connected With Server. \n".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


Server()
