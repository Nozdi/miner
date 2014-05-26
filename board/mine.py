from settings import RED, YELLOW, GREEN, WHITE
from random import randint


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
                    pos.append((x, y))
        return sorted(pos)

    def get_absolute_pos(self, pos_x, pos_y):
        pos = []
        for x, y in self.get_relative_pos():
            pos.append((pos_x + x, pos_y + y))

        return pos

    def visualise(self):
        return self.visual_generic.format(
            *['x' if elem == '1' else '_' for elem in self.bin_scheme]
        )

    def place(self, grid):
        grid_len = len(grid)
        position = (randint(0, grid_len-1), randint(0, grid_len-1))
        absolute_pos = self.get_absolute_pos(*position)
        for x, y in absolute_pos:
            # check if no mine is here
            try:
                if grid[x][y] != 0 and x != grid_len-1 and y != grid_len-1:
                    return False
            except IndexError:
                return False

            # check if the same mine is near (3x3 square) - Moore neighbourhood
            for i in range(-1, 2):
                for j in range(-1, 2):
                    try:
                        if grid[x+i][y+j] == 0:
                            continue
                        if grid[x+i][y+j].color == self.mine_class.color:
                            return False
                    except IndexError:
                        pass

        for x, y in absolute_pos:
            grid[x][y] = self.mine_class()
        return True


class BaseField(object):
    color = WHITE
    damage = 0

    def __init__(self):
        self.radiation = {
            RED: [0],
            YELLOW: [0],
            GREEN: [0],
        }
        self.max_radiation = {
            RED: 0,
            YELLOW: 0,
            GREEN: 0,
        }

    def compute_max(self):
        for key in self.max_radiation:
            self.max_radiation[key] = max(self.radiation[key])

    def __repr__(self):
        return '{}_{}:{}'.format(
            self.__class__.__name__, self.pos_x, self.pos_y)


class RedMine(BaseField):
    color = RED
    damage = 50


class YellowMine(BaseField):
    color = YELLOW
    damage = 20


class GreenMine(BaseField):
    color = GREEN
    damage = 10


if __name__ == '__main__':
    example_scheme = Scheme(57, YellowMine)
    print example_scheme.get_absolute_pos(12, 12)
    print example_scheme.visualise()
    print example_scheme.fetch_mines(12, 12)
