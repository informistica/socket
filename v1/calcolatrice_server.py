import socket, json  # Importa i moduli necessari per la comunicazione di rete (socket) e per la gestione dei dati in formato JSON

# Imposta l'indirizzo IP e la porta su cui il server ascolterà
SERVER_IP = "127.0.0.1"  # IP locale (localhost)
SERVER_PORT = 5005       # Porta su cui il server riceve le richieste
BUFFER_SIZE = 1024       # Dimensione massima dei dati ricevuti in un singolo pacchetto

# Crea un socket UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Associa il socket all'indirizzo e alla porta specificati
s.bind((SERVER_IP, SERVER_PORT))

# Inizio del ciclo principale del server: ascolta continuamente le richieste dei client
while True:
    # Riceve i dati dal client (massimo BUFFER_SIZE byte), insieme all'indirizzo del mittente
    data, addr = s.recvfrom(BUFFER_SIZE)
    
    # Se non riceve dati, termina il ciclo
    if not data:
        break

    # Decodifica i byte ricevuti in una stringa e poi li converte da JSON a un dizionario Python
    data = data.decode()
    data = json.loads(data)

    # Estrae i valori necessari dal dizionario
    primoNumero = data["primoNumero"]
    operazione = data["operazione"]
    secondoNumero = data["secondoNumero"]

    # Inizializza la variabile per il risultato dell'operazione
    risultato = 0

    # Esegue l'operazione richiesta tra i due numeri
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
            risultato = "Impossibile"  # Gestione divisione per zero
    elif operazione == "%":
        risultato = primoNumero % secondoNumero

    # Invia il risultato dell'operazione al client (convertito in stringa e codificato in byte)
    s.sendto(str(risultato).encode(), addr)
