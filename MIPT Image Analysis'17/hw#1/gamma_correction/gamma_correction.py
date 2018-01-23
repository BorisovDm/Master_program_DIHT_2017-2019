from __future__ import print_function
from sys import argv
import os.path
import cv2

def gamma_correction(src_path, dst_path, a, b):
    img = cv2.imread(src_path)

    img = img.astype('float64')
    img = (a * ((img / 255.) ** b)) * 255.
    img[img > 255.] = 255
    img = img.astype("uint8")

    cv2.imwrite(dst_path, img)


if __name__ == '__main__':
    assert len(argv) == 5
    assert os.path.exists(argv[1])
    argv[3] = float(argv[3])
    argv[4] = float(argv[4])

    gamma_correction(*argv[1:])