from enum import Enum
import Utils


class Components(Enum):
    ROBOT = 'R'
    SERVER = 'S'
    CLIENT = 'C'


def get_component(comp_val):
    return Utils.get_enum_of_val(comp_val, Components)
