from enum import Enum
from pathlib import Path

import numpy as np
from PIL import Image

class Orientation(Enum):
    LANDSCAPE = 1
    PORTRAIT = 2

class Edge(Enum):
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4

def crop_and_save(src_dir, dst_dir, crop_from_fn, threshold):
    src_path = Path(src_dir)
    dst_path = Path(dst_dir)
    
    for src in src_path.iterdir():
        im = Image.open(src)
        pixels = np.asarray(im)
        orientation = Orientation.LANDSCAPE if pixels.shape[1] > pixels.shape[0] else Orientation.PORTRAIT
        crop_from = crop_from_fn(orientation, pixels.shape, src)

        row_mean = pixels.mean((1,2))
        col_mean = pixels.mean((0,2))

        first_col_to_keep = 0
        last_col_to_keep = pixels.shape[1] - 1
        first_row_to_keep = 0
        last_row_to_keep = pixels.shape[0] - 1

        if Edge.BOTTOM in crop_from:
            last_row_to_keep = last_row_to_keep - (np.flip(row_mean) < threshold).argmax()
        if Edge.TOP in crop_from:
            first_row_to_keep = (row_mean < threshold).argmax()
        if Edge.LEFT in crop_from:
            first_col_to_keep = (col_mean < threshold).argmax()
        if Edge.RIGHT in crop_from:
            last_col_to_keep = last_col_to_keep - (np.flip(col_mean) < threshold).argmax()
        
        im_cropped = Image.fromarray(pixels[first_row_to_keep:last_row_to_keep, first_col_to_keep:last_col_to_keep])
        dst_img = dst_path / src.name
        im_cropped.save(dst_img)

def crop_from_general(orientation, shape, src):
    return [Edge.TOP, Edge.BOTTOM, Edge.LEFT, Edge.RIGHT]

# Assumption is that landscape images have white space below and that portrait images have white space to the left
def crop_from_custom(orientation, shape, src):
    crops = []
    if orientation == Orientation.LANDSCAPE:
        crops.append(Edge.BOTTOM)
    elif orientation == Orientation.PORTRAIT:
        crops.append(Edge.LEFT)
    if shape[1] > 2400:
        crops.append(Edge.LEFT)
    if src.name == 'grandpa_0050.jpg':
        crops.append(Edge.BOTTOM)
    return crops

crop_and_save('D:/Documents/test', 'D:/Documents/test result', crop_from_general, 200)