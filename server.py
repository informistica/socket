#!/usr/bin/env python3
#https://realpython.com/python-sockets/
import socket

HOST = '127.0.0.1'  # Indirizzo dell'interfaccia standard di loopback (localhost)
PORT = 65432        # Porta di ascolto, la lista di quelle utilizzabili parte da >1023)

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Optionale: permette di riavviare subito il codice,
# altrimenti bisognerebbe aspettare 2-4 minuti prima di poter riutilizzare(bindare) la stessa porta
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((HOST, PORT))
s.listen()
print("[*] In ascolto su %s:%d" % (HOST, PORT))
clientsocket, address = s.accept()
with clientsocket as cs:
    print('Connessione da', address)
    while True:
        dati = cs.recv(1024)
        dati.decode()
        if not dati:
            break
        dati = dati.decode()
        print("Ricevuto '%s' dal client" % dati)
        dati = "Ciao, " + str(address) + ". Ho ricevuto questo: '" + dati + "'"
        dati = dati.encode()
        # Invia i dati modificati al client
        cs.send(dati)
        print('Inviato al client:', dati)
