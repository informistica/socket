#!/usr/bin/env python3
import socket
from threading import Thread


# lasciando il campo vuoto sarebbe la stessa cosa (localhost)
SERVER_ADDRESS = '127.0.0.1'
# Numero di porta, deve essere >1024 perchè le altre sono riservate.)
SERVER_PORT = 22224


# La funzione avvia_server crea un endpoint di ascolto (sock_listen) dal quale accettare connessioni in entrata
# la socket di ascolto viene passata alla funzione ricevi_comandi la quale accetta richieste di connessione
# e per ognuna crea una socket per i dati (sock_service) da cui ricevere le richieste e inviare le risposte


def ricevi_comandi(sock_service, addr_client):
    print("Avviato il thread per servire le richieste da %s" % str(addr_client))
    print("Aspetto di ricevere i dati dell'operazione ")
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
        operazione = dati
        op, n1, n2 = dati.split(";")
        if op == "piu":
            dati = str(float(n1) + float(n2))
        elif op == "meno":
            dati = str(float(n1) - float(n2))
        elif op == "per":
            dati = str(float(n1) * float(n2))
        elif op == "diviso":
            if n2 == '0':
                dati = 'Divisione per zero impossibile'
            else:
                dati = str(float(n1) / float(n2))

        dati = "Il risultato dell'operazione: '" + op + "' tra '" + str(n1) + "' e '" + str(n2) + "' è: '" + dati + "'"
        print("Invio il risultato dell'operazione %s a %s\n" % (operazione, addr_client))
        # codifica la stringa in byte
        dati = dati.encode()
        # Invia la risposta al client.
        sock_service.send(dati)

    sock_service.close()


def ricevi_connessioni(sock_listen):
    while True:
        sock_service, addr_client = sock_listen.accept()
        print("\nConnessione ricevuta da %s" % str(addr_client))
        print("Creo un thread per servire le richieste")
        try:
            Thread(target=ricevi_comandi, args=(sock_service, addr_client)).start()
        except:
            print("Il thread non si avvia")
            sock_listen.close()



def avvia_server(indirizzo, porta):
    try:
        # Crea la socket
        sock_listen = socket.socket()
        # Opzionale: permette di riavviare subito il codice,
        # altrimenti bisognerebbe aspettare 2-4 minuti prima di poter riutilizzare(bindare) la stessa porta
        sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Associa indirizzo e porta.  Nota che  l'argumento è una tupla:
        sock_listen.bind((SERVER_ADDRESS, SERVER_PORT))
        # Imposta quante connessioni pendenti possono essere accodate
        sock_listen.listen(5)
        print("Server in ascolto su %s. Termina con ko" % str((indirizzo, porta)))
    except socket.error as errore:
        print(f"Qualcosa è andato storto... \n{errore}")

    ricevi_connessioni(sock_listen)


if __name__ == '__main__':
    avvia_server(SERVER_ADDRESS, SERVER_PORT)
print("ciao")