from enum import Enum
import random
import Definitions.Directions


DISPENSER_ROW, DISPENSER_COL = 0, 0


class CellTypes(Enum):
    EMPTY = 0       # actually contains a barcode
    OBSTACLE = 1
    DISPENSER = 2


class Grid:
    GRID = [
        [CellTypes.DISPENSER, CellTypes.EMPTY,    CellTypes.OBSTACLE],
        [CellTypes.EMPTY,     CellTypes.EMPTY,    CellTypes.EMPTY],
        [CellTypes.EMPTY,     CellTypes.OBSTACLE, CellTypes.EMPTY]
    ]

    # an empty destination is any empty cell on the borders
    def get_empty_dst():
        rows_amount = len(Grid.GRID)
        cols_amount = len(Grid.GRID[0])
        is_const_row = random.choice([True, False])
        row = random.choice([0, rows_amount - 1]) if is_const_row else random.randint(0, rows_amount - 1)
        col = random.randint(0, cols_amount - 1)  if is_const_row else random.choice([0, cols_amount - 1])
        return row, col
    

    def is_dispenser(location):
        row, col = location
        return row == DISPENSER_ROW and col == DISPENSER_COL


    def calculate_route(src_row, src_col, dst_row, dst_col):
        routes = Grid.__get_possible_routes(src_row, src_col, dst_row, dst_col, [(src_row, src_col)], [])
        shortest_route = min(routes, key=lambda route: len(route)) if routes else []
        return shortest_route


    def __get_possible_routes(src_row, src_col, dst_row, dst_col, route, routes):
        if Grid.__out_of_bounds(src_row, src_col) or Grid.GRID[src_row][src_col] == CellTypes.OBSTACLE or (route and (src_row, src_col) in route[:-1]):
            return routes
        if src_row == dst_row and src_col == dst_col:
            routes.append(route)
            return routes
        routes = Grid.__get_possible_routes(src_row - 1, src_col, dst_row, dst_col, route + [(src_row - 1, src_col)], routes)
        routes = Grid.__get_possible_routes(src_row + 1, src_col, dst_row, dst_col, route + [(src_row + 1, src_col)], routes)
        routes = Grid.__get_possible_routes(src_row, src_col - 1, dst_row, dst_col, route + [(src_row, src_col - 1)], routes)
        routes = Grid.__get_possible_routes(src_row, src_col + 1, dst_row, dst_col, route + [(src_row, src_col + 1)], routes)
        return routes


    def __out_of_bounds(row, col):
        return row < 0 or row >= len(Grid.GRID) or col < 0 or col >= len(Grid.GRID[0])
