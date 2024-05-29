Simple Chat Application
This is a simple chat application built using Python's socket and threading modules. The application supports multiple clients connecting to a server, where they can send messages to each other in real-time. The application also includes basic administration features such as kicking and banning users.

Features
Real-time messaging: Clients can send and receive messages in real-time.
Nickname selection: Each client can choose a nickname upon connecting.
Admin commands: The admin can kick or ban users from the server.
Ban persistence: Banned users are stored in a file and cannot reconnect until removed.
Requirements
Python 3.x


Usage
Starting the Server
Navigate to the directory containing the server script.

Run the server script:

bash
Code kopieren
python server.py
The server will start and begin listening for incoming connections on 127.0.0.1:55555.

Connecting a Client
Navigate to the directory containing the client script.

Run the client script:

bash
Code kopieren
python client.py
When prompted, enter a nickname. If you choose admin as your nickname, you will be prompted to enter a password. The default admin password is adminpass.

You can now send messages. If you are the admin, you can use the following commands:

/kick <nickname>: Kicks the specified user from the chat.
/ban <nickname>: Bans the specified user from the chat.
Example
Server Output:
vbnet
Code kopieren
Server is listening
Connected with ('127.0.0.1', 12345)
Nickname is user1
user1 joined!
Connected with ('127.0.0.1', 12346)
Nickname is admin
admin joined!
user1: Hello everyone!
admin: Welcome to the chat!
admin: /kick user1
user1 was kicked by an admin!
Client Output (User):
vbnet
Code kopieren
Choose your nickname: user1
Connected to server!
user1: Hello everyone!
You were kicked by an admin!
Client Output (Admin):
vbnet
Code kopieren
Choose your nickname: admin
Enter password for admin: adminpass
Connected to server!
admin: Welcome to the chat!
admin: /kick user1
user1 was kicked by an admin!
Code Overview
Server (server.py)
broadcast(message): Sends a message to all connected clients.
handle(client): Handles incoming messages from a client and processes admin commands.
receive(): Accepts new client connections and starts a thread for each client.
kick_user(name): Kicks a user from the chat.
main(): Starts the server and calls the receive function.
Client (client.py)
choose_nickname(): Prompts the user to choose a nickname.
connect_to_server(): Connects to the chat server.
receive(client, semaphore, stop_thread): Receives messages from the server.
write(client, nickname, semaphore, stop_thread): Sends messages to the server.
main(): Starts the client, sets up threads for receiving and writing messages.