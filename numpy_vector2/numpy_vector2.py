from numbers import Number

import numpy as np
from pygame.math import Vector2 as vec

OPERATIONS = {
    "add": np.add,
    "mul": np.multiply,
    "sub": np.subtract,
}


class Vector2:

    def __init__(self, x=0, y=0):
        assert(isinstance(x, Number))
        assert(isinstance(y, Number))

        self.data = np.array([x, y], dtype=np.longfloat)

    @property
    def pos(self):
        return self.data

    @pos.getter
    def pos(self):
        return self.data

    @property
    def x(self):
        """Property x is first element of vector.

        >>> Vector2(10, 20).x
        10.0
        """
        return self.data[0]

    @x.setter
    def x(self, value):
        self.data[0] = value

    @x.getter
    def x(self):
        return self.data[0]

    @property
    def y(self):
        """Property y is last element of vector.

        >>> Vector2(10, 20).y
        20.0
        """
        return self.data[1]

    @y.setter
    def y(self, value):
        self.data[1] = value

    @y.getter
    def y(self):
        return self.data[1]

    def __str__(self):
        return '[{0}, {1}]'.format(*self.data)

    def __repr__(self):
        return '<Vector2({0}, {1})>'.format(*self.data)

    def __mul__(self, value):
        return self._apply_operation(value, "mul")

    def __rmul__(self, value):
        return self.__mul__(value)

    def __add__(self, value):
        return self._apply_operation(value, "add")

    def __radd__(self, value):
        return self.__add__(value)

    def __sub__(self, value):
        if isinstance(value, type(self)):
            result = np.subtract(self.data, value.data)
        elif isinstance(value, Number):
            result = np.subtract(self.data, value)
        return type(self)(x=result[0], y=result[1])

    def __rsub__(self, value):
        return self._apply_operation(value, "sub")

    def _apply_operation(self, value, operation):

        result = OPERATIONS[operation](value.data if isinstance(value, type(self))
                                       else value,
                                       self.data)
        return type(self)(x=result[0], y=result[1])

    def length(self):
        return np.linalg.norm(self.data)

    def normalize(self):
        return self.data / self.length()

    def normalize_ip(self):
        self.data = self.normalize()

    def scale_to_length(self, value):
        self.data = self.normalize() * value

    def angle_radians(self):
        return np.arctan2(self.data[1], self.data[0])

    def angle_degrees(self):
        return np.degrees(self.angle_radians())

    def as_polar(self):
        return self.length(), self.angle_degrees()

    def angle_radians_to(self, v):
        assert(isinstance(v, type(self)))
        return np.arccos(np.clip(np.dot(self.normalize(), v.normalize()), -1.0, 1.0))

    def angle_to(self, v):
        return np.degrees(self.angle_radians_to(v))


# Test
if __name__ == "__main__":
    a = Vector2(5, 6)
    b = Vector2(2, 4)
    c = a * b
    d = 2 * a
    e = a * 2
    f = a + b
    g = a + 2
    h = 2 + a
    i = a - b
    j = 2 - a
    k = a - 2
    print(c, d, e, f, g, h, i, j, k, sep="\n")

    pya = vec(5, 6)
    pyb = vec(2, 4)

    def p():
        print(a, b)
        print(pya, pyb)

    from matplotlib import pyplot as plt

    print(a.angle_to(b))
    plt.ylim(-1, 1)
    plt.xlim(-1, 1)
    plt.plot([0, a.x], [0, a.y])
    plt.plot([0, b.x], [0, b.y])
    plt.show()
