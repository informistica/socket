import socket

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 65432

PROTOCOL = ['SYN', 'SYN ACK', 'ACK with Data', 'ACK for Data']

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((SERVER_ADDRESS, SERVER_PORT))
print("Connesso a " + str((SERVER_ADDRESS, SERVER_PORT)))


def send(seq):
    print(f"<-- {seq} {PROTOCOL[seq]}")
    data = seq.to_bytes(1, 'big')
    socket.send(data)


def recv():
    data = socket.recv(2048)

    if not data:
        return None

    seq = int.from_bytes(data, 'big')
    print(f"--> {seq} {PROTOCOL[seq]}")
    return seq


if __name__ == '__main__':
    # invia pacchetto iniziale: SYN
    send(0)

    while True:
        seq = recv()

        if seq == None:
            print("Server non risponde. Exit")
            break

        if seq >= len(PROTOCOL) - 1:
            print("sequenza terminata")
            break

        send(seq + 1)

    socket.close()