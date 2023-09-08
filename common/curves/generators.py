from random import random

import numpy as np
import pytweening

from common.curves.bezier import BezierCurve
from common.curves.helpers import is_list_of_points, is_numeric


def gen_mouse_movements(from_point, to_point, **kwargs):
    obj = HumanCurve(from_point, to_point, **kwargs)
    return obj.points


"""
the original author of this file is h0nda, used by their hcaptcha solver from 2021
"""


class HumanCurve:
    def __init__(self, from_point, to_point, **kwargs):
        self.from_point = from_point
        self.to_point = to_point
        points = self.generate_curve(**kwargs)
        points = list(dict.fromkeys([
            (int(x), int(y))
            for x, y in points
        ]))
        self.points = []
        for x, y in points:
            self.points.append((x, y))

    def generate_curve(self, **kwargs):
        offset_boundary_x = kwargs.get("offset_boundary_x", 100)
        offset_boundary_y = kwargs.get("offset_boundary_y", 100)
        left_boundary = kwargs.get("left_boundary", min(self.from_point[0], self.to_point[0])) - offset_boundary_x
        right_boundary = kwargs.get("right_boundary", max(self.from_point[0], self.to_point[0])) + offset_boundary_x
        down_boundary = kwargs.get("down_boundary", min(self.from_point[1], self.to_point[1])) - offset_boundary_y
        up_boundary = kwargs.get("up_boundary", max(self.from_point[1], self.to_point[1])) + offset_boundary_y
        knots_count = kwargs.get("knots_count", 2)
        distortion_mean = kwargs.get("distortion_mean", 1)
        distortion_standard_deviation = kwargs.get("distortion_standard_deviation", 1)
        distortion_frequency = kwargs.get("distortion_frequency", 0.5)
        tween = kwargs.get("tweening", pytweening.easeOutQuad)
        target_points = kwargs.get("target_points", 200)

        internal_knots = self.generate_internal_knots(left_boundary, right_boundary,
                                                      down_boundary, up_boundary, knots_count)
        points = self.generate_points(internal_knots)
        points = self.distort_points(points, distortion_mean, distortion_standard_deviation, distortion_frequency)
        points = self.tween_points(points, tween, target_points)
        return points

    @staticmethod
    def generate_internal_knots(left_boundary, right_boundary,
                                down_boundary, up_boundary,
                                knots_count):
        if not (is_numeric(left_boundary) and is_numeric(right_boundary) and
                is_numeric(down_boundary) and is_numeric(up_boundary)):
            raise ValueError("boundaries must be numeric")
        if not isinstance(knots_count, int) or knots_count < 0:
            raise ValueError("knots_count must be non-negative integer")
        if left_boundary > right_boundary:
            raise ValueError("left_boundary must be less than or equal to right_boundary")
        if down_boundary > up_boundary:
            raise ValueError("down_boundary must be less than or equal to up_boundary")

        knots_x = np.random.choice(range(left_boundary, right_boundary), size=knots_count)
        knots_y = np.random.choice(range(down_boundary, up_boundary), size=knots_count)
        knots = list(zip(knots_x, knots_y))
        return knots

    def generate_points(self, knots):
        if not is_list_of_points(knots):
            raise ValueError("knots must be valid list of points")

        mid_pts_cnt = max(
            abs(self.from_point[0] - self.to_point[0]),
            abs(self.from_point[1] - self.to_point[1]),
            2)
        knots = [self.from_point] + knots + [self.to_point]
        return BezierCurve.curve_points(mid_pts_cnt, knots)

    @staticmethod
    def distort_points(points, distortion_mean, distortion_standard_deviation, distortion_frequency):
        if not (is_numeric(distortion_mean) and is_numeric(distortion_standard_deviation) and
                is_numeric(distortion_frequency)):
            raise ValueError("distortions must be numeric")
        if not is_list_of_points(points):
            raise ValueError("points must be valid list of points")
        if not (0 <= distortion_frequency <= 1):
            raise ValueError("distortion_frequency must be in range [0,1]")

        distorted = []
        for i in range(1, len(points) - 1):
            x, y = points[i]
            delta = np.random.normal(distortion_mean, distortion_standard_deviation) if \
                random() < distortion_frequency else 0
            distorted += (x, y + delta),
        distorted = [points[0]] + distorted + [points[-1]]
        return distorted

    @staticmethod
    def tween_points(points, tween, target__points):
        if not is_list_of_points(points):
            raise ValueError("points must be valid list of points")
        if not isinstance(target__points, int) or target__points < 2:
            raise ValueError("target_points must be an integer greater or equal to 2")
        res = []
        for i in range(target__points):
            index = int(tween(float(i) / (target__points - 1)) * (len(points) - 1))
            res += points[index],
        return res
