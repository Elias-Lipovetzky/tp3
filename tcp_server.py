import socket
from config import SERVER_ID, LISTEN_PORT

HOST = "0.0.0.0"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, LISTEN_PORT))
server.listen()

print(f"Servidor TCP {SERVER_ID} escuchando en {LISTEN_PORT}")

while True:
    client, address = server.accept()

    print(f"Conexion recibida desde {address[0]}:{address[1]}")

    data = client.recv(4096)

    if data:
        message = data.decode("utf-8")
        print(f'Servidor {SERVER_ID} recibio: "{message}"')

    client.close()
