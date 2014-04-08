from settings import RED, YELLOW, GREEN


class BaseMine(object):

     def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y


class RedMine(BaseMine):

    def __init__(self, pos_x, pos_y):
        super(RedMine, self).__init__(pos_x, pos_y)
        self.color = RED


class YellowMine(BaseMine):

    def __init__(self, pos_x, pos_y):
        super(RedMine, self).__init__(pos_x, pos_y)
        self.color = YELLOW


class GreenMine(BaseMine):

    def __init__(self, pos_x, pos_y):
        super(RedMine, self).__init__(pos_x, pos_y)
        self.color = GREEN


class BaseScheme(object):
    visual_generic = "{}|{}|{}\n{}|{}|{}\n{}|{}|{}"

    def __init__(self, scheme):
        if not (0 < scheme < 512):
            raise ValueError("scheme must be between 1 and 511")
        self.scheme = scheme

    @property
    def bin_scheme(self):
        var = bin(self.scheme)[2:]
        return ('0'*9)[8-len(var):]+var

    def visualise(self):
        print self.visual_generic.format(
            *['x' if elem == '1' else '_' for elem in self.bin_scheme]
        )
