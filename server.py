#!/usr/bin/env python3


#premessa sul formato di dati scambiato
input_string = 'Hello'
print(type(input_string))
input_bytes_encoded = input_string.encode()
print(type(input_bytes_encoded))
print(input_bytes_encoded)
output_string=input_bytes_encoded.decode()
print(type(output_string))
print(output_string)

#https://realpython.com/python-sockets/
import socket

HOST = '127.0.0.1'  # Indirizzo dell'interfaccia standard di loopback (localhost)
PORT = 65432        # Porta di ascolto, la lista di quelle utilizzabili parte da >1023)
#https://www.pythonforbeginners.com/files/with-statement-in-python
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_listen:
    sock_listen.bind((HOST, PORT))
    sock_listen.listen()
    print("[*] In ascolto su %s:%d" % (HOST, PORT))
    sock_service, address_client = sock_listen.accept()
    with sock_service as ss:
        print('Connessione da', address_client)
        while True:
            data = ss.recv(1024)
            if not data:
                break
            ss.sendall(data)