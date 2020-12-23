from enum import Enum
import Utils


class Directions(Enum):
    UP = 'U'
    DOWN = 'D'
    RIGHT = 'R'
    LEFT = 'L'


def get_direction(dir_val):
    return Utils.get_enum_of_val(dir_val, Directions)
