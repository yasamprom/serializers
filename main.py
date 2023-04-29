from xml_marshaller import xml_marshaller
import jsonpickle
import yaml
import msgpack
from fastapi import FastAPI, HTTPException
import fastavro
import time
import sys
from pympler import asizeof
import logging


class Data:
    def __init__(self):
        self.float = 123.001
        self.integer = 123
        self.string = "123" * 100
        self.lst = [123] * 100
        self.myset = {123, 123123, 123123123}
        self.dct = {"123": 123, "123123": [123] * 50}
        self.tup = (123, 123, 123)
data_dict =  {
        "float": 123.001,
        "integer": 123,
        "string":"123" * 100,
        "lst": [123] * 100,
        "myset": {123, 123123, 123123123},
        "dct": {"123": "123"}
}

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

def to_avro(cls):
    data_schema = {
        "type": "record",
        "name": "dict",
        "fields": [
            {"name": "float", "type": "float"},
            {"name": "integer", "type": "int"},
            {"name": "string", "type": "string"},
            {"name": "lst", "type": {"type": "array", "items": "int"}},
            {"name": "dct", "type": {"type": "map", "values": "string"}},
        ]
    }
    with open("data.avro", "wb") as avro_file:
        fastavro.schemaless_writer(avro_file, data_schema, data_dict)
    return None

def from_avro(msg):
    return
    with open('data.avro', 'rb') as fo:
        avro_reader = fastavro.reader(fo)
        for _ in avro_reader:
            pass


dt = Data()

app = FastAPI()

@app.get("/test/{type}")
async def test(type: str):
    logging.info("main server got query: %s", type)
    cycles = 100
    ser_func, deser_func = None, None
    if type == "json":
        ser_func = to_json
        deser_func = from_json
    if type == "xml":
        ser_func = to_xml
        deser_func = from_xml
    if type == "yaml":
        ser_func = to_yaml
        deser_func = from_yaml
    if type == "msgpack":
        ser_func = to_msg
        deser_func = from_msg
    if type == "avro":
        ser_func = to_avro
        deser_func = from_avro

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
        "size": asizeof.asizeof(dt)
    }
