#!/usr/bin/env python3

import socket,json

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22224

sock_service = socket.socket()

sock_service.connect((SERVER_ADDRESS, SERVER_PORT))

print("Connesso a " + str((SERVER_ADDRESS, SERVER_PORT)))
#1 Spiega a cosa serve il try-except EOFError
while True:
    primoNumero = float(input("Inserisci il primo numero: "))
    operazione = input("Inserisci l'operazione (simbolo +,-,*,/, 0 per terminare)")
    secondoNumero = float(input("Inserisci il secondo numero: "))
    dati = {"primoNumero":primoNumero,
            "operazione":operazione,
            "secondoNumero":secondoNumero}
    dati = json.dumps(dati)

    if operazione == '0':
        print("Fine connessione!")
        break

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