import socket

HOST = '127.0.0.1'
PORT = 65432

PROTOCOL = ['SYN', 'SYN + ACK', 'ACK + Data', 'ACK for Data']

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Optionale: permette di riavviare subito il codice,
# altrimenti bisognerebbe aspettare 2-4 minuti prima di poter riutilizzare(bindare) la stessa porta
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind del socket alla porta
server_socket.bind((HOST, PORT))

# mette il socket in ascolto, con un backlog di 5 connessioni
server_socket.listen(5)
print(f"[{HOST}] In ascolto su {PORT}")


def send(socket, seq):
    print(f"--> {seq} {PROTOCOL[seq]}")
    data = seq.to_bytes(1, 'big')
    socket.send(data)


def recv(socket):
    data = socket.recv(2048)

    if not data:
        return None

    seq = int.from_bytes(data, 'big')
    print(f"<-- {seq} {PROTOCOL[seq]}")
    return seq


if __name__ == '__main__':
    while True:
        socket, address = server_socket.accept()
        print("Connessione ricevuta da " + str(address))
        print("Aspetto di ricevere i dati ")

        while True:
            seq = recv(socket)

            if seq == None:
                print("client si è disconnesso")
                break

            if seq >= len(PROTOCOL) - 1:
                print("sequenza terminata")
                break

            send(socket, seq + 1)
        
        socket.close()