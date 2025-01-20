import RoadAlgorithm
import random

from NewField import NewField # To create a field from large blocks
from TmxCityWrite import TmxWrite # To record a field from large blocks

from CityTilePlace import CityTilePlace # For placing roads (for now)
from TbxCityWrite import CellMapper # To record roads on the field

def city_generate():
    '''Generates a city'''
    field_bsize_coord = random.randint(7, 8)
    max_rect_size_coord = random.randint(5, 7)
    min_rect_size_coord = (3, 3)
    max_rects_count = random.randint(15, 20)

    write = TmxWrite(NewField(field_bsize_coord).field)
    write.write('result/intermediate_file.pzw') # intermediate file

    # Link to folder with roads
    template = 'paste/the/absolute/path/to/the/roads/folder'

    road_gen = CityTilePlace(RoadAlgorithm.main((field_bsize_coord, field_bsize_coord),
                                               (max_rect_size_coord, max_rect_size_coord),
                                               min_rect_size_coord,
                                               max_rects_count))
    road_gen.be_place()

    mapper = CellMapper(road_gen.city_field, template)
    mapper.map_cells()
    mapper.write_to_file('result/city.pzw')

city_generate()



