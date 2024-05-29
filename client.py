import socket
import threading

def choose_nickname():
    nickname = input("Choose your nickname: ")
    password = None
    if nickname == 'admin':
        password = input("Enter password for admin: ")
    return nickname, password

def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 55555))
    return client

def receive(client, semaphore, stop_thread):
    while True:
        if stop_thread[0]:
            break
        try:
            semaphore.acquire()
            message = client.recv(1024).decode('ascii')
            semaphore.release()
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection was refused! Wrong password!")
                        stop_thread[0] = True
                elif next_message == 'BAN':
                    print('Connection refused because of ban!')
                    client.close()
                    stop_thread[0] = True
            else:
                print(message)
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            break

def write(client, nickname, semaphore, stop_thread):
    while True:
        if stop_thread[0]:
            break
        message = f'{nickname}: {input("")}'
        if message[len(nickname) + 2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname) + 2:].startswith('/kick'):
                    semaphore.acquire()
                    client.send(f'KICK {message[len(nickname) + 8:]}'.encode('ascii'))
                    semaphore.release()
                elif message[len(nickname) + 2:].startswith('/ban'):
                    semaphore.acquire()
                    client.send(f'BAN {message[len(nickname) + 7:]}'.encode('ascii'))
                    semaphore.release()
                else:
                    print("Commands can only be executed by the admin!")
            else:
                print("Commands can only be executed by the admin!")
        else:
            semaphore.acquire()
            client.send(message.encode('ascii'))
            semaphore.release()

def main():
    global nickname, password
    nickname, password = choose_nickname()
    client = connect_to_server()
    stop_thread = [False]  # Using a list to allow modification within threads
    semaphore = threading.Semaphore(2)

    receive_thread = threading.Thread(target=receive, args=(client, semaphore, stop_thread))
    write_thread = threading.Thread(target=write, args=(client, nickname, semaphore, stop_thread))
    receive_thread.start()
    write_thread.start()

if __name__ == "__main__":
    main()
