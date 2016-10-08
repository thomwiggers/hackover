import logging


logging.basicConfig(level=logging.DEBUG)


def get_val(val, lower, upper):
    rng = upper - lower
    return (val % rng) + lower


class RNG_analiser(object):

    def __init__(self, m, a, b, vals=None):
        self.m = m
        self.a = a
        self.b = b
        self.vals = vals or []
        self.compute_possibilities()

    def add_val(self, val):
        self.vals.append(val)

    def compute_possibilities(self):
        if not hasattr(self, 'possibilities'):
            logging.info('Starting with all possibilities')
            self.possibilities = range(self.m)
        logging.info('Computing possibilities left')
        possibilities = []
        for j, possibility in enumerate(self.possibilities):
            if j % 100000 == 0:
                logging.debug("tried %d possibilities", j)
            for i, val in enumerate(self.vals):
                if get_val(self.step(possibility, i), 1, 101) != val:
                    break
                if i == (len(self.vals)-1):
                    logging.debug('%s is a possibility', possibility)
                    possibilities.append(possibility)
        self.possibilities = possibilities

    def step(self, val, n=1):
        for __ in range(n):
            val = (self.a * val + self.b) % self.m
        return val

    def get_sequence_for(self, candidate):
        print([get_val(self.step(candidate, i), 1, 101) for i in range(10)])
