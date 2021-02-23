#Il client invia NUM_WORKERS richieste in serie al server

#!/usr/bin/env python3

import socket
import sys
import random
import os
import time
import threading
import multiprocessing

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22224
NUM_WORKERS = 15


def genera_richieste(address, port):
    #time.sleep(0.1)
    start_time_thread = time.time()
    print("Client PID: %s, Process Name: %s, Thread Name: %s" % (
        os.getpid(),
        multiprocessing.current_process().name,
        threading.current_thread().name)
    )
    try:
        s = socket.socket()  # creazione socket client
        s.connect((address, port))  # connessione al server
        print(f"{threading.current_thread().name} Connessessione al Server: {address}:{port}")
    except s.error as errore:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n{errore}")
        sys.exit()
    comandi=['piu','meno','per','diviso']
    operazione = comandi[random.randint(0,3)]
    dati = str(operazione)+";"+str(random.randint(1,100))+";"+str(random.randint(1,100))
    dati = dati.encode()
    s.send(dati)
    dati = s.recv(2048)
    if not dati:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
       

    dati = dati.decode()
    print(f"{threading.current_thread().name} Ricevuto dal server:")
    print(dati + '\n')
    #dati = "ko"
    #dati = dati.encode()
    #s.send(dati)
    s.close
    end_time_thread = time.time()
    print(f"{threading.current_thread().name} execution time =", end_time_thread - start_time_thread)
   
   
if __name__ == '__main__':
    # Run tasks using serial function
    start_time = time.time()
    for _ in range(0,NUM_WORKERS):
        genera_richieste(SERVER_ADDRESS, SERVER_PORT)
    end_time = time.time()    
    print("Total SERIAL time=", end_time - start_time)

    # Run tasks using threads
    start_time = time.time()
    threads = [threading.Thread(target=genera_richieste,args=(SERVER_ADDRESS, SERVER_PORT,)) for _ in range(NUM_WORKERS)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    end_time = time.time()
    print("Total THREADS time=", end_time - start_time)

     # Run tasks using processes
    start_time = time.time()
    processes = [multiprocessing.Process(target=genera_richieste,args=(SERVER_ADDRESS, SERVER_PORT,)) for _ in range(NUM_WORKERS)]
    [process.start() for process in processes]
    [process.join() for process in processes]
    end_time = time.time()
    print("\nTotal PROCESS time=", end_time - start_time)
    
# if __name__ == '__main__': consente al nostro codice di capire se stia venendo eseguito come script a se stante,
# o se è invece stato richiamato come modulo da un qualche programma per usare una o più delle sua varie
# funzioni e classi.
