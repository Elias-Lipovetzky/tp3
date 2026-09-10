import socket
from config import SERVER_ID, LISTEN_PORT

HOST = "0.0.0.0"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, LISTEN_PORT))

print(f"Servidor {SERVER_ID} escuchando en UDP puerto {LISTEN_PORT}")

while True:
    data, client_address = sock.recvfrom(4096)

    message = data.decode("utf-8")

    print(
        f'servidor {SERVER_ID} recibió de '
        f'{client_address[0]}:{client_address[1]}: "{message}"'
    )
