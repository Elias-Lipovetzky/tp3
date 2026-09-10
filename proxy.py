import argparse
import socket
import threading


def parse_backend(value):
    host, port = value.rsplit(":", 1)
    return host, int(port)


parser = argparse.ArgumentParser()

parser.add_argument("--escucha", type=int, required=True)
parser.add_argument("--backend", action="append", required=True)
parser.add_argument("--balancer", action="store_true")

args = parser.parse_args()

backends = [parse_backend(value) for value in args.backend]

if not args.balancer and len(backends) != 1:
    parser.error("Sin --balancer debe haber un solo backend")


current_backend = 0
backend_lock = threading.Lock()


def choose_backend():
    global current_backend

    if not args.balancer:
        return backends[0]

    with backend_lock:
        backend = backends[current_backend]
        current_backend = (current_backend + 1) % len(backends)
        return backend


def copy_bytes(source, destination, direction):
    total = 0

    try:
        while True:
            data = source.recv(4096)

            if not data:
                break

            destination.sendall(data)
            total += len(data)

            print(f"{direction}: {len(data)} bytes (total: {total})")

    except OSError as error:
        print(f"{direction}: {error}")

    finally:
        try:
            destination.shutdown(socket.SHUT_WR)
        except OSError:
            pass


def handle_client(client, client_address):
    backend_address = choose_backend()

    print(
        f"Cliente {client_address[0]}:{client_address[1]} "
        f"-> backend {backend_address[0]}:{backend_address[1]}"
    )

    try:
        backend = socket.create_connection(backend_address)

    except OSError as error:
        print(f"No se pudo conectar al backend: {error}")
        client.close()
        return

    client_to_backend = threading.Thread(
        target=copy_bytes,
        args=(client, backend, "cliente -> servidor"),
    )

    backend_to_client = threading.Thread(
        target=copy_bytes,
        args=(backend, client, "servidor -> cliente"),
    )

    client_to_backend.start()
    backend_to_client.start()

    client_to_backend.join()
    backend_to_client.join()

    client.close()
    backend.close()


listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

listener.bind(("0.0.0.0", args.escucha))
listener.listen()

print(f"Proxy escuchando en 0.0.0.0:{args.escucha}")
print("Backends:", backends)


while True:
    client, address = listener.accept()

    threading.Thread(
        target=handle_client,
        args=(client, address),
        daemon=True,
    ).start()
