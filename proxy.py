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
    "xml": 8090
}
BUFF_SIZE = 1024


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, int(PORT)))
    logging.info("Listen %s:%s", HOST, PORT)
    while True:
        data = s.recv(BUFF_SIZE)
        if not data:
            pass
        query = json.loads(data.decode("utf-8").replace("'", '"'))
        logging.info("proxy <- client: %s", query)
        if query["type"] == "get_result":
            body = {"addr": query["addr"]}
            link = "http://" + HOST + ":" + str(FORWARD[query["format"]]) + "/test/" + query["format"]

            logging.info("proxy -> main: %s", link)
            resp = requests.get(link, params=body)

            logging.info("proxy got response: %s", resp)
            logging.info("redirect to client")

            s.sendto(bytes(resp.text, encoding="utf-8"), (query["addr"], int(query["port"])))