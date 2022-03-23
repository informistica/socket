import socket

# lasciando il campo vuoto sarebbe la stessa cosa (localhost)
SERVER_ADDRESS = '127.0.0.1'

# Numero di porta, deve essere >1024 perchè le altre sono riservate.)
SERVER_PORT = 22224

# Crea la socket
s = socket.socket()
op=" "
n1=0
n2=0
# Opzionale: permette di riavviare subito il codice, 
# altrimenti bisognerebbe aspettare 2-4 minuti prima di poter riutilizzare(bindare) la stessa porta
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Associa indirizzo e porta.  Nota che  l'argumento è una tupla:
s.bind((SERVER_ADDRESS, SERVER_PORT))

# Imposta quante connessioni pendenti possono essere accodate
s.listen(5)

print("Server in ascolto su %s. Termina con ko" % str((SERVER_ADDRESS, SERVER_PORT)))

# Abbiamo creato un endpoint di ascolto dal quale accettare connessioni in entrata
# Il loop accetterà una connessione alla volta e la servirà finchè il client non si disconnette
# dopodichè il server ne accetterà di nuove tra quelle in coda

while True:
    c, addr = s.accept()
    print("\nConnessione ricevuta da %s" % str(addr))
    print("\nScrivere operazione.n1.n2 ")

    while True:
        dati = c.recv(2048)
        if not dati :
            print("Fine dati dal client. Reset")
            break
        

        # Decodifica i byte ricevuti in una stringa unicode
        dati = dati.decode()
        if dati=="ko":
            print("Fine dati dal client. Exit")
            break
        op,n1,n2=dati.split(";")
        if op=="piu":
            dati=str(float(n1)+float(n2))
        elif op=="meno":
            dati=str(float(n1)-float(n2))
        elif op=="per":
            dati=str(float(n1)*float(n2))
        elif op=="diviso":
            dati=str(float(n1)/float(n2))

        print("Ricevuto: '%s'" % dati)

        dati = "Risposta: " + str(addr) + ". Il risultato dell'operazione: '" + op + "' tra '"+str(n1)+"' e '"+str(n2)+"' è: '"+dati+"'"

        # codifica la stringa in byte
        dati = dati.encode()

        # Invia la risposta al client.
        c.send(dati)

    c.close()