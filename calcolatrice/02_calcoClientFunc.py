#!/usr/bin/env python3

import socket

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22225

def invia_comandi(sock_service):
    while True:
        try:
            n1 = input("Inserisci il primo numero: ")
            n2 = input("Inserisci il secondo numero: ")
            oper = input("Inserisci l'operazione da effettuare(piu / meno / per / diviso): ")
            dati=f"{oper};{n1};{n2}"

        except EOFError:
            print("\nOkay. Exit")
            break
        if not dati:
            print("Non puoi inviare una stringa vuota!")
            continue
        if dati == '0':
            print("Chiudo la connessione con il server!")
            sock_service.close()
            break
        
        dati = dati.encode()
        sock_service.sendall(dati)
        dati = sock_service.recv(2048)
        if not dati:
            print("Server non risponde. Exit")
            break
        dati = dati.decode()
        print("Ricevuto dal server:")
        print(dati + '\n')
        

def connessione_server(address,port):
    sock_service = socket.socket()
    sock_service.connect((SERVER_ADDRESS, SERVER_PORT))
    print("Connesso a " + str((SERVER_ADDRESS, SERVER_PORT)))
    invia_comandi(sock_service)

if __name__=='__main__':
    connessione_server(SERVER_ADDRESS,SERVER_PORT)