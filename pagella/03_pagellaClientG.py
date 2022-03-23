import socket
import json
import pprint

HOST="127.0.0.1"
PORT=65431

def controllaComando(comando):
  if(comando=="#list" or comando=="#exit" or comando=="#close"):
    return True
  if("#set" in comando or "#get" in comando or "#put" in comando):
    return True
  return False


with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
  s.connect((HOST,PORT))
  while True:
    print("\nComandi disponibili: ")
    print("#list: per vedere i voti inseriti")
    print("#set /nomestudente: per inserire uno studente")
    print("#put /nomestudente/materia/voto/ore: per aggiungere i voti della materia allo studente")
    print("#get /nomestudente: per richiedere i voti di uno studente")
    print("#exit: per chiudere solo il client")
    print("#close: per chiudere sia client sia server")
    messaggio=input("Digita il comando: ")
    ok=controllaComando(messaggio)
    if ok==False:
      print("Comando non valido")
      continue
    s.sendall(messaggio.encode("UTF-8"))
    data=s.recv(1024)
    if messaggio=="#list":
      data=json.loads(data)
      pp=pprint.PrettyPrinter(indent=4)
      pp.pprint(data)   
      continue
    if "#set" in messaggio:
      data=data.decode()
      if data=="ok":
        print("Studente aggiunto con successo")
      else:
        print("Studente già presente")
      continue
    if "#get" in messaggio:
      data=json.loads(data)
      if data['ok']=="ok":
        print(data['voti'])
      else:
        print("Studente non trovato")
      continue
    if "#put" in messaggio:
      print(data.decode())
      continue
    if messaggio=="#exit":
      if data.decode()=="Uscita":
        print("Chiusura connessione client")
      else:
        print("Errore nella chiusura client")
      break
    if messaggio=="#close":
      if data.decode()=="Uscita":
        print("Chiusura connessione client e server")
      else:
        print("Errore nella chiusura client e server")
      break