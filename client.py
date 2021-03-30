#!/usr/bin/env python3

import socket
import random

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22224

sock_service = socket.socket()

sock_service.connect((SERVER_ADDRESS, SERVER_PORT))

print("Connesso a " + str((SERVER_ADDRESS, SERVER_PORT)))
protocollo = ["Send SYN", "Receives SYN ACK","Sends ACK with Data"]
step=0
syn = random.randint(1,1000)
dati = str(step)+";"+str(syn)
while True:
    dati = dati.encode()
    sock_service.send(dati)
    print(protocollo[int(step)])
    dati = sock_service.recv(2048)
    print(dati)
    if not dati:
        print("Server non risponde. Exit")
        break
    dati = dati.decode()
    step,msg = dati.split(";")
    if step == '3':
        print("Termino protocollo")
        break
    else:
        print(str(step)+ protocollo[int(step)])
       
    print(dati + '\n')

sock_service.close()
