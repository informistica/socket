import socket
import sys
import random
import os
import time
import threading
import multiprocessing

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22224
NUM_WORKERS=15

def genera_ricieste(address,port):
    start_time_thread= time.time()
    print(f"Client PID: {os.getpid()}, Process Name: {multiprocessing.current_process().name}, Thread Name: {threading.current_thread().name}")
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"{threading.current_thread().name} Connessione al server: {address}:{port}")
    except s.error as errore:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n{errore}")
        sys.exit()
    comandi=['piu','meno','per','diviso']
    operazione=comandi[random.randint(0,3)]
    dati=str(operazione)+";"+str(random.randint(1,100))+";"+str(random.randint(1,100))
    dati=dati.encode()
    s.send(dati)
    dati=s.recv(2048)
    if not dati:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
    dati=dati.decode()
    print(f"{threading.current_thread().name}: Ricevuto dal server:")
    print(dati + '\n')
    dati="ko"
    dati=dati.encode()
    s.send(dati)
    s.close()
    end_time_thread=time.time()
    print(f"{threading.current_thread().name} execution time=", end_time_thread-start_time_thread)

if __name__ == '__main__':
    start_time=time.time()
    for _ in range (0,NUM_WORKERS):
        genera_ricieste(SERVER_ADDRESS, SERVER_PORT)
    end_time=time.time()
    print("Total SERIAL time=", end_time - start_time)

    start_time=time.time()
    threads=[threading.Thread(target=genera_ricieste, args=(SERVER_ADDRESS, SERVER_PORT,)) for _ in range(NUM_WORKERS)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    end_time=time.time()
    print("Total THREADS time= ", end_time - start_time)

    start_time=time.time()
    processes =[multiprocessing.Process(target=genera_ricieste, args=(SERVER_ADDRESS, SERVER_PORT,)) for _ in range(NUM_WORKERS)]
    [process.start() for process in processes]
    [process.join() for process in processes]
    end_time=time.time()
    print("Total PROCESS time= ", end_time - start_time)