__author__ = 'richy734'


class Map(object):
    def __init__(self, walls, length, breadth, itemLocale, digitLocale):
        assert isinstance(walls, list)
        self.walls = walls
        self.length = length
        self.breadth = breadth
        self.itemLocale = itemLocale
        self.digitLocale = digitLocale
