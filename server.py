# Chat program
# SERVER
import requests
import json

# Python program to implement server side of chat room. 
import socket 
import select 
import sys
import os
from _thread import start_new_thread
import time
import json

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

# checks whether sufficient arguments have been provided 
if len(sys.argv) != 3: 
    print ("Correct usage: script.py <IP address> <port number>")
    exit() 

# takes the first argument from command prompt as IP address 
IP_address = str(sys.argv[1])
# takes second argument from command prompt as port number 
Port = int(sys.argv[2])

server.bind((IP_address, Port))
server.listen(100) 

connected_clients = [] 

def clientthread(index, null): 
    # sends a message to the client whose user object is conn
    client = connected_clients[index]
    conn = client["conn"]
    name = client["name"]
    conn.send("Welcome to this chatroom!\n".encode())
    while True:
            name = client["name"]
            try:
                unclean = conn.recv(2048)
                clean = json.loads(unclean)
                text = clean["text"]
                action = clean["action"]
                if action == "message":
                    if text != '':
                        sent_message = name + " : " + text
                        # Calls broadcast function to send message to all 
                        broadcast(sent_message, conn, index, 2)
                elif action == "name":
                    for client in connected_clients:
                        if client["conn"] == conn:
                            if text != '':
                                client["name"] = text
                            break
            except: 
                continue

def broadcast(message, connection, index, broadcast_type):
    if broadcast_type == 1:
        for client in connected_clients:
            try:
                client["conn"].send(message.encode())
            except:
                client["conn"].close()
                del connected_clients[index]
    elif broadcast_type == 2:
        for client in connected_clients:
            if client["conn"] != connection: 
                try:
                    client["conn"].send(("["+time.ctime(time.time())+"] " + message + "\n").encode())
                except:
                    client["conn"].close()
                    del connected_clients[index]
        conn = connected_clients[index]["conn"]
        message = "["+time.ctime(time.time())+"] (You) " + message + "\n"
        conn.send(message.encode())

while True: 
    conn, addr = server.accept()
    connected_clients.append({"conn" : conn, "name" :  addr[0]}) 
    # prints the address of the user that just connected 
    print (addr[0] + " connected")
    broadcast(str(addr[0]) + ' has joined the chat!\n', None, None, 1)
    # creates and individual thread for every user  
    # that connects 
    start_new_thread(clientthread,((len(connected_clients)-1), addr[0]))
conn.close() 
server.close() 
