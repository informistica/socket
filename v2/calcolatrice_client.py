# Client TCP che invia due numeri e un'operazione al server, riceve il risultato e lo stampa

import socket   # Modulo per la comunicazione di rete
import json     # Modulo per la codifica/decodifica JSON

# --- Configurazione del server a cui connettersi ---
HOST = "127.0.0.1"   # Indirizzo IP del server (localhost)
PORT = 65432         # Porta su cui il server è in ascolto

# Creazione della socket TCP del client usando il costrutto `with` (si chiude automaticamente alla fine)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_service:
    sock_service.connect((HOST, PORT))  # Connessione al server

    # Ciclo continuo per inviare operazioni
    while True:
        # --- Raccolta dati dall'utente ---
        primoNumero = float(input("Inserisci il primo numero: "))  # Primo numero
        operazione = input("Inserisci l'operazione (simbolo): ")   # Operazione (+, -, *, /, %)
        secondoNumero = float(input("Inserisci il secondo numero: "))  # Secondo numero

        # Crea un dizionario con i dati dell'operazione
        messaggio = {
            "primoNumero": primoNumero,
            "operazione": operazione,
            "secondoNumero": secondoNumero
        }

        # Converte il dizionario in una stringa JSON
        messaggio = json.dumps(messaggio)

        # Invia il messaggio codificato al server
        sock_service.sendall(messaggio.encode("UTF-8"))

        # Riceve il risultato dal server (fino a 1024 byte)
        data = sock_service.recv(1024)

        # Stampa il risultato ricevuto, decodificato da byte a stringa
        print("Received: ", data.decode())
