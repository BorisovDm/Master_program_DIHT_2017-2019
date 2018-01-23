from __future__ import print_function
from sys import argv
import os.path, json
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def generate_data(img_size, line_params, n_points, sigma, inlier_ratio):
    w, h = img_size
    a, b, c = line_params
    assert not (a == 0 and b == 0)

    inlier_count = int(n_points * inlier_ratio)
    outlier_count = n_points - inlier_count

    if a == 0: #horizontal line
        y_value = -1. * c / b
        inlier_x = np.random.uniform(3 * sigma, w - 3 * sigma, inlier_count)
        inlier_y = np.zeros(inlier_count) + y_value
        x_start, x_end = 0, w
        y_start, y_end = y_value - h / 2., y_value + h / 2.
    elif b == 0: #vertical line
        x_value = -1. * c / a
        inlier_y = np.random.uniform(3 * sigma, h - 3 * sigma, inlier_count)
        inlier_x = np.zeros(inlier_count) + x_value
        x_start, x_end = x_value - w / 2., x_value + w / 2.
        y_start, y_end = 0, h
    else:
        # y = kx + t
        k, t = -1. * a / b, -1. * c / b
        img_tan = 1. * h / w
        line_tan = abs(k)

        if line_tan <= img_tan:
            inlier_x = np.random.uniform(3 * sigma, w - 3 * sigma, inlier_count)
            inlier_y = k * inlier_x + t
            x_start, x_end = 0, w
            y_mean = (np.max(inlier_y) + np.min(inlier_y)) / 2.
            y_start, y_end = y_mean - h / 2., y_mean + h / 2.
        else:
            inlier_y = np.random.uniform(3 * sigma, h - 3 * sigma, inlier_count)
            inlier_x = (inlier_y - t) / k
            x_mean = (np.max(inlier_x) + np.min(inlier_x)) / 2.
            x_start, x_end = x_mean - w / 2., x_mean + w / 2.
            y_start, y_end = 0, h

    inlier_x_noise = inlier_x + np.random.normal(0, sigma, inlier_count)
    inlier_y_noise = inlier_y + np.random.normal(0, sigma, inlier_count)

    outlier_x = np.random.uniform(x_start, x_end, outlier_count)
    outlier_y = np.random.uniform(y_start, y_end, outlier_count)

    x = np.hstack((inlier_x_noise, outlier_x))
    y = np.hstack((inlier_y_noise, outlier_y))

    points = np.array(zip(x, y))
    np.random.shuffle(points)
    return points

def compute_ransac_iter_count(conv_prob, inlier_ratio):
    return int(np.ceil(np.log(1 - conv_prob) / np.log(1 - inlier_ratio**2)))

def compute_ransac_thresh(alpha, sigma):
    return stats.chi2.ppf(alpha, sigma)

def compute_line_ransac(data, t, n):
    n_points, _ = data.shape
    cost = 0

    for i in range(n):
        indexes = np.random.randint(0, n_points, size=2)
        x1, y1 = data[indexes[0]]
        x2, y2 = data[indexes[1]]

        line_coeffs = np.array((y1 - y2, x2 - x1, x1 * y2 - x2 * y1))
        a, b, c = line_coeffs
        d = abs(a * data[:,0] + b * data[:,1] + c) / np.sqrt(a**2 + b**2)

        current_cost = sum(d <= t)
        if current_cost > cost:
            cost, coeffs = current_cost, line_coeffs
    return coeffs

def main():
    assert len(argv) == 2
    assert os.path.exists(argv[1])

    with open(argv[1]) as fin:
        params = json.load(fin)

    """
    params:
    line_params: (a,b,c) - line params (ax+by+c=0)
    img_size: (w, h) - size of the image
    n_points: count of points to be used

    sigma - Gaussian noise
    alpha - probability of point is an inlier

    inlier_ratio - ratio of inliers in the data
    conv_prob - probability of convergence
    """

    data = generate_data((params['w'], params['h']),
                         (params['a'], params['b'], params['c']),
                         params['n_points'], params['sigma'],
                         params['inlier_ratio'])

    t = compute_ransac_thresh(params['alpha'], params['sigma'])
    n = compute_ransac_iter_count(params['conv_prob'], params['inlier_ratio'])

    detected_line = compute_line_ransac(data, t, n)
    true_line = params['a'], params['b'], params['c']

    x_min, x_max = np.min(data[:,0]), np.max(data[:,0])
    y_min, y_max = np.min(data[:,1]), np.max(data[:,1])
    colors = ['red', 'yellow']
    labels = ['true line', 'detected line']

    for line_coeffs, color, label in zip(np.array((true_line, detected_line)), colors, labels):
        a, b, c = line_coeffs
        if b == 0:
            x_value = -1. * c / a
            plt.plot([x_value, x_value], [y_min, y_max], color=color, linewidth=1, label=label)
        else:
            x_plot = np.array((x_min, x_max))
            y_plot = -(a * x_plot + c) / b
            plt.plot(x_plot, y_plot, color=color, linewidth=1, label=label)
    plt.scatter(data[:,0], data[:,1], color='blue', label='points', s = 8)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
