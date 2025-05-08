#Client
import socket
import json

HOST = "127.0.0.1" #Indirizzo del server
PORT = 65432 #Porta usata dal server
#Creazione della socket del server con il costrutto with
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_service:
    sock_service.connect((HOST, PORT))
    while True:
        primoNumero = float(input("Inserisci il primo numero: "))
        operazione = input("Inserisci l'operazione (simbolo)")
        secondoNumero = float(input("Inserisci il secondo numero: "))
        messaggio = {"primoNumero":primoNumero,
                    "operazione":operazione,
                    "secondoNumero":secondoNumero}
        messaggio = json.dumps(messaggio)
        sock_service.sendall(messaggio.encode("UTF-8"))
        data = sock_service.recv(1024) #Il parametro indica la dimensione massima dei dati che possono essere ricevuti in una sola volta

        print("Received: ", data.decode())