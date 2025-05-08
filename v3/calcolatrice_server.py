# Server TCP multithread che accetta connessioni da più client e calcola risultati di operazioni aritmetiche

import socket           # Per la comunicazione di rete
import json             # Per la gestione dei dati in formato JSON
from threading import Thread  # Per gestire le connessioni in parallelo (multithreading)

# Funzione eseguita in un thread per ogni client connesso
def ricevi_comandi(sock_service, addr_client):
    print("Client: ", addr_client)  # Stampa l'indirizzo del client connesso
    with sock_service as sock_client:  # Gestisce automaticamente la chiusura della connessione
        while True:
            # Riceve dati dal client
            data = sock_client.recv(DIM_BUFFER)

            # Se il client ha chiuso la connessione, esce dal ciclo
            if not data:
                break

            # Decodifica i byte ricevuti e li converte da JSON a dizionario
            data = data.decode()
            data = json.loads(data)

            # Estrae i dati ricevuti
            primoNumero = data["primoNumero"]
            operazione = data["operazione"]
            secondoNumero = data["secondoNumero"]

            # Esegue l'operazione richiesta
            risultato = 0
            if operazione == "+":
                risultato = primoNumero + secondoNumero
            elif operazione == "-":
                risultato = primoNumero - secondoNumero
            elif operazione == "*":
                risultato = primoNumero * secondoNumero
            elif operazione == "/":
                if secondoNumero != 0:
                    risultato = primoNumero / secondoNumero
                else:
                    risultato = "Impossibile"
            elif operazione == "%":
                risultato = primoNumero % secondoNumero

            print(risultato)  # Stampa il risultato lato server

            # Invia il risultato al client (convertito in stringa e codificato)
            sock_client.sendall(str(risultato).encode())

# Funzione che accetta una nuova connessione e lancia un thread per gestirla
def ricevi_connessioni(sock_listen):
    sock_service, address_client = sock_listen.accept()  # Accetta la connessione da un client
    try:
        # Avvia un nuovo thread per gestire i comandi del client
        Thread(target=ricevi_comandi, args=(sock_service, address_client)).start()
    except Exception as e:
        print(e)  # Stampa eventuali errori nella creazione del thread

# Funzione principale che avvia il server e resta in ascolto di nuove connessioni
def avvia_server(indirizzo, porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_server:
        # Imposta l'opzione per riutilizzare subito la porta dopo un riavvio del server
        sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Associa il server all'indirizzo e alla porta specificati
        sock_server.bind((indirizzo, porta))

        # Mette il server in ascolto con una coda massima di 5 connessioni pendenti
        sock_server.listen(5)

        # Ciclo infinito per accettare e gestire connessioni multiple
        while True:
            ricevi_connessioni(sock_server)
            print(f" ---- Server in ascolto su {indirizzo}:{porta} ----")

# --- MAIN ---
# Configurazione del server
IP = "127.0.0.1"           # Indirizzo locale
PORTA = 65432              # Porta di ascolto
DIM_BUFFER = 1024          # Dimensione del buffer per la ricezione dati

# Avvio del server
avvia_server(IP, PORTA)
