import socket
import sys

if len(sys.argv) != 3:
    print("Uso: python tcp_client.py HOST PUERTO")
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])

message = "Hola desde el cliente TCP"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((host, port))

sock.sendall(message.encode("utf-8"))

sock.close()
