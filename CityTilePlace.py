import json
import random

class CityTileData:
    '''Loads road data'''
    with open('roads/30_30.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

class CityTilePlace(CityTileData): #(26, 0) (26, 79)
    def __init__(self, rectangles):
        self.rect = rectangles
        self.city_field =  {}

    def add_tile(self, x, y, city_cell):
        '''Adds a tile to the field'''
        if (x, y) not in self.city_field:
            self.city_field[(x, y)] = city_cell

    def check_coord(self, x, y):
        '''Checks which coordinates from the list of coordinates are near the specified coordinate'''
        coord_neighbours = {
            'North': (x, y - 1),
            'East': (x + 1, y),
            'South': (x, y + 1),
            'West': (x - 1, y)
        }
        coord_direction = {}
        for name, coord in coord_neighbours.items():
            if coord in self.rect:
                coord_direction[name] = coord
        return coord_direction

    def check_direction(self, coord, tile):
        '''Checks the direction of roads at neighboring coordinates.
        Ensures correct connection of roads'''
        coord = self.check_coord(*coord)
        # Проверка соответствия направлениям
        for direction, coord_value in coord.items():
            if tile.get(direction) != 'road':
                return False
        # Проверка оставшихся направлений в tile
        for direction, tile_value in tile.items():
            if direction not in coord and direction != 'Name' and tile_value != 'nones' and tile_value != 'house':
                return False
        return True

    def be_place(self):
        '''Responsible for selecting successful tiles on the field'''
        for coord in self.rect:
            while True:
                tile = random.choice(list(self.data.values()))
                if self.check_direction(coord, tile):
                    self.add_tile(*coord, tile)
                    break

