class HexCoord(object):
    def __init__(self, q, r):
        self.q = q
        self.r = r


class CubeCoord(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class CubeHelper(object):
    @classmethod
    def get_distance(cls, a, b):
        return (abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)) / 2


class OddRHelper(object):
    @classmethod
    def convert_hex_to_cube(cls, hex_coord):
        """
        (0, 0) (1, 0)
           (0, 1) (1, 1)
        (0, 2)
        """
        x = hex_coord.q - ((hex_coord.r - (hex_coord.r & 1)) / 2)
        z = hex_coord.r
        y = -x - z
        return CubeCoord(x, y, z)

    @classmethod
    def get_distance(cls, a, b):
        ac = cls.convert_hex_to_cube(a)
        bc = cls.convert_hex_to_cube(b)
        return CubeHelper.get_distance(ac, bc)


print OddRHelper.get_distance(HexCoord(2, 2), HexCoord(1, 1))
print OddRHelper.get_distance(HexCoord(2, 2), HexCoord(1, 0))
print OddRHelper.get_distance(HexCoord(2, 2), HexCoord(0, 1))
print OddRHelper.get_distance(HexCoord(2, 2), HexCoord(3, 1))

print OddRHelper.get_distance(HexCoord(3, 3), HexCoord(2, 1))
print OddRHelper.get_distance(HexCoord(3, 3), HexCoord(2, 2))
print OddRHelper.get_distance(HexCoord(3, 3), HexCoord(4, 1))
print OddRHelper.get_distance(HexCoord(3, 3), HexCoord(5, 2))
