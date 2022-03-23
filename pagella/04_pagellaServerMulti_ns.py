#pagella server pagellaServerMulti_V01.py versione 1.0 multithread
#nome del file : pagellaServerMulti_V01.py
import socket
from threading import Thread
import json

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22001

def ricevi_comandi(sock_service,addr_client):
    print("avviato")
    
    while True:
        data=sock_service.recv(1024)
        if not data: 
                break
        data=data.decode()
        data=json.loads(data)
        
        # completare:
        #1. recuperare materia, voto e assenze

        ris="\nmateria : "+materia+" con la seguente valutazione "
        #2. restituire la materia e un giudizio testuale sapendo che :
        # voto < 4 Gravemente insufficiente
        # voto < 5 Insufficiente
        # voto = 6 Sufficiente
        # voto compreso tra 6 e 7 Discreto 
        # voto compreso tra 7 e 9 Buono
        # voto > 9 Ottimo
        
        
        
        ris=str(ris)
        sock_service.sendall(ris.encode("UTF-8"))

    sock_service.close()

def ricevi_connessioni(sock_listen):
        sock_service, addr_client = sock_listen.accept()
        print("\nConnessione ricevuta da " + str(addr_client))
        print("\nCreo un thread per servire le richieste ")
        try:
            Thread(target=ricevi_comandi,args=(sock_service,addr_client)).start()
        except:
            print("il thread non si avvia")
            sock_listen.close()
        
def avvia_server(SERVER_ADDRESS,SERVER_PORT):
    sock_listen=socket.socket()
    sock_listen.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock_listen.bind((SERVER_ADDRESS,SERVER_PORT))
    sock_listen.listen(5)
    print("Server in ascolto su %s." %str((SERVER_ADDRESS,SERVER_PORT)))
    ricevi_connessioni(sock_listen)

if __name__=='__main__':
    avvia_server(SERVER_ADDRESS,SERVER_PORT)