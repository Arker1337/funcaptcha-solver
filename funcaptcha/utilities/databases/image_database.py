import base64
import random
import threading
from hashlib import md5
from io import BytesIO
from itertools import product

import imagehash
import requests
from PIL import Image

from common.databases import global_redis_database_fc_3, global_redis_database_fc_4

coordinates_4 = [
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


def split_gt3_image_grid(image_in: Image) -> list[Image]:
    images = []
    box_size = 150 if image_in.size == (450, 300) else 100
    image_width, image_height = image_in.size
    grid = product(
        range(0, image_height - image_height % box_size, box_size),
        range(0, image_width - image_width % box_size, box_size)
    )
    for box_x, box_y in grid:
        box = (box_y + 2, box_x + 2, box_y + box_size - 2, box_x + box_size - 2)
        images.append(image_in.crop(box))
    return images


class Tile:
    data: Image
    index: int
    perceptual_hash: str
    answered: bool

    def __init__(self, data: Image, index: int):
        self.data = data
        bio = BytesIO()
        data.save(bio, format='png')
        self.image_bytes = bio.getvalue()
        del bio
        self.index = index
        self.answered = False
        self.perceptual_hash = md5(str(imagehash.average_hash(data, 4)).encode()).hexdigest()

    def answer(self):
        self.answered = True


class Grid:
    tiles: list[Tile]
    hand_tile: Tile
    grid_bytes: bytes

    def __init__(self, game_difficulty, grid: bytes, hand: bool = False):
        idx: int = 0
        self.tiles = []
        self.grid_bytes = grid
        bio = BytesIO(grid)
        img = Image.open(bio)
        self.img = img
        del bio
        if hand:
            cr = img.crop((0, 200, 130, 400))
            self.hand_tile = Tile(cr, idx)
            for coord in coordinates_4[0:game_difficulty]:
                x1, y1, x2, y2 = coord
                cropped_img = img.crop((x1, y1, x2, y2))
                self.tiles.append(Tile(cropped_img, idx))
                idx += 1
        else:
            for grid_tile in split_gt3_image_grid(img):
                self.tiles.append(Tile(grid_tile, idx))
                idx += 1


def save_bad_type3(coord, variant, grid: Grid):
    grid.tiles.pop(coord)
    for g in grid.tiles:
        global_redis_database_fc_3.set(g.perceptual_hash + ":" + variant, "bad")


def save_good_type3(coord, variant, grid: Grid):
    global_redis_database_fc_3.set(grid.tiles[coord].perceptual_hash + ":" + variant, "good")


def threaded(fn):
    def wrap(*args):
        threading.Thread(target=fn, args=args).start()
    return wrap


@threaded
def save_bad_type4(coord: int, variant: str, grid: Grid):
    hand_hash = grid.hand_tile.perceptual_hash
    grid.tiles.pop(coord)
    for g in grid.tiles:
        global_redis_database_fc_4.set(hand_hash + ":" + g.perceptual_hash + ":" + variant, "bad")


@threaded
def save_good_type4(coord: int, variant: str, grid: Grid):
    hand_hash = grid.hand_tile.perceptual_hash
    global_redis_database_fc_4.set(hand_hash + ":" + grid.tiles[coord].perceptual_hash + ":" + variant, "good")


def get_grid_hashes_type3(grid: Grid):
    hashes = []
    for tile in grid.tiles:
        hashes.append(tile.perceptual_hash)
    return hashes


def get_image_validity_type3(grid: Grid, variant: str, xd: str = None):
    hashes = get_grid_hashes_type3(grid)
    indexes = [i for i in range(6)]
    for _hash_ in hashes:
        try:
            image_state = global_redis_database_fc_3.get(_hash_ + ":" + variant).decode()
            if image_state == "good":
                print("good")
                return hashes.index(_hash_), True
            elif image_state == "bad":
                print("bad")
                indexes.remove(hashes.index(_hash_))
        except Exception:
            pass
    # _id_ = requests.post("http://127.0.0.1:80/in.php", data={
    #     "method": "image",
    #     "imginstructions": 'ident' if variant == 'square_icon_pair' else 'fingers_sum3',
    #     "body": base64.b64encode(grid.grid_bytes).decode(),
    #     "json": "1"
    # })
    # if "error" in _id_.text.lower():
    #     return random.randint(0, 5), False
    # _id_ = _id_.json()["request"]
    # o = requests.get("http://127.0.0.1/res.php?action=get&id=" + str(_id_) + "&json=1")
    # if "error" in o.text.lower():
    #     return random.randint(0, 5), False
    # solved = int(o.json()["request"]) - 1
    # return solved, False
    return random.choice(indexes) if len(indexes) != 0 else random.randint(0, 5), False


def get_grid_hashes_type4(grid: Grid):
    hashes = []
    for g in grid.tiles:
        hashes.append(g.perceptual_hash)
    return {
        "challenge_hashes": hashes,
        "hand_hash": grid.hand_tile.perceptual_hash
    }


def get_image_validity_type4(grid: Grid, variant: str, difficulty: int, xd: str = None):
    hash_dict = get_grid_hashes_type4(grid)
    challenge_hashes = hash_dict.get('challenge_hashes')
    hand_hash = hash_dict.get('hand_hash')
    indexes = [i for i in range(difficulty + 1)]
    for challenge_hash in challenge_hashes:
        try:
            image_state = global_redis_database_fc_4.get(hand_hash + ":" + challenge_hash + ":" + variant).decode()
            if image_state == "good":
                return challenge_hashes.index(challenge_hash), hand_hash, True
            elif image_state == "bad":
                indexes.remove(challenge_hashes.index(challenge_hash))
        except Exception:
            pass
    # _id_ = requests.post("http://127.0.0.1:80/in.php", data={
    #     "method": "image",
    #     "imginstructions": variant,
    #     "body": base64.b64encode(grid.grid_bytes).decode(),
    #     "json": "1"
    # }, timeout=22999)
    # if "error" in _id_.text.lower():
    #     return random.randint(0, 5), hand_hash, False
    # _id_ = _id_.json()["request"]
    # o = requests.get("http://127.0.0.1/res.php?action=get&id=" + str(_id_) + "&json=1", timeout=22999)
    # solved = int(o.json()["request"]) - 1
    # return solved, hand_hash, False
    return random.choice(indexes) if len(indexes) != 0 else random.choice(indexes), hand_hash, False
