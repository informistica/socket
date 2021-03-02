import socket
from threading import Thread

HOST = '127.0.0.1'
PORT = 65432

operazioni = {
    "somma": lambda a, b: a + b,
    "sottrazione": lambda a, b: a - b,
    "moltiplicazione": lambda a, b: a * b,
    "divisione": lambda a, b: a / b,
}


def esegui(comando):
    parti = comando.split(";")
    if len(parti) != 3:
        err = "comando non valido"
        return ("error", err)

    op_code, a, b = parti

    op = operazioni.get(op_code)
    a_num = try_float(a)
    b_num = try_float(b)

    if not op:
        err = f'"{op_code}" operazione non riconosciuta'
        return ("error", err)

    if not a_num:
        err = f'"{a}" non è un numero valido'
        return ("error", err)

    if not b_num:
        err = f'"{b}" non è un numero valido'
        return ("error", err)

    ris = f'Risposta: il risultato dell\'opereazione "{op_code} tra {a_num} e {b_num} è {op(a_num, b_num)}'
    return ("ok", ris)


def try_float(n):
    try:
        return float(n)
    except ValueError:
        return None


def avvia_server(indirizzo, porta):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Optionale: permette di riavviare subito il codice,
    # altrimenti bisognerebbe aspettare 2-4 minuti prima di poter riutilizzare(bindare) la stessa porta
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind del socket alla porta
    server_socket.bind((indirizzo, porta))

    # mette il socket in ascolto, con un backlog di 5 connessioni
    server_socket.listen(5)

    return server_socket


def ricevi_comando(sock_listen):
    dati = sock_listen.recv(2048)
    if not dati:
        return ("exit", None)

    comando = dati.decode()

    if comando == 'exit':
        return ("exit", None)

    return ("command", comando)


def gestisci_client(sock):
    while True:
        action, cmd = ricevi_comando(sock)
        print("ricevuto comando")

        if action == "exit":
            print("ricevuto 'exit'")
            break

        status, res = esegui(cmd)

        # invia risposta
        if status == "error":
            print("il comando ha prodotto un errore")
            ris = "ERRORE: " + res
        else:
            print("il comando è andato a buon fine")
            ris = res

        ris = ris.encode()
        sock.send(ris)

    print('chiudo connessione')
    sock.close()


def main():
    server_socket = avvia_server(HOST, PORT)
    print(f"[{HOST}] In ascolto su {PORT}")

    while True:
        sock, address = server_socket.accept()

        try:
            Thread(target=gestisci_client, args=(sock,)).start()
        except:
            sock.close()


if __name__ == '__main__':
    main()