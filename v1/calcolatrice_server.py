import socket, json

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((SERVER_IP, SERVER_PORT))

#Blocco 2
while True:
    #Ricevo i dati
    data, addr = s.recvfrom(1024)
    if not data:
        break
    data = data.decode()
    data = json.loads(data)
    primoNumero = data["primoNumero"]
    operazione = data["operazione"]
    secondoNumero = data["secondoNumero"]

    #Calcolo il risultato e lo invio
    risultato = 0
    if operazione == "+":
        risultato = primoNumero + secondoNumero
    elif operazione == "-":
        risultato = primoNumero - secondoNumero
    elif operazione == "*":
        risultato = primoNumero * secondoNumero
    elif operazione == "/":
        if secondoNumero != 0:
            risultato = primoNumero / secondoNumero
        else:
            risultato = "Impossibile"
    elif operazione == "%":
        risultato = primoNumero % secondoNumero
    
    s.sendto(str(risultato).encode(), addr) #Invia a tutti i client
