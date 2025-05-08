import socket  # Importa il modulo per la comunicazione via rete (UDP)
import json    # Importa il modulo per la codifica/decodifica JSON

# Imposta l'indirizzo IP e la porta del server a cui inviare i dati
SERVER_IP = "127.0.0.1"  # Indirizzo IP locale (localhost)
SERVER_PORT = 5005       # Porta su cui il server riceve i dati
BUFFER_SIZE = 1024       # Dimensione massima dei dati ricevuti

# Crea un socket UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Inizio del ciclo per inviare operazioni al server
while True:
    # --- Blocco 1: Raccolta dati dall'utente ---
    primoNumero = float(input("Inserisci il primo numero: "))
    operazione = input("Inserisci l'operazione (simbolo): ")
    secondoNumero = float(input("Inserisci il secondo numero: "))

    # Prepara un dizionario con i dati inseriti
    messaggio = {
        "primoNumero": primoNumero,
        "operazione": operazione,
        "secondoNumero": secondoNumero
    }

    # Converte il dizionario in stringa JSON
    messaggio = json.dumps(messaggio)

    # Invia il messaggio codificato in byte al server specificato
    s.sendto(messaggio.encode("UTF-8"), (SERVER_IP, SERVER_PORT))

    # --- Ricezione del risultato dal server ---
    # Riceve il risultato come byte e lo decodifica in stringa
    data = s.recv(BUFFER_SIZE)
    print("Risultato: ", data.decode())
