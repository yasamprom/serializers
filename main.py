from xml_marshaller import xml_marshaller
import jsonpickle
import yaml
import msgpack
from fastapi import FastAPI, HTTPException
import time
import sys


class Data:
    def __init__(self):
        self.float = 123.001
        self.integer = 123
        self.string = "123" * 100
        self.lst = [123] * 100
        self.myset = {123, 123123, 123123123}
        self.dct = {"123": 123, "123123": [123] * 50}
        self.tup = (123, 123, 123)

def to_json(cls):
    return jsonpickle.encode(cls)

def from_json(cls):
    return jsonpickle.decode(cls)

def to_xml(cls):
    return xml_marshaller.dumps(cls)

def from_xml(xml_str):
    return xml_marshaller.loads(xml_str)

def to_yaml(cls):
    return yaml.dump(cls)

def from_yaml(yaml_str):
    return yaml.load(yaml_str, Loader=yaml.Loader)

def encode(obj):
    if isinstance(obj, Data):
        return [obj.float, obj.integer, obj.string, obj.lst,
                obj.myset, obj.dct, obj.tup]

def to_msg(cls):
    return msgpack.packb(cls, default=encode)

def from_msg(msg_str):
    return msgpack.unpackb(msg_str, strict_map_key=False)


dt = Data()

app = FastAPI()

@app.get("/test/{type}")
async def test(type: int):
    cycles = 100
    ser_func, deser_func = None, None
    if type == 1:  # json
        ser_func = to_json
        deser_func = from_json
    if type == 2:  # xml
        ser_func = to_xml
        deser_func = from_xml
    if type == 3:  # yaml
        ser_func = to_yaml
        deser_func = from_yaml
    if type == 4:  # msgpack
        ser_func = to_msg
        deser_func = from_msg

    if ser_func is None or deser_func is None:
        return {"error": "no such type of serialization"}

    enc = ''
    start_time = time.time()
    for i in range(cycles):
        enc = ser_func(dt)
    ser_time = (time.time() - start_time) / cycles

    start_time = time.time()
    for i in range(cycles):
        deser_func(enc)
    deser_time = (time.time() - start_time) / cycles

    return {
        "serialization": "%.6f" % ser_time,
        "deserialization": "%.6f" % deser_time,
        "size": sys.getsizeof(dt)
    }
