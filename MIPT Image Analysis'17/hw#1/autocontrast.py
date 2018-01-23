from __future__ import print_function
from sys import argv
import os.path
import numpy as np
import cv2

def autocontrast(src_path, dst_path, white_perc, black_perc):
    img = cv2.imread(src_path, 1)

    width, height, channels = img.shape
    size = width * height

    temp = img.astype('float64')

    for i in range(channels):
        hist = cv2.calcHist([img], [i], None, [256], [0, 256]).ravel()

        white_bound = 255
        while white_perc * size > np.sum(hist[white_bound:]):
            white_bound -= 1

        black_bound = 0
        while float(black_perc) * size > np.sum(hist[:black_bound]):
            black_bound += 1

        temp[:, :, i] = (temp[:, :, i] - black_bound) * 255. / (white_bound - black_bound)

    temp[temp > 255.] = 255
    temp[temp < 0.] = 0
    img = temp.astype('uint8')

    cv2.imwrite(dst_path, img)


if __name__ == '__main__':
    assert len(argv) == 5
    assert os.path.exists(argv[1])
    argv[3] = float(argv[3])
    argv[4] = float(argv[4])

    assert 0 <= argv[3] < 1
    assert 0 <= argv[4] < 1

    autocontrast(*argv[1:])