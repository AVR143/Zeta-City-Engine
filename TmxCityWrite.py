import xml.etree.ElementTree as ET
import xml.dom.minidom

class TmxWrite:
    '''Records the coordinates of an empty field consisting of large 300 by 300 blocks.
    Saves the result to an intermediate file'''
    def __init__(self, data):
        self.tree = ET.parse('example.xml') # this file always remains unchanged; we build other files on its basis
        self.root = self.tree.getroot()
        self.insertion_point = self.root.find('.//objectgroup[@name="RoomTone"]')
        self.data = data

    def write(self, name):
        if self.insertion_point is not None:
            index = list(self.root).index(self.insertion_point) + 1
        else:
            index = len(self.root)

        for coords in sorted(self.data.keys()):
            x, y = coords
            cell_elem = ET.Element('cell', {'x': str(x), 'y': str(y), 'map': '0_0.tmx'})

            self.root.insert(index, cell_elem)
            index += 1

        xmlstr = ET.tostring(self.root, encoding='utf-8')
        reparsed = xml.dom.minidom.parseString(xmlstr)
        pretty_xml_as_string = reparsed.toprettyxml(indent=" ")

        cleaned_xml = '\n'.join([line for line in pretty_xml_as_string.split('\n') if line.strip()])

        with open(name, 'wb') as f:
            f.write(cleaned_xml.encode('utf-8'))