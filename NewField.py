class NewField:
    def __init__(self, field_size):
        self.field = {}
        self.initialize_field(field_size)

    def initialize_field(self, field_size):
        '''Creates a field of large blocks of the specified size'''
        for x in range(field_size):
            for y in range(field_size):
                self.field[(x, y)] = '0_0.tmx'


