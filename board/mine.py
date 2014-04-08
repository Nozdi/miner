from settings import RED, YELLOW, GREEN


class BaseMine(object):

    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y


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


class BaseScheme(object):
    visual_generic = "{}|{}|{}\n{}|{}|{}\n{}|{}|{}"

    def __init__(self, scheme):
        if not (0 < scheme < 512):
            raise ValueError("Scheme must be between 1 and 511")
        self.scheme = scheme

    @property
    def bin_scheme(self):
        return '{0:09b}'.format(self.scheme)

    def fetch_rel_positions(self):
        array = [self.bin_scheme[i:i+3] for i in range(0, len(self.bin_scheme), 3)]

        pos = []
        for y in range(3):
            for x in range(3):
                if array[x][y] == '1':
                    pos.append((x,y))
        return sorted(pos)

    def visualise(self):
        return self.visual_generic.format(
            *['x' if elem == '1' else '_' for elem in self.bin_scheme]
        )


class Scheme(BaseScheme):

    def __init__(self, mine_class, scheme):
        super(Scheme, self).__init__(scheme)
        self.mines = [mine_class(*elem) for elem in self.fetch_rel_positions()]


if __name__ == '__main__':
    example_scheme = Scheme(GreenMine, 57)
    print example_scheme.fetch_rel_positions()
    print example_scheme.visualise()
