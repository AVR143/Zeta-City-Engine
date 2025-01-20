import xml.etree.ElementTree as ET
import xml.dom.minidom

class CellMapper:
    '''Records the coordinates of buildings on a field consisting of large blocks of 300 by 300.
        Saves the result to a file'''
    def __init__(self, data, template):
        self.data = data
        self.template = template
        self.tree = ET.parse('result/intermediate_file.pzw')
        self.root = self.tree.getroot()

    def retransform_coordinates(self, coord):
        main_cell_x = coord[0] // 10
        main_cell_y = coord[1] // 10
        segment_x = coord[0] % 10
        segment_y = coord[1] % 10
        return (main_cell_x, main_cell_y), (segment_x, segment_y)

    def find_main_cell(self, main_coord):
        for cell in self.root.findall('.//cell'):
            if cell.attrib['x'] == str(main_coord[0]) and cell.attrib['y'] == str(main_coord[1]):
                return cell
        return None

    def map_cells(self):
        for coord, path in self.data.items():
            main_coord, segment_coord = self.retransform_coordinates(coord)
            main_cell = self.find_main_cell(main_coord)
            if main_cell is not None:
                lot_elem = ET.SubElement(main_cell, 'lot', {
                    'x': str(segment_coord[0] * 30),
                    'y': str(segment_coord[1] * 30),
                    'width': '30',
                    'height': '30',
                    'map': self.template + path['Name']
                })

    def write_to_file(self, file_name):
        xmlstr = ET.tostring(self.root, encoding='utf-8')
        reparsed = xml.dom.minidom.parseString(xmlstr)
        pretty_xml_as_string = reparsed.toprettyxml(indent=" ")

        cleaned_xml = '\n'.join([line for line in pretty_xml_as_string.split('\n') if line.strip()])

        with open(file_name, 'wb') as f:
            f.write(cleaned_xml.encode('utf-8'))



