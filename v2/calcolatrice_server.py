#Server
import socket
import json

#Configurazione del server
IP = "127.0.0.1"
PORTA = 65432
DIM_BUFFER = 1024

#Creazione della socket del server con il costrtto with
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_server:
    sock_server.bind((IP, PORTA))
    sock_server.listen()
    print(f"Server in ascolto su {IP}:{PORTA}...")
    #Loop principale del server
    while True:
        #accetta le connessioni
        sock_service, address_client = sock_server.accept()

        with sock_service as sock_client:
            #leggi i dati inviati dal client
            data = sock_client.recv(DIM_BUFFER)
            if not data:
                break
            data = data.decode()
            data = json.loads(data)
            primoNumero = data["primoNumero"]
            operazione = data["operazione"]
            secondoNumero = data["secondoNumero"]

            #Calcolo il risultato e lo invio
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
            
            print(risultato)
            sock_client.sendall(str(risultato).encode()) #Invia a tutti i client