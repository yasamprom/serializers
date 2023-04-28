import time, os
import socket
import random
import logging
logging.basicConfig(level=logging.INFO)


HOST = os.getenv("CLIENT_HOST")
PORT = os.getenv("CLIENT_PORT")
PROXY_PORT = os.getenv("PROXY_PORT")
SAMPLE_QUERIES = 5

logging.warning("Start client on %s:%s. Proxy port: %s", HOST, PORT, PROXY_PORT)

for pings in range(SAMPLE_QUERIES):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind((HOST, int(PORT)))
    client_socket.settimeout(5.0)
    formats = ["json", "xml", "msgpack", "yaml"]
    chosen_format_index = random.randint(0, len(formats) - 1)
    message = {
        "type": "get_result",
        "format": str(formats[chosen_format_index]),
        "addr": str(HOST),
        "port": str(PORT)
    }
    addr = (HOST, int(PROXY_PORT))
    logging.info("client -> proxy %s.           Sent to %s", message, addr)
    client_socket.sendto(bytes(str(message), encoding="utf-8"), addr)
    data = client_socket.recv(1024)
    logging.info("proxy -> client: %s", data)