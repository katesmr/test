import os
import math
import operator
import functools
from PIL import Image


def is_equal_image(image1, image2):
    h1 = image1.histogram()
    h2 = image2.histogram()
    # calculate the root-mean-square
    rms = math.sqrt(functools.reduce(operator.add, map(lambda a, b: (a - b) ** 2, h1, h2)) / len(h1))
    return rms == 0


def find_repeatable_images(path, image):
    def scan_dir(parent, image_obj):
        for token in os.listdir(parent):
            child = os.path.join(parent, token)
            if os.path.isdir(child):
                scan_dir(child, image_obj)
            elif token.endswith(('.png', '.jpg', '.jpeg')):
                try:
                    comparison_image = Image.open(child)
                except IOError:
                    continue
                if is_equal_image(image_obj, comparison_image):
                    res.append(child)
    res = []
    scan_dir(path, image)
    return res
