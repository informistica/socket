#!/usr/bin/env python3

import socket

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22224

sock_service = socket.socket()

sock_service.connect((SERVER_ADDRESS, SERVER_PORT))

print("Connesso a " + str((SERVER_ADDRESS, SERVER_PORT)))
while True:
    try:
        dati = input("Inserisci i dati da inviare: ")
    except EOFError:
        print("\nOkay. Exit")
        break

    if not dati:
        print("Non puoi inviare una stringa vuota!")
        continue

    dati = dati.encode()

    sock_service.send(dati)

    dati = sock_service.recv(2048)

    if not dati:
        print("Server non risponde. Exit")
        break

    dati = dati.decode()

    print("Ricevuto dal server:")
    print(dati + '\n')

sock_service.close()
