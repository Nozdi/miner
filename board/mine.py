from settings import RED, YELLOW, GREEN


class Scheme(object):
    visual_generic = "{}|{}|{}\n{}|{}|{}\n{}|{}|{}"

    def __init__(self, scheme, mine_class):
        if not (0 < scheme < 512):
            raise ValueError("Scheme must be between 1 and 511")
        self.scheme = scheme
        self.mine_class = mine_class

    @property
    def bin_scheme(self):
        return '{0:09b}'.format(self.scheme)

    def get_relative_pos(self):
        array = [self.bin_scheme[i:i+3] for i in range(0, len(self.bin_scheme), 3)]

        pos = []
        for y in range(3):
            for x in range(3):
                if array[x][y] == '1':
                    pos.append((x,y))
        return sorted(pos)

    def get_absolute_pos(self, pos_x, pos_y):
        pos = []
        for x, y in self.get_relative_pos():
            pos.append((pos_x + x, pos_y + y))

        return pos

    # FABRYKA xD
    def fetch_mines(self, x, y):
        return [self.mine_class(*elem) for elem in self.get_absolute_pos(x, y)]

    def visualise(self):
        return self.visual_generic.format(
            *['x' if elem == '1' else '_' for elem in self.bin_scheme]
        )


class BaseMine(object):

    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def __repr__(self):
        return '{}_{}:{}'.format(
            self.__class__.__name__, self.pos_x, self.pos_y)


class RedMine(BaseMine):

    def __init__(self, pos_x, pos_y):
        super(RedMine, self).__init__(pos_x, pos_y)
        self.color = RED
        self.demage = 50


class YellowMine(BaseMine):

    def __init__(self, pos_x, pos_y):
        super(YellowMine, self).__init__(pos_x, pos_y)
        self.color = YELLOW
        self.demage = 20


class GreenMine(BaseMine):

    def __init__(self, pos_x, pos_y):
        super(GreenMine, self).__init__(pos_x, pos_y)
        self.color = GREEN
        self.demage = 10


if __name__ == '__main__':
    example_scheme = Scheme(57, YellowMine)
    print example_scheme.get_absolute_pos(12, 12)
    print example_scheme.visualise()
    print example_scheme.fetch_mines(12, 12)
