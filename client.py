#!/usr/bin/env python3
import socket
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22224
sock_service = socket.socket()
sock_service.connect((SERVER_ADDRESS, SERVER_PORT))

print("Client connesso a " + str((SERVER_ADDRESS, SERVER_PORT)))
#              send   receive      send            receive
protocollo = ["SYN", "SYN ACK","ACK with Data","ACK for Data"]
step=0
dati = str(0)
while True:
    dati = dati.encode()
    sock_service.send(dati)
    print("Invio: "+ str(dati)+ " - " + protocollo[int(dati)])
    dati = sock_service.recv(2048)
    if not dati:
        print("Server non risponde. Exit")
        break
    dati = dati.decode()
    if dati == '3':
        print("Ricevuto: "+ dati+ " - " + protocollo[int(dati)])
        print("Termino connessione")
        break
    else:
        print("Ricevuto: "+ dati+ " - " + protocollo[int(dati)])
        dati = int(dati)+1
        dati = str(dati)
        
sock_service.close()
