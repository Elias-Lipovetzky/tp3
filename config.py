import os
from dotenv import load_dotenv

load_dotenv()

SERVER_ID = os.getenv("SERVER_ID", "0")
LISTEN_PORT = int(os.getenv("LISTEN_PORT", "5001"))

print(f"servidor {SERVER_ID}, puerto {LISTEN_PORT}")
