#client calcoClientMulti.py
import socket
import sys
import random
import os
import time
import threading
import multiprocessing
import json

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22225
NUM_WORKERS=2

def genera_richieste(num,address,port):
    start_time_thread= time.time()
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()
    
    comandi=['+','-','*','%']
    primoNumero=random.randint(1,100)
    operazione=comandi[random.randint(0,3)]
    secondoNumero=random.randint(1,100)

    messaggio={'primoNumero':primoNumero,
    'operazione':operazione,
    'secondoNumero':secondoNumero}
    print(f"Invio richiesta {messaggio}")
    messaggio=json.dumps(messaggio) 
    s.sendall(messaggio.encode("UTF-8")) 
    data=s.recv(1024)
    if not data:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
    else:
        print(f"{threading.current_thread().name}: Risultato: {data.decode()}") # trasforma il vettore di byte in stringa
    s.close()
    end_time_thread=time.time()
    print(f"{threading.current_thread().name} tempo di esecuzione time=", end_time_thread-start_time_thread)

if __name__ == '__main__':
    start_time=time.time()
    for num in range (0,NUM_WORKERS):
        genera_richieste(num,SERVER_ADDRESS, SERVER_PORT)
    end_time=time.time()
    print("Total SERIAL time=", end_time - start_time)
     
    start_time=time.time()
    threads=[]
    for num in range(NUM_WORKERS):
        threads.append(threading.Thread(target=genera_richieste, args=(num,SERVER_ADDRESS, SERVER_PORT,)))
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    end_time=time.time()
    print("Total THREADS time= ", end_time - start_time)

    start_time=time.time()
    process=[]
    for num in range(NUM_WORKERS):
        process.append(multiprocessing.Process(target=genera_richieste, args=(num,SERVER_ADDRESS, SERVER_PORT,)))
    [process.start() for process in process]
    [process.join() for process in process]
    end_time=time.time()
    print("Total PROCESS time= ", end_time - start_time)