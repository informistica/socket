#Client
import socket
import json
import random
import os
import time
import threading
import multiprocessing

HOST = "127.0.0.1" #Indirizzo del server
PORT = 22224 #Porta usata dal server
NUM_WORKERS = 15
OPERAZIONI = ["+", "-", "*", "/", "%"]

def genera_richieste(address, port):
    #Creazione della socket del server con il costrutto with
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_service:
        sock_service.connect((address, port))

        primoNumero = random.randint(0, 100)
        operazione = OPERAZIONI[random.randint(0, 3)] 
        secondoNumero = random.randint(0, 100)
        messaggio = {"primoNumero":primoNumero,
                    "operazione":operazione,
                    "secondoNumero":secondoNumero}
        messaggio = json.dumps(messaggio)
        sock_service.sendall(messaggio.encode("UTF-8"))
        start_time_thread = time.time()
        data = sock_service.recv(1024) #Il parametro indica la dimensione massima dei dati che possono essere ricevuti in una sola volta
    
    end_time_thread = time.time()
    print("Received: ", data.decode())
    print(f"{threading.current_thread().name} exec time = ", end_time_thread - start_time_thread)


if __name__ == "__main__":
    start_time = time.time()
    threads = [threading.Thread(target=genera_richieste, args=(HOST, PORT)) for _ in range(NUM_WORKERS)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    end_time = time.time()

    print("Tempo totale impiegato = ", end_time - start_time)