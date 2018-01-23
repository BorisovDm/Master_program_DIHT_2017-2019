from __future__ import print_function
from sys import argv
import os.path
import cv2

def box_flter(src_path, dst_path, w, h):
    img = cv2.imread(src_path)
    integral_img = cv2.integral(img)

    width, height, channels = img.shape
    window_size = w * h

    img = img[0:width - w + 1, 0:height - h + 1, :].astype('float64')

    for i in range(0, width - w + 1):
        for j in range(0, height - h + 1):
            img[i, j] = (integral_img[i + w][j + h] + integral_img[i][j] \
                             - integral_img[i][j + h] - integral_img[i + w][j]) / window_size

    img = img.astype('uint8')
    cv2.imwrite(dst_path, img)


if __name__ == '__main__':
    assert len(argv) == 5
    assert os.path.exists(argv[1])
    argv[3] = int(argv[3])
    argv[4] = int(argv[4])
    assert argv[3] > 0
    assert argv[4] > 0

    box_flter(*argv[1:])