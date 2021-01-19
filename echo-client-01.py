#!/usr/bin/env python3

import socket

SERVER_ADDRESS = '127.0.0.1'  # The server's hostname or IP address
SERVER_PORT = 65433        # The port used by the server
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((SERVER_ADDRESS, SERVER_PORT))
dati = input("Inserisci messaggio per il server: ")
dati = dati.encode()
# Send data to server
c.send(dati)
# Receive response from server
dati = c.recv(2048)
if dati:
    # Convert back to string for python3
    dati = dati.decode()
    print("Ho ricevuto dal server: ")
    print(dati + '\n')



