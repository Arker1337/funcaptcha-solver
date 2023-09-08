import math


class BezierCurve(object):
    @staticmethod
    def binomial(n, k):
        return math.factorial(n) / float(math.factorial(k) * math.factorial(n - k))

    @staticmethod
    def bernstein_polynomial_point(x, i, n):
        return BezierCurve.binomial(n, i) * (x ** i) * ((1 - x) ** (n - i))

    @staticmethod
    def bernstein_polynomial(points):
        def bern(t):
            n = len(points) - 1
            x = y = 0
            for i, point in enumerate(points):
                _bern = BezierCurve.bernstein_polynomial_point(t, i, n)
                x += point[0] * _bern
                y += point[1] * _bern
            return x, y

        return bern

    @staticmethod
    def curve_points(n, points):
        curve_points = []
        bernstein_polynomial = BezierCurve.bernstein_polynomial(points)
        for i in range(n):
            t = i / (n - 1)
            curve_points += bernstein_polynomial(t),
        return curve_points
