import socket

CLIENT_ID = 1

SERVERS = [
    ("10.0.3.1", 5001),
    ("10.0.3.2", 5002),
    ("10.0.3.3", 5003),
]

message = f"Hola desde el cliente {CLIENT_ID}"
data = message.encode("utf-8")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for server in SERVERS:
    sock.sendto(data, server)
    print(f"Mensaje enviado a {server[0]}:{server[1]}")

sock.close()
