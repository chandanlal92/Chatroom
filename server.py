import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists for Clients and Their Nicknames
clients = []
nicknames = []

# Semaphore for synchronizing access to clients and nicknames lists
client_semaphore = threading.Semaphore(2)

def broadcast(message):
    """Send message to all connected clients."""
    client_semaphore.acquire()
    for client in clients:
        client.send(message)
    client_semaphore.release()

def handle(client):
    """Handle incoming messages from a client."""
    while True:
        try:
            message = client.recv(1024)
            msg = message.decode('ascii')
          
            if msg.startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_kick = msg[5:].strip()
                    kick_user(name_to_kick)
                else:
                    client.send('Connection was refused'.encode('ascii'))
            elif msg.startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = msg[4:].strip()
                    kick_user(name_to_ban)
                    with open('bans.txt', 'a') as f:
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned!')
                else:
                    client.send('Connection was refused'.encode('ascii'))
            else:
                broadcast(message)
        except:
            # Removing and closing clients
            if client in clients:
                client_semaphore.acquire()
                index = clients.index(client)
                clients.remove(client)
                client_semaphore.release()
                client.close()
                nickname = nicknames[index]
                broadcast(f'{nickname} left!'.encode('ascii'))
                nicknames.remove(nickname)
                break

def receive():
    """Accept new connections from clients."""
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Request and store nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        
        with open('bans.txt', 'r') as f:
            bans = f.readlines()

        if nickname + '\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue

        if nickname == 'admin':
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            if password != 'adminpass':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        client_semaphore.acquire()
        nicknames.append(nickname)
        clients.append(client)
        client_semaphore.release()

        # Print and broadcast nickname
        print(f"Nickname is {nickname}")
        broadcast(f"{nickname} joined!".encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start handling thread for client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick_user(name):
    """Kick a user from the chat."""
    if name in nicknames:
        client_semaphore.acquire()
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You were kicked by an admin!'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        client_semaphore.release()
        broadcast(f'{name} was kicked by an admin!'.encode('ascii'))

def main():
    print("Server is listening")
    receive()

if __name__ == "__main__":
    main()
