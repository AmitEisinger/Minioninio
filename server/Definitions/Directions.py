from enum import Enum
import Utils
from Definitions.Grid import Grid


class Directions(Enum):
    UP = 'U'
    FORWARD = UP        # TODO: check if its also what Amit thought
    DOWN = 'D'
    BACKWARD = DOWN     # TODO: check if its also what Amit thought
    RIGHT = 'R'
    LEFT = 'L'


def get_direction(dir_val):
    return Utils.get_enum_of_val(dir_val, Directions)


"""
returns: step - the direction in which the robot should move (considering it's current face direction)
         new_face_dir - robot's face direction after this step
"""
def step_to_direction(src, dst, face_dir):
    src_row, src_col = src
    dst_row, dst_col = dst
    # should go down
    if src_row - dst_row == -1 and src_col == dst_col:
        if face_dir == Directions.DOWN:
            step = Directions.FORWARD
        elif face_dir == Directions.UP:
            step = Directions.BACKWARD
        elif face_dir == Directions.LEFT:
            step = Directions.LEFT
        elif face_dir == Directions.RIGHT:
            step = Directions.RIGHT
        new_face_dir = Directions.DOWN
    # sould go up
    elif src_row - dst_row == 1 and src_col == dst_col:
        if face_dir == Directions.DOWN:
            step = Directions.BACKWARD
        elif face_dir == Directions.UP:
            step = Directions.FORWARD
        elif face_dir == Directions.LEFT:
            step = Directions.RIGHT
        elif face_dir == Directions.RIGHT:
            step = Directions.LEFT
        new_face_dir = Directions.UP
    # sould go right
    elif src_row == dst_row and src_col - dst_col == -1:
        if face_dir == Directions.DOWN:
            step = Directions.LEFT
        elif face_dir == Directions.UP:
            step = Directions.RIGHT
        elif face_dir == Directions.LEFT:
            step = Directions.BACKWARD
        elif face_dir == Directions.RIGHT:
            step = Directions.FORWARD
        new_face_dir = Directions.RIGHT
    # sould go left
    elif src_row == dst_row and src_col - dst_col == 1:
        if face_dir == Directions.DOWN:
            step = Directions.RIGHT
        elif face_dir == Directions.UP:
            step = Directions.LEFT
        elif face_dir == Directions.LEFT:
            step = Directions.FORWARD
        elif face_dir == Directions.RIGHT:
            step = Directions.BACKWARD
        new_face_dir = Directions.LEFT
    return step, new_face_dir


"""
returns: rotate_dir - the direction in which the robot should rotate in order to drop the item right to the robot
         new_face_dir - robot's face direction after rotation
"""
def get_rotation_direction(location, face_dir):
    row, col = location
    # should drop up while facing left
    if row == 0:
        if face_dir == Directions.UP:
            rotate_dir = Directions.LEFT
        elif face_dir == Directions.DOWN:
            rotate_dir = Directions.RIGHT
        elif face_dir == Directions.LEFT:
            rotate_dir = Directions.FORWARD
        elif face_dir == Directions.RIGHT:
            rotate_dir = Directions.BACKWARD
        new_face_dir = Directions.LEFT
    # should drop down while facing right
    elif row == len(Grid.GRID) - 1:
        if face_dir == Directions.UP:
            rotate_dir = Directions.RIGHT
        elif face_dir == Directions.DOWN:
            rotate_dir = Directions.LEFT
        elif face_dir == Directions.LEFT:
            rotate_dir = Directions.BACKWARD
        elif face_dir == Directions.RIGHT:
            rotate_dir = Directions.FORWARD
        new_face_dir = Directions.RIGHT
    # should drop left while facing down
    elif col == 0:
        if face_dir == Directions.UP:
            rotate_dir = Directions.BACKWARD
        elif face_dir == Directions.DOWN:
            rotate_dir = Directions.FORWARD
        elif face_dir == Directions.LEFT:
            rotate_dir = Directions.LEFT
        elif face_dir == Directions.RIGHT:
            rotate_dir = Directions.RIGHT
        new_face_dir = Directions.DOWN
    # should drop right while facing up
    elif col == len(Grid.GRID[0]) - 1:
        if face_dir == Directions.UP:
            rotate_dir = Directions.FORWARD
        elif face_dir == Directions.DOWN:
            rotate_dir = Directions.BACKWARD
        elif face_dir == Directions.LEFT:
            rotate_dir = Directions.RIGHT
        elif face_dir == Directions.RIGHT:
            rotate_dir = Directions.LEFT
        new_face_dir = Directions.UP
    return rotate_dir, new_face_dir
