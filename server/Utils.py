import json


def get_enum_of_val(val, _enum):
    for e in _enum:
        if e.value == val:
            return e

def zero_padding(num, len):
    return str(num).zfill(len)

def bytes_to_string(b):
    return b.decode()

def string_to_bytes(s):
    return s.encode()

def bytes_json_to_dict(b):
    s = bytes_to_string(b)
    return json.loads(s)

def dict_to_json(d):
    return json.dumps(d)
