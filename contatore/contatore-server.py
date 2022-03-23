
import socket

# lasciando il campo vuoto sarebbe la stessa cosa (localhost)
SERVER_ADDRESS = '127.0.0.1'

# Numero di porta, deve essere >1024 perchè le altre sono riservate.)
SERVER_PORT = 22222

# Crea la socket
s = socket.socket()

# Optionale: permette di riavviare subito il codice, .
# altrimenti bisognerebbe aspettare 2-4 minuti prima di poter riutilizzare(bindare) la stessa porta
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Associa indirizzo e porta.  Nota che  l'argumento è una tupla:
s.bind((SERVER_ADDRESS, SERVER_PORT))

# Imposta quante connessioni pendenti possono essere accodate
s.listen(5)

print("Server in ascolto su %s. Termina il server con Ctrl-C" % str((SERVER_ADDRESS, SERVER_PORT)))

# Abbiamo creato un endpoint di ascolto dal quale accettare connessioni in entrata
# Il loop accetterà una connessione alla volta e la servirà finchè il client non si disconnette
# dopodichè il server ne accetterà di nuove tra quelle in coda

while True:
    c, addr = s.accept()
    print("\nConnection received from %s" % str(addr))
    contatore=0
    while True:
        dati = c.recv(2048)
        contatore+=1
        if not dati:
            print("End of file from client. Resetting")
            break
        # Decodifica i byte ricevuti in una stringa unicode
        dati = dati.decode()
        print("Ricevuto '%s' dal client" % dati)
        if dati!="KO":
            dati = "Ciao, " + str(addr) + ". Ho ricevuto questo da te : '" + str(contatore)+ ") "+ dati + "'"
            # codifica la stringa in byte
            dati = dati.encode()
            # Invia la risposta al client.
            c.send(dati)
        else:
            print("Chiudo connessione con il client")
            dati = dati.encode()
            c.send(dati)
            c.close()
            print("Resto in attesa di nuove connessioni")
            break

    