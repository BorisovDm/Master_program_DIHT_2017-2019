import numpy as np

'''
    Используем метод Гаусса с выделением главного элемента для приведения к верхне-треугольной матрице.
    Детерминант такой матрицы - это произведение диагональных элементов.
    Но считать произведение не будем(нам это особо и не нужно).
    Если хотя бы один диагональный элемент нулевой(верхне-треугольной матрицы), то сразу полагаем det = 0.
    Но из-за не точных вычислений будем проверять равенство нулю с погрешностью 1e-10.
'''
def is_determinant_zero(matrix):
    size = matrix.shape[0]
    for i in range(size):
        max_element, line = abs(matrix[i,i]), i
        for j in range(i + 1, size):
            if abs(matrix[j,i]) > max_element:
                max_element, line = abs(matrix[j,i]), j

        if abs(max_element) < 1e-10:
            return True

        if i != line:
            matrix[i], matrix[line] = np.copy(matrix[line]), np.copy(matrix[i])

        for j in range(i + 1, size):
            coeff = matrix[j,i] / matrix[i,i]
            matrix[j] -= matrix[i] * coeff
    return False

def main():
    edges = []
    size = 0
    n = int(input())

    for i in range(n):
        vertex1, vertex2 = [int(i) for i in input().split(' ')]
        edges.append((vertex1, vertex2))

        max_vertex = max(vertex1, vertex2)
        if max_vertex > size: size = max_vertex
    size += 1

    num_attempts = 10
    for attempt in range(num_attempts):
        adjacency_matrix = np.zeros((size, size))
        for vertex1, vertex2 in edges:
            adjacency_matrix[vertex1, vertex2] = np.random.randint(1, 1000)

        if is_determinant_zero(adjacency_matrix) == False:
            print('yes')
            return
    print('no')


if __name__ == '__main__':
    main()