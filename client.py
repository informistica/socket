#!/usr/bin/env python3

import socket,json
import sys

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22224


# La funzione riceve la socket connessa al server e la utilizza per richiedere il servizio
def invia_comandi(sock_service):
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


# La funzione crea una socket (s) per la connessione con il server e la passa alla funzione invia_comandi(s)
def connessione_server(address, port):
    try:
        s = socket.socket()  # creazione socket client
        s.connect((address, port))  # connessione al server
        print(f"Connessessione al Server: {address}:{port}")
    except s.error as errore:
        print(f"Qualcosa è andato storto, sto uscendo... \n{errore}")
        sys.exit()
    invia_comandi(s)


if __name__ == '__main__':
    connessione_server(SERVER_ADDRESS, SERVER_PORT)

# if __name__ == '__main__': consente al nostro codice di capire se stia venendo eseguito come script a se stante,
# o se è invece stato richiamato come modulo da un qualche programma per usare una o più delle sua varie
# funzioni e classi.
