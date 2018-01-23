import numpy as np
from numpy import transpose


def main():
    input_line = np.array([int(i) for i in input().split(' ')])

    input_matrix_size = len(input_line)
    input_matrix = np.zeros((input_matrix_size, input_matrix_size), dtype=np.int)
    input_matrix[0] = input_line

    for i in range(1, input_matrix_size):
        input_matrix[i] = np.array([int(i) for i in input().split(' ')])

    l_matrix, u_matrix, p_matrix = lup_decomposition(input_matrix, input_matrix_size, input_matrix_size)

    for output_line in l_matrix:
        print(' '.join(str(i) for i in output_line))

    for output_line in u_matrix:
        print(' '.join(str(i) for i in output_line))

    for output_line in p_matrix:
        print(' '.join(str(i) for i in output_line))


def lup_decomposition(a, n, m):
    if n == 1:
        l = np.eye(1, dtype=np.int)
        p = np.eye(m, dtype=np.int)

        if a[0, 0] == 0:
            for i in range(m):
                if a[0, i] == 1:
                    p[0, 0], p[i, i] = 0, 0
                    p[i, 0], p[0, i] = 1, 1
                    break
        u = permutation(a, p)
        return l, u, p

    if n & (n - 1):
        h1 = 1
        while h1 * 2 < n:
            h1 *= 2
    else:
        h1 = n // 2
    h2 = n - h1

    l1, u1, p1 = lup_decomposition(a[:h1], h1, m)
    d = permutation(a[h1:], transpose(p1))

    fe = mul(cut(d, 0, h1), reverse(cut(u1, 0, h1)))
    g = add(d, mul(fe, u1))
    l2, u2, p2 = lup_decomposition(cut(g, h1), h2, m - h1)

    p3 = np.zeros((m, m), dtype=np.int)
    for i in range(h1):
        p3[i, i] = 1

    for i in range(h1, m):
        for j in range(h1, m):
            p3[i, j] = p2[i - h1, j - h1]

    h = permutation(u1, transpose(p3))
    l = np.zeros((n, n), dtype=np.int)

    for i in range(h1):
        for j in range(i + 1):
            l[i, j] = l1[i, j]

    for i in range(h2):
        for j in range(h1):
            l[h1 + i, j] = fe[i, j]

    for i in range(h2):
        for j in range(i + 1):
            l[h1 + i, h1 + j] = l2[i, j]

    u = np.zeros((n, m), dtype=np.int)
    for i in range(h1):
        for j in range(i, m):
            u[i, j] = h[i, j]

    for i in range(h2):
        for j in range(i, m - h1):
            u[h1 + i, h1 + j] = u2[i, j]

    p = permutation(p3, p1)
    return l, u, p


def permutation(a, p):
    n, m = a.shape
    permut = []
    for i in range(m):
        for j in range(m):
            if p[i, j]:
                permut.append(j)

    res = np.zeros((n, m), dtype=np.int)
    for j in range(m):
        for i in range(n):
            res[i, permut[j]] = a[i, j]
    return res


def cut(a, l, r=None):
    if r is None:
        r = a.shape[1]
    return a[:, l:r]


def reverse(a):
    n = a.shape[0]
    if n == 1:
        return a

    half_size = n // 2
    b = cut(a[: half_size], half_size)
    c = reverse(cut(a[half_size:], half_size))
    a = reverse(cut(a[: half_size], 0, half_size))
    b = mul(mul(a, b), c)

    res = np.zeros((n, n), dtype=np.int)
    res[:half_size, :half_size] = np.copy(a)
    res[:half_size, half_size:] = np.copy(b)
    res[half_size:, half_size:] = np.copy(c)
    return res


def add(a, b):
    return (a + b) % 2


def mul(a, b):
    n, r = a.shape
    m, l = b.shape

    dim = 1
    max_size = max(n, m, l)
    while dim < max_size:
        dim *= 2

    res = np.zeros((dim, dim), dtype=np.int)
    res[:n, :r] = a
    a = np.copy(res)

    res = np.zeros((dim, dim), dtype=np.int)
    res[:m, :l] = b
    b = np.copy(res)

    res = np.zeros((dim, dim), dtype=np.int)
    if dim <= 2:
        res = np.dot(a, b) % 2
    else:
        half_size = dim // 2
        a11 = cut(a[: half_size], 0, half_size)
        a12 = cut(a[: half_size], half_size)
        a21 = cut(a[half_size:], 0, half_size)
        a22 = cut(a[half_size:], half_size)

        b11 = cut(b[: half_size], 0, half_size)
        b12 = cut(b[: half_size], half_size)
        b21 = cut(b[half_size:], 0, half_size)
        b22 = cut(b[half_size:], half_size)

        p1 = mul(add(a11, a22), add(b11, b22))
        p2 = mul(add(a21, a22), b11)
        p3 = mul(a11, add(b12, b22))
        p4 = mul(a22, add(b21, b11))
        p5 = mul(add(a11, a12), b22)
        p6 = mul(add(a21, a11), add(b11, b12))
        p7 = mul(add(a12, a22), add(b21, b22))

        c11 = add(add(p1, p4), add(p5, p7))
        c12 = add(p3, p5)
        c21 = add(p2, p4)
        c22 = add(add(p1, p2), add(p3, p6))

        res[:half_size, :half_size] = np.copy(c11)
        res[:half_size, half_size:] = np.copy(c12)
        res[half_size:, :half_size] = np.copy(c21)
        res[half_size:, half_size:] = np.copy(c22)
    return cut(res[: n], 0, l)


if __name__ == '__main__':
    main()
