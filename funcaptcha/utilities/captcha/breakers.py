import datetime
import math
import random
from typing import Union


def get_position(tile_number: int, large: bool) -> tuple[int, int]:
    grid_size = 3
    tile_size = 150 if large else 100
    row = tile_number // grid_size
    col = tile_number % grid_size
    pos_x = random.randint(0, tile_size - 1)
    pos_y = random.randint(0, tile_size - 1)
    x = col * tile_size + pos_x
    y = row * tile_size + pos_y
    return x, y


class GT4Breakers:

    @staticmethod
    def get_cords(tile: int) -> tuple[int, int]:
        coordinates = [
            (0, 0, 200, 200),
            (200, 0, 400, 200),
            (400, 0, 600, 200),
            (600, 0, 800, 200),
            (800, 0, 1000, 200),
            (1000, 0, 1200, 200),
            (1200, 0, 1400, 200),
            (1400, 0, 1600, 200),
            (1600, 0, 1800, 200),
            (1800, 0, 2000, 200),
            (2000, 0, 2200, 200),
            (2200, 0, 2400, 200),
            (2400, 0, 2800, 200),
            (2800, 0, 3000, 200),
            (3000, 0, 3200, 200),
            (3200, 0, 3400, 200),
            (3400, 0, 3800, 200),
            (3800, 0, 4000, 200),
            (4000, 0, 4200, 200),
            (0, 200, 130, 400)
        ]
        tile = coordinates[tile]
        return random.randint(tile[0], tile[2]), random.randint(tile[1], tile[3])

    class Keys:
        @staticmethod
        def alpha(index):
            return [round(100 * random.random()), index, round(100 * random.random())]

        @staticmethod
        def beta(index):
            return {
                'size': 50 - index,
                'id': index,
                'limit': 10 * index,
                'req_timestamp': round(datetime.datetime.now().timestamp() * 1000)
            }

        @staticmethod
        def gamma(index):
            return index

        @staticmethod
        def delta(index):
            return {
                'index': index
            }

        @staticmethod
        def epsilon(index):
            var0 = []
            var1 = round(5 * random.random()) + 1
            var2 = random.randint(0, var1 - 1)
            for hz in range(var1):
                if hz == var2:
                    var0.append(index)
                else:
                    var0.append(round(10 * random.random()))
            var0.append(var2)
            return var0

        @staticmethod
        def zeta(index):
            var0 = round(random.random() * 5) + 1
            result = []
            for idx in range(var0):
                result.append(None)
            result.append(index)
            return result

        @staticmethod
        def ka(index):
            return index

        @staticmethod
        def kb(index):
            return [index]

        @staticmethod
        def kc(index):
            return {
                "guess": index
            }

    class Values:

        @staticmethod
        def alpha(index):
            return float(str(index) + str(1)) - 2

        @staticmethod
        def beta(index):
            return -index

        @staticmethod
        def gamma(index):
            return 3 * (3 - index)

        @staticmethod
        def delta(index):
            return 7 * index

        @staticmethod
        def epsilon(index):
            return 2 * index

        @staticmethod
        def zeta(index):
            try:
                return 100 / index
            except ZeroDivisionError:
                return index

        @staticmethod
        def va(index):
            return index + 3

        @staticmethod
        def vb(index):
            return 0 - index

        @staticmethod
        def vc(index):
            return 10 - index

        @staticmethod
        def vd(index):
            return 3 * index


class GT3Breakers:

    @staticmethod
    def no_breakers(location):
        return {
            "px": '{:.2f}'.format(location[0] / 300),
            "py": '{:.2f}'.format(location[1] / 200),
            "x": location[0],
            "y": location[1]
        }

    @staticmethod
    def method_1(location):
        return {
            "x": location[1],
            "y": location[0]
        }

    @staticmethod
    def method_2(location):
        return {
            "x": location[0],
            "y": (location[1] + location[0]) * location[0]
        }

    @staticmethod
    def method_3(location):
        return {
            "a": location[0],
            "b": location[1]
        }

    @staticmethod
    def method_4(location):
        return [location[0], location[1]]

    @staticmethod
    def method_5(location):
        return [math.sqrt(location[1]), math.sqrt(location[0])]


def fix_answer(game_type: int, api_breakers: Union[str, dict, None], answer: int, large: Union[bool, None] = None):
    if game_type == 4:
        if api_breakers is None:
            return {"index": answer}
        index: int = answer
        for element in api_breakers["value"]:
            index = getattr(GT4Breakers.Values, element)(index)
        index = getattr(GT4Breakers.Keys, api_breakers["key"])(index)
        return index
    else:
        return getattr(GT3Breakers, api_breakers if api_breakers else 'no_breakers')(get_position(answer, large))
