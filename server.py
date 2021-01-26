#!/usr/bin/env python3
import socket

# lasciando il campo vuoto sarebbe la stessa cosa (localhost)
SERVER_ADDRESS = '127.0.0.1'

# Numero di porta, deve essere >1024 perchè le altre sono riservate.)
SERVER_PORT = 22224

# Crea la socket
sock_listen = socket.socket()

# Opzionale: permette di riavviare subito il codice,
# altrimenti bisognerebbe aspettare 2-4 minuti prima di poter riutilizzare(bindare) la stessa porta
sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Associa indirizzo e porta.  Nota che  l'argumento è una tupla:
sock_listen.bind((SERVER_ADDRESS, SERVER_PORT))

# Imposta quante connessioni pendenti possono essere accodate
sock_listen.listen(5)

print("Server in ascolto su %s. Termina con ko" % str((SERVER_ADDRESS, SERVER_PORT)))

# Abbiamo creato un endpoint di ascolto (sock_listen) dal quale accettare connessioni in entrata
# Il loop accetterà una connessione alla volta e la servirà in una nuova connessione (sock_service) finchè il client non si disconnette
# dopodichè il server ne accetterà di nuove tra quelle in coda

op = " " #operazione
n1 = 0   #primo termine
n2 = 0   #secondo termine
while True:
    sock_service, addr_client = sock_listen.accept()
    print("\nConnessione ricevuta da %s" % str(addr_client))
    print("\nAspetto di ricevere i dati dell'operazione ")

    while True:
        dati = sock_service.recv(2048)
        if not dati:
            print("Fine dati dal client. Reset")
            break

        # Decodifica i byte ricevuti in una stringa unicode
        dati = dati.decode()
        print("Ricevuto: '%s'" % dati)
        if dati == "ko":
            print("Fine dati dal client. Exit")
            break
        op, n1, n2 = dati.split(";")
        if op == "piu":
            dati = str(float(n1) + float(n2))
        elif op == "meno":
            dati = str(float(n1) - float(n2))
        elif op == "per":
            dati = str(float(n1) * float(n2))
        elif op == "diviso":
            if n2=='0':
                dati='Divisione per zero impossibile'
            else:
                dati = str(float(n1) / float(n2))

        dati = "Il risultato dell'operazione: '" + op + "' tra '" + str(n1) + "' e '" + str(n2) + "' è: '" + dati + "'"

        # codifica la stringa in byte
        dati = dati.encode()

        # Invia la risposta al client.
        sock_service.send(dati)

    sock_service.close()