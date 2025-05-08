#Server
import socket
import json
from threading import Thread
import classi


def ricevi_comandi(sock_service, addr_client):
    print("Client: ", addr_client)
    with sock_service as sock_client:
            while True: #Metto tutto in un ciclo, se i dati non ci sono si chiude la sessione
                data = sock_client.recv(DIM_BUFFER)
                if not data:
                    break
                data = data.decode()
                data = json.loads(data)
                
                comando = data["comando"]
                parametri = data["parametri"]
                parametri = parametri.split("/")[1:] #[Nome studente, materia, voto, ore]
                
                print(comando, parametri)
                
                risposta = "Default KO"
                valori = ""
                if comando == "list":
                    print("LIST by ", (sock_service, addr_client))
                    valori = str(tabellone)
                    risposta = "ok"
                elif comando == "get":
                    print("GET by ", (sock_service, addr_client))
                    if tabellone.cercaPagella(parametri[0]) != -1:
                        valori = tabellone[tabellone.cercaPagella(parametri[0])]
                        risposta = "ok"
                    else:
                        risposta = "ko"
                        valori = "Studente non trovato"   
                elif comando == "set":
                    print("SET by ", (sock_service, addr_client))
                    if tabellone.cercaPagella(parametri[0]) == -1:
                        tabellone.push(classi.Pagella(parametri[0]))
                        valori = "Studente inserito"
                        risposta = "ok"
                    else:
                        valori = "Studente già inserito"
                        risposta = "ko"
                elif comando == "put":
                    print("PUT by ", (sock_service, addr_client))
                    if tabellone.cercaPagella(parametri[0]) != -1 and parametri[1] not in tabellone.pagelle[tabellone.cercaPagella(parametri[0])].materie: #Valori true-ish e false-ish dovrebbero salvarmi dal far andare in errore questa riga
                        tabellone.pagelle[tabellone.cercaPagella(parametri[0])].aggiungiMateria((parametri[1], parametri[2], parametri[3]))
                        risposta = "ok"
                        valori = "Dati inseriti"
                    
                    else:
                        risposta = "ko"
                        valori = "Studente non presente"

                elif comando == "close":
                    print("CLOSE by ", (sock_service, addr_client))
                    sock_client.close()
                
                
                dati = {"risposta":risposta,
                        "valori":valori}
                dati = json.dumps(dati)
                sock_client.sendall(str(dati).encode("UTF-8"))

def ricevi_connessioni(sock_listen):
        sock_service, address_client = sock_listen.accept()
        try:
            Thread(target = ricevi_comandi, args = (sock_service, address_client)).start()
        except Exception as e:
            print(e)

def avvia_server(indirizzo, porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_server:
        sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_server.bind((indirizzo, porta))
        sock_server.listen(5)
        while True:
            ricevi_connessioni(sock_server)
            print(f" ---- Server in ascolto su {indirizzo}:{porta} ----")

#MAIN
#Configurazione del server
IP = "127.0.0.1"
PORTA = 22224
DIM_BUFFER = 2048
if __name__ == "__main__":
    tabellone = classi.Tabellone()
    avvia_server(IP, PORTA)