class Coordinate:
    def __init__(self, xy, total_size=None):
        x, y = xy
        if type(x) == type(y) == int:
            W, H = total_size
            self._relative_x = x / W
            self._relative_y = y / H
        elif type(x) == type(y) == float:
            self._relative_x = x
            self._relative_y = y
    def relative(self):
        return (self._relative_x, self._relative_y)
    def absolute(self, absolute_size):
        W, H = absolute_size
        return (int(self._relative_x * W), int(self._relative_y * H))
class Oval:
    def __init__(self, center, radius):
        self._CX, self._CY = center
        self._RX, self._RY = radius
    def top_left(self):
        X0 = self._CX - self._RX
        Y0 = self._CY - self._RY
        return ((X0, Y0))
    def bottom_right(self):
        X1 = self._CX + self._RX
        Y1 = self._CY + self._RY
        return ((X1, Y1))
    def all(self):
        X0, Y0 = self.top_left()
        X1, Y1 = self.bottom_right()
        return (X0, Y0, X1, Y1)
