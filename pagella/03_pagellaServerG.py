# server.py
import socket
import json

HOST = '127.0.0.1'
PORT=65431
voti = {'Giuseppe Gullo':[("Matematica",9,0),("Italiano",7,3),("Inglese",7.5,4),("Storia",7.5,4),("Geografia",5,7)],
           'Antonio Barbera':[("Matematica",8,1),("Italiano",6,1),("Inglese",9.5,0),("Storia",8,2),("Geografia",8,1)],
           'Nicola Spina':[("Matematica",7.5,2),("Italiano",6,2),("Inglese",4,3),("Storia",8.5,2),("Geografia",8,2)]}
fine=0
uscita=0
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind((HOST,PORT))
  s.listen(2)
  while uscita==0:
    fine=0
    print("[*] In ascolto su %s:%d"%(HOST,PORT))
    clientsocket, address=s.accept()
    with clientsocket as cs:
      print("Connessione da ",address)
      while fine==0:
        data=cs.recv(1024)
        print("24")
        print(data)
        # if len(data)==0:
        if not data:
          break
        data=data.decode()
        if data=="#list":
          messaggio=json.dumps(voti)
          cs.sendall(messaggio.encode("UTF-8"))
          continue
        if data=="#exit":
          fine=1
          cs.sendall("Uscita".encode("UTF-8"))
          break
        if data=="#close":
          fine=1
          uscita=1
          cs.sendall("Uscita".encode("UTF-8"))
          break
        # Fine dei messaggi con una parola
        if "#set" in data:
          comando, nome=list(map(lambda x:x.strip(),data.split("/")))
          if voti.get(nome,None)==None:
            voti[nome]=[]
            cs.sendall("ok".encode("UTF-8"))
            continue
          cs.sendall("ko".encode("UTF-8"))
          continue
        if "#get" in data:
          param = data.split('/')
          nomeStudente=str(param[1])
          ris={}
          ris['voti']=voti.get(nomeStudente,None)
          if ris!=None:
            ris['ok']="ok"
            messaggio=json.dumps(ris)
            cs.sendall(messaggio.encode("UTF-8"))
            continue
          ris['ok']="ko"
          messaggio=json.dumps(ris)
          cs.sendall(messaggio.encode("UTF-8"))
          continue
        if "#put" in data:
          comando, nome, materia, voto, ore=list(map(lambda x:x.strip(),data.split("/")))
          if voti.get(nome,None)==None:
            cs.sendall("Studente non trovato".encode("UTF-8"))
            continue
          elenco=voti[nome]
          ok=True
          for tupla in elenco:
            if tupla[0]==materia:
              cs.sendall("Materia già presente".encode("UTF-8"))
              ok=True
              break
          if ok==False:
            continue
          voti[nome].append((materia,int(voto),int(ore)))
          cs.sendall("Voto inserito con successo".encode("UTF-8"))
          continue