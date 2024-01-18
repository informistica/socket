#!/usr/bin/env python3
import socket, json
from threading import Thread


# lasciando il campo vuoto sarebbe la stessa cosa (localhost)
SERVER_ADDRESS = '127.0.0.1'
# Numero di porta, deve essere >1024 perchè le altre sono riservate.)
SERVER_PORT = 22224


# La funzione avvia_server crea un endpoint di ascolto (sock_listen) dal quale accettare connessioni in entrata
# la socket di ascolto viene passata alla funzione ricevi_connessioni la quale accetta richieste di connessione
# e per ognuna crea una socket per i dati (sock_service) che viene passata come parametro ad una funzione ricevi_comandi 
# eseguita da un thread per servire le richieste di uno specifico client  


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
        dati = json.loads(dati)
        n1 = dati["primoNumero"]
        operazione = dati["operazione"]
        n2 = dati["secondoNumero"]
        print("32",n1,n2,operazione)
        if operazione == "0":
            print("Fine dati dal client. Exit")
            break
        elif operazione == "+":
            risultato = float(n1) + float(n2)
        elif operazione == "-":
            risultato = float(n1) - float(n2)
        elif operazione == "*":
            risultato = float(n1) * float(n2)
        elif operazione == "/":
            if n2 == '0':
                risultato = 'Divisione per zero impossibile'
            else:
                risultato = float(n1) / float(n2)

        print(f"{n1} {operazione} {n2} = {risultato}")
        print(f"Invio il risultato a {addr_client}")
        # codifica la stringa in byte
        dati = str(risultato).encode()
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
        sock_listen.bind((indirizzo, porta))
        # Imposta quante connessioni pendenti possono essere accodate
        sock_listen.listen(5)
        print("Server in ascolto su %s. Termina con 0" % str((indirizzo, porta)))
    except socket.error as errore:
        print(f"Qualcosa è andato storto... \n{errore}")

    ricevi_connessioni(sock_listen)


if __name__ == '__main__':
    avvia_server(SERVER_ADDRESS, SERVER_PORT)
print("Termina")       