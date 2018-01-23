from __future__ import print_function
from sys import argv
import os.path
import cv2
import numpy as np

def otsu(src_path, dst_path):
    img = cv2.imread(src_path, 0)
    N = img.shape[0] * img.shape[1]
    hist = cv2.calcHist([img], [0], None, [256], [0, 256]).ravel() / N

    start, end = 0, hist.shape[0] - 1
    while(hist[start] == 0): start += 1
    while(hist[end] == 0): end -= 1

    w1, w2 = hist[start], 1 - hist[start]
    m1 = start
    m2 = np.sum(np.arange(start + 1, end + 1) * hist[start + 1 : end + 1]) / w2

    std = w1 * w2 * (m1 - m2) ** 2
    T = start

    for t in range(start + 1, end):
        p = hist[t]
        w1_new, w2_new = w1 + p, w2 - p

        m1_new = (m1 * w1 + p * t) / w1_new
        m2_new = (m2 * w2 - p * t) / w2_new

        w1, w2, m1, m2 = w1_new, w2_new, m1_new, m2_new
        std_new = w1 * w2 * (m1 - m2) ** 2

        if std_new > std:
            std, T = std_new, t

    print("Threshold =", T)
    img[img > T] = 255
    img[img <= T] = 0
    cv2.imwrite(dst_path, img)


if __name__ == '__main__':
    assert len(argv) == 3
    assert os.path.exists(argv[1])
    otsu(*argv[1:])
