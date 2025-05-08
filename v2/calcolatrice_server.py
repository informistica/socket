# Server TCP che riceve due numeri e un'operazione dal client, esegue il calcolo e restituisce il risultato

import socket    # Modulo per la comunicazione di rete
import json      # Modulo per la gestione dei dati in formato JSON

# --- Configurazione del server ---
IP = "127.0.0.1"          # Indirizzo IP locale (localhost)
PORTA = 65432             # Porta su cui il server sarà in ascolto
DIM_BUFFER = 1024         # Dimensione massima dei dati da ricevere

# Creazione della socket del server (TCP) usando il costrutto `with` per gestire automaticamente la chiusura
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_server:
    sock_server.bind((IP, PORTA))     # Collega la socket all'indirizzo IP e porta specificati
    sock_server.listen()              # Mette la socket in modalità ascolto
    print(f"Server in ascolto su {IP}:{PORTA}...")

    # Ciclo principale per accettare e gestire le connessioni
    while True:
        # Attende una nuova connessione da parte di un client
        sock_service, address_client = sock_server.accept()

        # Gestione della connessione usando un secondo costrutto `with` per chiudere automaticamente la connessione
        with sock_service as sock_client:
            # Riceve i dati dal client (massimo DIM_BUFFER byte)
            data = sock_client.recv(DIM_BUFFER)
            
            # Se non arrivano dati, esce dal ciclo (connessione chiusa dal client)
            if not data:
                break

            # Decodifica i byte ricevuti e li trasforma da stringa JSON a dizionario Python
            data = data.decode()
            data = json.loads(data)

            # Estrae i numeri e l'operazione dal dizionario
            primoNumero = data["primoNumero"]
            operazione = data["operazione"]
            secondoNumero = data["secondoNumero"]

            # --- Calcolo del risultato ---
            risultato = 0
            if operazione == "+":
                risultato = primoNumero + secondoNumero
            elif operazione == "-":
                risultato = primoNumero - secondoNumero
            elif operazione == "*":
                risultato = primoNumero * secondoNumero
            elif operazione == "/":
                # Gestione del caso di divisione per zero
                if secondoNumero != 0:
                    risultato = primoNumero / secondoNumero
                else:
                    risultato = "Impossibile"
            elif operazione == "%":
                risultato = primoNumero % secondoNumero

            # Stampa il risultato sul lato server (debug/log)
            print(risultato)

            # Invia il risultato al client (convertito in stringa e codificato in byte)
            sock_client.sendall(str(risultato).encode())
