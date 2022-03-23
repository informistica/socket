import socket
import os
import json
import pprint

# lasciando il campo vuoto sarebbe la stessa cosa (localhost)
SERVER_ADDRESS = '127.0.0.1'

# Numero di porta, deve essere >1024 perchè le altre sono riservate.)
SERVER_PORT = 22225

# Crea la socket
s = socket.socket()

# Opzionale: permette di riavviare subito il codice, 
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

#Il server dispone di un dizionario per contenere il tabellone dei voti
students = {
    "Giuseppe Gullo":[("Matematica", 9, 0), ("Italiano", 7, 3), ("Inglese", 7.5, 4), ("Storia", 7.5, 4), ("Geografia", 5, 7)],
    "Antonio Barbera":[("Matematica", 8, 1), ("Italiano", 6, 1), ("Inglese", 9.5, 0), ("Storia", 8, 2), ("Geografia", 8, 1)],
    "Nicola Spina":[("Matematica", 7.5, 2), ("Italiano", 6, 2), ("Inglese", 4, 3), ("Storia", 8.5, 2), ("Geografia", 8, 2)]
}
while True:
    c, addr = s.accept()
    print("\nConnessione ricevuta da %s" % str(addr))
    while True:
        request = c.recv(1024)
        request=request.decode()
        request=request.strip()
        print ("[*] Received: %s" % request)
        # send back a packet
        if request == "#list":
            serialized_dict = json.dumps(students)
            c.sendall(serialized_dict.encode())   
        elif request.find('#get') != -1:
            param = request.split('/')
            nomestudente=str(param[1])
            if students.get(nomestudente) == None:
                msg="Studente non trovato"
                print (msg)
                c.sendall(msg.encode("UTF-8"))
            else:
                #msg="ok"
                #print (msg)
                #c.send(msg.encode())
                serialized_dict = json.dumps(students.get(nomestudente))
                print(serialized_dict)
                c.sendall(serialized_dict.encode("UTF-8"))
        elif request.find('#put') != -1:
            vuoto,studente,materia,voto,ore = request.split('/')
            if studente in students:
                dati=students.get(nomestudente)
                if materia in dati[0]:
                    c.sendall("Materia già presente".encode())
                    print("Materia già presente")
                else:
                    students[studente].append((materia,voto,ore))
                    c.sendall("Materia inserita".encode())
            else:
                c.send("Studente non presente, usa #set per inserirlo ".encode())
        elif request.find('#set') != -1:
            vuoto,studente= request.split('/')
            if studente in students:
                c.sendall("Studente già presente".encode())
            else:
                students.update({studente: []})
                c.sendall("Studente inserito ".encode())  
        elif request == "#close":
            #print response
            fine = 0
            print ("Termino la connessione")
            c.sendall("closed".encode())
            fine=1 
    c.close()