import socket
import os
import json
import pprint

# (127.0.0.1 indirizzo "localhost").
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22225

# Crea la  socket
client = socket.socket()

# Connette la socket al server
client.connect((SERVER_ADDRESS, SERVER_PORT))

print("Connesso a " + str((SERVER_ADDRESS, SERVER_PORT)))
print("Comandi disponibili;")
print( "#list : per vedere tutti i voti inseriti")
print( "#get /nomestudente : per richiedere i voti di uno studente")
print( "#set /nomestudente : per inserire uno studente")
print( "#put /nomestudente/materia/voto/ore : per aggiungere i voti della materia allo studente")
print( "#close : per chiudere la connessione")


fine=1
while fine!=0:
    try:
        comando = input("Digita il comando: ")
    except EOFError:
        print("\nOkay. Exit")
        break

    if not comando:
        print("Non puoi inviare una stringa vuota!")
        continue
    # invia al server
    client.send(comando.encode())
    dati = client.recv(4096)
    if not dati:
        print("Server non risponde. Exit")
        break
    dati = dati.decode()
    if comando=="#list":
        stud_dict = json.loads(dati)
        print ("Dizionario studenti")
        pp=pprint.PrettyPrinter(indent=4)
        pp.pprint(stud_dict)
    elif comando.find('#get')!=-1:
        if dati!="Studente non trovato":
            dati = client.recv(4096)
            dati = dati.decode()
            stud_dict = json.loads(dati)
            pp=pprint.PrettyPrinter(indent=4)
            pp.pprint(stud_dict)   
        else:
            print ("Studente non trovato")
    elif comando.find('#put')!=-1:
        print ("Inserimento materia in corso ... " + dati)
    elif comando.find('#set')!=-1:
        print ("Inserimento studente in corso ... " + dati)
    elif comando=="#close":
        if dati=="closed":
            print ("Connessione chiusa")
            fine = 0
        else:
            print ("Problemi nella chiusura della connessione")

client.close()