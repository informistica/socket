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
NUM_WORKERS = 1
OPERAZIONI = ["list", "get", "set", "put", "close"]

def genera_richieste(address, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_service:
        sock_service.connect((address, port))
        #Ciclo inserimento operazione
        while True:
            valueNotValid = True
            while valueNotValid:
                operazione = input("Inserire operazione: ")
                comando = operazione.split(" ")[0]
                if comando in OPERAZIONI:
                    valueNotValid = False
            
            parametri = "".join(operazione.split(" ")[1:]) #oppure "".join()
            
            dati = {"comando": comando,
                    "parametri": parametri}
            dati = json.dumps(dati)
            print(dati)
            sock_service.sendall(dati.encode("UTF-8"))
            #start_time_thread = time.time()
            data = sock_service.recv(2048)  
            if not data:
                break  
        #end_time_thread = time.time()
            data = data.decode()
            data = json.loads(data)
            print("Risposta: ", data["risposta"])
            print("Valori: ", data["valori"])
            #print(f"{threading.current_thread().name} exec time = ", end_time_thread - start_time_thread)

if __name__ == "__main__":
    start_time = time.time()
    threads = [threading.Thread(target = genera_richieste, args = (HOST, PORT)) for _ in range(NUM_WORKERS)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    end_time = time.time()

    print("Tempo totale impiegato = ", end_time - start_time)