import numpy as np


def main():
    n = int(input())

    # вычисляем квадратичные вычеты
    quadratic_residues = calculate_quadratic_residues(n - 1)

    # вычисляем символы Лежандра
    legendre_symbol = dict()
    for i in range(-n + 2, n - 1):
        if i == 0:
            legendre_symbol[i] = 0
        elif (i + n - 1) % (n - 1) in quadratic_residues:
            legendre_symbol[i] = 1
        else:
            legendre_symbol[i] = -1

    # вычисляем нормализованную матрицу Адамара
    hadamard_matrix = np.zeros((n, n), dtype=np.int)
    hadamard_matrix[0, :] = 1
    hadamard_matrix[:, 0] = 1
    for i in range(1, n):
        for j in range(1, n):
            if i == j:
                hadamard_matrix[i, j] = -1
            else:
                hadamard_matrix[i, j] = legendre_symbol[i - j]

    # замена элементов -1 на 0 в матрице Адамара -> матрица А
    hadamard_matrix[hadamard_matrix == -1] = 0

    # печатаем строку из матрицы А и её дополнение
    for line in hadamard_matrix:
        print(''.join(str(i) for i in line))
        print(''.join(str(i) for i in (line + 1) % 2))


def calculate_quadratic_residues(p):
    quadratic_residues = set()
    for a in range(1, p + 1):
        for x in range(0, p + 1):
            if a == x**2 % p:
                quadratic_residues.add(a)
    return quadratic_residues


if __name__ == '__main__':
    main()
