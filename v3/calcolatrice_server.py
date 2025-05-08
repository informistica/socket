#Server
import socket
import json
from threading import Thread

def ricevi_comandi(sock_service, addr_client):
    print("Client: ", addr_client)
    with sock_service as sock_client:
            while True: #Metto tutto in un ciclo, se i dati non ci sono si chiude la sessione
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
                sock_client.sendall(str(risultato).encode()) #Sendall perchè tanto c'è un solo client connesso per volta

def ricevi_connessioni(sock_listen):
        sock_service, address_client = sock_listen.accept()
        try:
            Thread(target = ricevi_comandi, args = (sock_service, address_client)).start()
        except Exception as e:
            print(e)

def avvia_server(indirizzo, porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_server:
        sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_server.bind((indirizzo, porta))
        sock_server.listen(5)
        while True:
            ricevi_connessioni(sock_server)
            print(f" ---- Server in ascolto su {indirizzo}:{porta} ----")

#MAIN
#Configurazione del server
IP = "127.0.0.1"
PORTA = 65432
DIM_BUFFER = 1024

avvia_server(IP, PORTA)