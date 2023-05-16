import socket
import os
import json
import requests
import logging
logging.basicConfig(level=logging.INFO)

HOST = os.getenv("PROXY_HOST")
PORT = os.getenv("PROXY_PORT")
FORWARD = {
    "json": 8080,
    "yaml": 8088,
    "msgpack": 8089,
    "xml": 8090,
    "avro": 8091,
    "proto": 8092,
    "native": 8093
}
BUFF_SIZE = 1024


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, int(PORT)))
    logging.info("Listen %s:%s", HOST, PORT)
    while True:
        data, addr = s.recvfrom(BUFF_SIZE)
        if not data:
            pass
        query = json.loads(data.decode("utf-8").replace("'", '"'))
        logging.info("proxy <- client: %s", query)
        if query["type"] == "get_result":
            if query["format"] not in FORWARD:
                s.sendto(bytes("Bad data format", encoding="utf-8"), addr)
            else:
                link = "http://" + query["format"] + ":" + str(FORWARD[query["format"]]) + "/test/" + query["format"]

                logging.info("proxy -> main: %s", link)
                resp = requests.get(link)

                logging.info("proxy got response: %s", resp)
                logging.info("redirect to client")

                s.sendto(bytes(resp.text, encoding="utf-8"), addr)