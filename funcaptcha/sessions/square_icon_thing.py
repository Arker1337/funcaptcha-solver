import traceback

import cv2
import numpy as np

# set maximum recursion depth


class Processor:
    def __init__(self, data: bytes) -> None:
        self.processed = None
        self.data = data
        self.img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_UNCHANGED)
        self.marked = []

    @staticmethod
    def rotate_image(mat, angle):
        height, width = mat.shape[:2]  # image shape has 3 dimensions
        image_center = (
            width / 2,
            height / 2,
        )  # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

        rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)

        # rotation calculates the cos and sin, taking absolutes of those.
        abs_cos = abs(rotation_mat[0, 0])
        abs_sin = abs(rotation_mat[0, 1])

        # find the new width and height bounds
        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        # subtract old image center (bringing image back to origo) and adding the new image center coordinates
        rotation_mat[0, 2] += bound_w / 2 - image_center[0]
        rotation_mat[1, 2] += bound_h / 2 - image_center[1]

        # rotate image with the new bounds and translated rotation matrix
        rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
        return rotated_mat

    def process_matching_pixel(self, x: int, y: int) -> list:
        if [x, y] in self.processed:
            return []
        self.processed.append([x, y])

        if x < 0 or y < 0 or x >= self.img.shape[1] or y >= self.img.shape[0]:
            return []
        output = []
        r, g, b = self.img[y, x]
        if r > 180 and g > 180 and b > 180:
            output.append((x, y))
            output += self.process_matching_pixel(x + 1, y)
            output += self.process_matching_pixel(x - 1, y)
            output += self.process_matching_pixel(x, y + 1)
            output += self.process_matching_pixel(x, y - 1)
        return output

    def mark_matched(self, region: tuple) -> None:
        if region in self.marked:
            return
        self.marked.append(region)
        for pixel in region[4]:
            self.img[pixel[1], pixel[0]] = (255, 0, 0)

    def process(self):
        potential_pixels = self.get_potential_pixels()
        self.processed = []
        regions = []
        for pixel in potential_pixels:
            region = self.process_matching_pixel(pixel[0], pixel[1])
            max_x = 0
            max_y = 0
            min_y = 999999
            min_x = 999999

            if 0 < len(region) < 350:
                for pixel in region:
                    if pixel[0] > max_x:
                        max_x = pixel[0]
                    if pixel[1] > max_y:
                        max_y = pixel[1]
                    if pixel[0] < min_x:
                        min_x = pixel[0]
                    if pixel[1] < min_y:
                        min_y = pixel[1]

                width = max_x - min_x
                height = max_y - min_y
                regions.append((min_x, min_y, width, height, region))

                for match in region:
                    self.img[match[1], match[0]] = (0, 0, 255)
        if len(regions) > 120:
            print("wtf this should not happen")
            with open("test.png", "wb") as f:
                _, data = cv2.imencode(".png", self.img)
                f.write(data)
                raise Exception()
        for region in regions:
            for potential in regions:
                if region == potential:
                    continue

                rx = region[0]
                ry = region[1]
                rwidth = region[2]
                rheight = region[3]

                px = potential[0]
                py = potential[1]
                pwidth = potential[2]
                pheight = potential[3]

                # rotate the region[4]
                for rotation in range(-90, 90):
                    # create a blank image with the same size as the region
                    blank = np.zeros((rheight, rwidth, 3), np.uint8)
                    # draw the region on the blank image
                    for pixel in region[4]:
                        try:
                            blank[pixel[1] - ry - 1, pixel[0] - rx - 1] = (
                                255,
                                255,
                                255,
                            )
                        except Exception:
                            pass
                    # rotate the blank image
                    try:
                        blank = self.rotate_image(blank, rotation)
                    except Exception:
                        continue
                    if blank is None:
                        continue

                    bwidth = blank.shape[1]
                    bheight = blank.shape[0]

                    dwidth = abs(bwidth - pwidth)
                    dheight = abs(bheight - pheight)

                    if dwidth < 2 and dheight < 2:
                        if region not in self.marked and potential not in self.marked:
                            self.mark_matched(region)
                            self.mark_matched(potential)

        return len(regions) - len(self.marked)

    def get_potential_pixels(self):
        pixels = []
        for y in range(self.img.shape[0]):
            for x in range(self.img.shape[1]):
                r, g, b = self.img[y, x]
                if r > 250 and g > 250 and b > 250:
                    pixels.append((x, y))
                    pass
        return pixels


def process(data: bytes):
    try:
        return Processor(data).process()
    except Exception as e:
        traceback.print_exc()
        print("error")
        raise IndexError("No image found.")
