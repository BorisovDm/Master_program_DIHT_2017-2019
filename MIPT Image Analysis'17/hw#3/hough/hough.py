from __future__ import print_function
from sys import argv
import cv2
import numpy as np


def gradient_img(img):
    hor_grad = (img[1:, :] - img[:-1, :])[:, :-1]
    ver_grad = (img[:, 1:] - img[:, :-1])[:-1:, :]
    magnitude = np.sqrt(hor_grad ** 2 + ver_grad ** 2)

    return magnitude

def hough_transform(img, theta, rho):
    img /= np.max(img)
    height, width = img.shape
    max_distance = np.ceil(np.sqrt(width ** 2 + height ** 2))

    thetas = np.arange(0, np.pi + theta, theta)
    rhos = np.arange(-max_distance, max_distance + rho, rho)
    ht_map = np.zeros((len(thetas), len(rhos)))

    for i in range(height):
        for j in range(width):
            for k in range(len(thetas)):
                if img[i][j] > 0.:
                    r = i * np.sin(thetas[k]) + j * np.cos(thetas[k])
                    ht_map[k][int(np.around((r + max_distance) / rho))] += img[i][j]

    return ht_map, thetas, rhos


def get_lines(ht_map, thetas, rhos, n_lines, min_delta_rho, min_delta_theta):

    theta_collision_step = int(np.ceil(min_delta_theta / abs(thetas[1] - thetas[0])))
    rho_collision_step = int(np.ceil(min_delta_rho / abs(rhos[1] - rhos[0])))

    lines = []
    for k in range(n_lines):
        max_value = ht_map[0][0]
        index = (0, 0)

        for i in range(len(thetas)):
            for j in range(len(rhos)):
                if ht_map[i][j] > max_value:
                    max_value = ht_map[i][j]
                    index = (i, j)

        for i in range(max(0, index[0] - theta_collision_step), min(index[0] + theta_collision_step + 1, len(thetas))):
                ht_map[i][max(0, index[1] - rho_collision_step) : min(index[1] + rho_collision_step + 1, len(rhos))] = 0.

        theta_index = index[0]
        rho_index = index[1]

        lines.append((-np.cos(thetas[theta_index]) / np.sin(thetas[theta_index]),
                   rhos[rho_index] / np.sin(thetas[theta_index])))

    return lines


if __name__ == '__main__':
    assert len(argv) == 9
    src_path, dst_ht_path, dst_lines_path, theta, rho,\
        n_lines, min_delta_rho, min_delta_theta = argv[1:]

    theta = float(theta)
    rho = float(rho)
    n_lines = int(n_lines)
    min_delta_rho = float(min_delta_rho)
    min_delta_theta = float(min_delta_theta)

    assert theta > 0.0
    assert rho > 0.0
    assert n_lines > 0
    assert min_delta_rho > 0.0
    assert min_delta_theta > 0.0

    image = cv2.imread(src_path, 0)
    assert image is not None

    image = image.astype(float)
    gradient = gradient_img(image)

    ht_map, thetas, rhos = hough_transform(gradient, theta, rho)
    cv2.imwrite(dst_ht_path, ht_map)

    lines = get_lines(ht_map, thetas, rhos, n_lines, min_delta_rho, min_delta_theta)
    with open(dst_lines_path, 'w') as fout:
        for line in lines:
            fout.write('%0.3f, %0.3f\n' % line)
