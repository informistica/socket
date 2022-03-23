
import socket

# (127.0.0.1 indirizzo "localhost").
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22222

# Crea la  socket
c = socket.socket()

# Connette la socket al server
c.connect((SERVER_ADDRESS, SERVER_PORT))

print("Connesso a " + str((SERVER_ADDRESS, SERVER_PORT)))
while True:
    try:
        dati = input("Inserisci i dati da inviare: ")
    except EOFError:
        print("\nOkay. Exit")
        break

    if not dati:
        print("Non puoi inviare una stringa vuota!")
        continue

    # Converte la stringa in byte
    dati = dati.encode()

    # invia al server
    c.send(dati)

    # Riceve la risposta dal server
    dati = c.recv(2048)
    if not dati:
        print("Server non risponde. Exit")
        break

    # Converte in stringa
    dati = dati.decode()

    print("Ricevuto dal server:")
    print(dati + '\n')

c.close()