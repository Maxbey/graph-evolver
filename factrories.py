class VertexFactory(object):
    def __init__(self):
        self.index = 0

    def create(self):
        to_return = self.index + 1
        self.index += 1

        return to_return