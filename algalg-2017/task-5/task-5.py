from math import pi, sin, cos


def main():
    coeffs = list(map(float, input().strip().split()))
    result = recursive_fft(coeffs)
    print(' '.join(f'{x.real},{x.imag}' for x in result))


def recursive_fft(coeffs):
    n = len(coeffs)
    if n == 1:
        return coeffs

    w = 1
    w_n = cos(2 * pi / n) + 1j * sin(2 * pi / n)

    y_0 = recursive_fft(coeffs[0::2])
    y_1 = recursive_fft(coeffs[1::2])
    y = [0.] * n

    for k in range(n // 2):
        y[k] = y_0[k] + w * y_1[k]
        y[k + n // 2] = y_0[k] - w * y_1[k]
        w = w * w_n
    return y


if __name__ == '__main__':
    main()
