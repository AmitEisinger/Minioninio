import json
import os


def read_json_as_dict_from_file(file):
    with open(file, 'r') as json_file:
        data = json_file.read()
    return json.loads(data)

def get_full_path(relative_path):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, relative_path)
    return filename
