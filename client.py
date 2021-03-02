import socket
import sys
import random
import os
import time
import threading
import multiprocessing
from util import benchmark

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 65432

NUM_WORKERS = 15
COMANDI = [
    "somma",
    "sottrazione",
    "moltiplicazione",
    "divisione",
]


def print_info():
    print(f"Client PID: {os.getpid()}, Process Name: {multiprocessing.current_process().name}, Thread Name: {threading.current_thread().name}")


def connetti(address, port):
    try:
        s = socket.socket()
        s.connect((address, port))
        print(
            f"{threading.current_thread().name} Connessione al server: {address}:{port}")
        return s
    except Exception as errore:
        print(
            f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n{errore}")
        sys.exit()


def invia_riciesta(address, port):
    print_info()
    start_time_thread = time.time()

    s = connetti(address, port)

    operazione = random.choice(COMANDI)

    comando = ";".join([
        operazione,  # opcode
        str(random.randint(1, 100)),  # numero 1
        str(random.randint(1, 100)),  # numero 2
    ])
    s.send(comando.encode())

    data = s.recv(2048)
    if not data:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")

    res = data.decode()
    print(f"{threading.current_thread().name}: Ricevuto dal server:")
    print(res + '\n')

    s.close()

    end_time_thread = time.time()
    print(f"{threading.current_thread().name} execution time=",
          end_time_thread-start_time_thread)


def run_seq():
    for _ in range(0, NUM_WORKERS):
        invia_riciesta(SERVER_ADDRESS, SERVER_PORT)


def run_threads():
    threads = [threading.Thread(target=invia_riciesta, args=(
        SERVER_ADDRESS, SERVER_PORT,)) for _ in range(NUM_WORKERS)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]


def run_processes():
    processes = [multiprocessing.Process(target=invia_riciesta, args=(
        SERVER_ADDRESS, SERVER_PORT,)) for _ in range(NUM_WORKERS)]
    [process.start() for process in processes]
    [process.join() for process in processes]


if __name__ == '__main__':
    benchmark([
        ('sequential', run_seq),
        ('threads', run_threads),
        ('processes', run_processes),
    ])