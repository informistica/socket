#!/usr/bin/env python3
import socket



SERVER_ADDRESS = '127.0.0.1'

SERVER_PORT = 22224

sock_listen = socket.socket()

sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock_listen.bind((SERVER_ADDRESS, SERVER_PORT))

sock_listen.listen(5)

print("Server in ascolto su %s." % str((SERVER_ADDRESS, SERVER_PORT)))

protocollo=["Receive SYN","Send SYN + ACK", "Receive ACK", "Handshake ok"]

while True:
    sock_service, addr_client = sock_listen.accept()
    print("\nConnessione ricevuta da " + str(addr_client))
    print("\nAspetto di ricevere i dati ")
    while True:
        dati = sock_service.recv(2048)
        if not dati:
            print("Fine dati dal client. Reset")
            break
        
        dati = dati.decode()
        step,msg=dati.split(";")
        print(f"{protocollo[int(step)]}")
        if step=='3':
            print("Fine protocollo  " + str(addr_client))
            break
        dati = str(int(step)+1)+";"+ protocollo[int(step)+1]
        print(f"Invio: {dati}")
        dati = dati.encode()
        sock_service.send(dati)

    sock_service.close()