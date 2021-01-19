#!/usr/bin/env python3

import socket

SERVER_ADDRESS = '127.0.0.1'  # The server's hostname or IP address
SERVER_PORT = 65433        # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_ADDRESS, SERVER_PORT))
dati = input("Inserisci messaggio per il server: ")
dati = dati.encode()
# Send data to server
s.send(dati)
# Receive response from server
dati = s.recv(2048)
if dati:
    # Convert back to string for python3
    dati = dati.decode()
    print("Ho ricevuto dal server: ")
    print(dati + '\n')



