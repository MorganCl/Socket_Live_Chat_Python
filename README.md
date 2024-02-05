# Chat Program

This simple chat program consists of a server and a client implemented in Python using sockets. The server allows multiple clients to connect and exchange messages in a chatroom-like environment.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Server](#server)
- [Client](#client)
- [Contributing](#contributing)
- [License](#license)

## Features

- Multi-client chat server
- Basic client with GUI
- User preferences like changing name
- Options to save chat, clear chat, and exit

## Prerequisites

- Python 3.x

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/chat-program.git

    Navigate to the project directory:

    bash

cd chat-program

Run the server:

bash

python server.py <IP_address> <port_number>

Replace <IP_address> and <port_number> with the desired IP address and port number.

Run the client:

bash

    python client.py <IP_address> <port_number>

    Replace <IP_address> and <port_number> with the same IP address and port number used for the server.

Server

The server is responsible for managing connections from multiple clients. It listens for incoming connections and broadcasts messages to all connected clients.
Client

The client provides a simple GUI for users to interact with the chat server. It allows users to send messages, change their name, save the chat, clear the chat, and exit the application.
Contributing

Contributions are welcome! Feel free to open issues or pull requests.
License

This project is licensed under the MIT License.

typescript


Replace `<IP_address>` and `<port_number>` with the actual IP address and port number you want to use for your server. Additionally, include any additional information or customization based on your project's specific requirements.