"""
@author: Thang Nguyen <nhthang1009@gmail.com>
Modified for dynamic aspect ratio detection and resolution scaling.
"""
import argparse
import cv2
import numpy as np
import glob
from itertools import product


def get_args():
    parser = argparse.ArgumentParser("Viet Nguyen Photomosaic")
    parser.add_argument("--input", type=str, default="data/input.jpg", help="Path to input image")
    parser.add_argument("--output", type=str, default="data/output.jpg", help="Path to output image")
    parser.add_argument("--pool", type=str, default="image_pool", help="Path to directory containing component images")
    parser.add_argument("--stride", type=int, default=30, help="size of each component image")
    parser.add_argument("--scale", type=int, default=1, help="Multiplier to upscale the final mosaic resolution")
    args = parser.parse_args()
    return args


def get_component_images(path, tile_w, tile_h):
    images = []
    avg_colors = []
    for image_path in glob.glob("{}/*.png".format(path)) + glob.glob("{}/*.jpg".format(path)):
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        image = cv2.resize(image, (tile_w, tile_h))
        images.append(image)
        avg_colors.append(np.sum(np.sum(image, axis=0), axis=0) / (tile_w * tile_h))
    return images, np.array(avg_colors)


def main(opt):
    image_paths = glob.glob("{}/*.png".format(opt.pool)) + glob.glob("{}/*.jpg".format(opt.pool))
    
    if not image_paths:
        print("Error: No images found in the pool directory. Check your --pool path.")
        return

    sample_image = cv2.imread(image_paths[0], cv2.IMREAD_COLOR)
    orig_h, orig_w, _ = sample_image.shape
    
    # Scale the tile dimensions automatically based on the scale multiplier
    tile_h = opt.stride * opt.scale
    tile_w = int((opt.stride * opt.scale) * (orig_w / orig_h))

    input_image = cv2.imread(opt.input, cv2.IMREAD_COLOR)
    
    # Scale up the original canvas
    if opt.scale > 1:
        input_image = cv2.resize(input_image, (input_image.shape[1] * opt.scale, input_image.shape[0] * opt.scale), interpolation=cv2.INTER_CUBIC)

    height, width, num_channels = input_image.shape
    blank_image = np.zeros((height, width, 3), np.uint8)
    
    images, avg_colors = get_component_images(opt.pool, tile_w, tile_h)
    
    for i, j in product(range(int(width / tile_w)), range(int(height / tile_h))):
        partial_input_image = input_image[j * tile_h: (j + 1) * tile_h,
                              i * tile_w: (i + 1) * tile_w, :]
        partial_avg_color = np.sum(np.sum(partial_input_image, axis=0), axis=0) / (tile_w * tile_h)
        distance_matrix = np.linalg.norm(partial_avg_color - avg_colors, axis=1)
        idx = np.argmin(distance_matrix)
        blank_image[j * tile_h: (j + 1) * tile_h, i * tile_w: (i + 1) * tile_w, :] = images[idx]
        
    cv2.imwrite(opt.output, blank_image)


if __name__ == '__main__':
    opt = get_args()
    main(opt)