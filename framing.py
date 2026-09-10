import socket
import threading


HOST = "10.0.3.1"
PORT = 9000

server_ready = threading.Event()


def recibir_exacto(sock, n):
    data = bytearray()

    while len(data) < n:
        chunk = sock.recv(n - len(data))

        if not chunk:
            raise ConnectionError("La conexion se cerro antes de recibir todos los bytes")

        data.extend(chunk)

    return bytes(data)


def enviar_mensaje(sock, message):
    msg = message.encode("utf-8")
    header = len(msg).to_bytes(4, "big")

    sock.sendall(header + msg)


def recibir_mensaje(sock):
    header = recibir_exacto(sock, 4)
    n = int.from_bytes(header, "big")
    msg = recibir_exacto(sock, n)

    return msg.decode("utf-8")


def servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen()

    print(f"Servidor escuchando en {HOST}:{PORT}")

    server_ready.set()

    client, address = server.accept()

    print(f"Cliente conectado desde {address[0]}:{address[1]}")

    message = recibir_mensaje(client)

    print(f'Mensaje recibido: "{message}"')

    client.close()
    server.close()


def cliente():
    server_ready.wait()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    enviar_mensaje(sock, "Hola con framing correcto")

    sock.close()


thread = threading.Thread(target=servidor)
thread.start()

cliente()

thread.join()
