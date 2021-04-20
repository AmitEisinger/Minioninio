import json


def get_enum_of_val(val, _enum):
    for e in _enum:
        if e.value == val:
            return e

def zero_padding(num, len):
    return str(num).zfill(len)

def remove_zero_padding(s):
    non_zero_index = 0
    for c in s:
        if c == '0':
            non_zero_index += 1
        else:
            break
    return int(s[non_zero_index:]) if non_zero_index < len(s) else 0

def bytes_to_string(b):
    return b.decode()

def string_to_bytes(s):
    return s.encode()

def json_to_dict(j):
    return json.loads(j)

def dict_to_json(d):
    return json.dumps(d)
