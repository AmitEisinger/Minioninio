# NOTE: This file has to be in the same path as main.py
import unittest
from Definitions.Grid import Grid
from Definitions.Directions import *


class TestGrid(unittest.TestCase):
    """
    when grid is:
        GRID = [
            [CellTypes.DISPENSER, CellTypes.EMPTY,    CellTypes.OBSTACLE],
            [CellTypes.EMPTY,     CellTypes.EMPTY,    CellTypes.EMPTY],
            [CellTypes.EMPTY,     CellTypes.OBSTACLE, CellTypes.EMPTY]
        ]
    """
    SRC_ROW, SRC_COL = 0,0
    DST_ROW1, DST_COL1 = 1,2
    DST_ROW2, DST_COL2 = 0,1
    DST_ROW3, DST_COL3 = 2,0
    DST_ROW4, DST_COL4 = 0,2

    def test1(self):
        route = Grid.calculate_route(TestGrid.SRC_ROW, TestGrid.SRC_COL, TestGrid.DST_ROW1, TestGrid.DST_COL1)
        print("route 1: ", route)
        self.assertEquals(len(route), 4)
        print("dirs 1: ", self.__route_to_dirs(route))

    def test2(self):
        route = Grid.calculate_route(TestGrid.SRC_ROW, TestGrid.SRC_COL, TestGrid.DST_ROW2, TestGrid.DST_COL2)
        print("route 2: ", route)
        self.assertEquals(len(route), 2)
        print("dirs 2: ", self.__route_to_dirs(route))

    def test3(self):
        route = Grid.calculate_route(TestGrid.SRC_ROW, TestGrid.SRC_COL, TestGrid.DST_ROW3, TestGrid.DST_COL3)
        print("route 3: ", route)
        self.assertEquals(len(route), 3)
        print("dirs 3: ", self.__route_to_dirs(route))
    
    def test4(self):
        route = Grid.calculate_route(TestGrid.SRC_ROW, TestGrid.SRC_COL, TestGrid.DST_ROW4, TestGrid.DST_COL4)
        print("route 4: ", route)
        self.assertEquals(len(route), 0)
        print("dirs 4: ", self.__route_to_dirs(route))
    

    def __route_to_dirs(self, route):
        face_dir = Directions.UP
        dirs = []
        for i in range(len(route)-1):
            step, face_dir = step_to_direction(route[i], route[i+1], face_dir)
            dirs.append(step)
        return dirs


if __name__ == '__main__':
    unittest.main()
