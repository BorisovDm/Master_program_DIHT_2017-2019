import numpy as np


def main():
    # считываем количество ребер; будем хранить ребра в списках смежности
    edges_number = int(input())
    adjacency_list = dict()

    # создадим словарь для внутренней нумерации вершин
    vertices_number = 0
    vertices = dict()

    for i in range(edges_number):
        # считываем ребра
        vertex1, vertex2 = [int(i) for i in input().split(' ')]

        # заполняем словарь vertices
        for vertex in [vertex1, vertex2]:
            if vertex not in vertices:
                vertices[vertex] = vertices_number
                vertices_number += 1

        # вершины уже в новых обозначениях
        vertex1, vertex2 = vertices[vertex1], vertices[vertex2]

        # заполняем списки смежности adjacency_list
        for vertex in [vertex1, vertex2]:
            if vertex not in adjacency_list:
                adjacency_list[vertex] = set()
        adjacency_list[vertex1].add(vertex2)
        adjacency_list[vertex2].add(vertex1)

    # создаем и заполняем матрицу Лапласа
    laplace_matrix = np.zeros((vertices_number, vertices_number), dtype=np.int)
    for vertex1 in range(vertices_number):
        for vertex2 in adjacency_list[vertex1]:
            laplace_matrix[vertex1, vertex2] = -1
        laplace_matrix[vertex1, vertex1] = len(adjacency_list[vertex1])

    # найдем собственные значения и векторы матрицы Лапласа;
    # матрица Лапласа является положительно полуопределеной, поэтому
    # она имеет n неотрицательных вещественных собственных значений;
    # функция eigh возвращает собственные значения в порядке возрастания;

    # берем собств.вектор второго собств.значения
    vector = np.linalg.eigh(laplace_matrix)[1][:, 1]

    # считаем перестановку вектора
    vector_with_indices = [0] * len(vector)
    for index, coord in enumerate(vector):
        vector_with_indices[index] = (coord, index)
    vector_sorted = sorted(vector_with_indices, reverse=True)
    permutation = np.array(vector_sorted, dtype=np.int)[:, 1]

    # считаем плотности разрезов
    cut_density = [0] * (vertices_number - 1)
    for k in range(1, vertices_number):
        a = permutation[:k]
        cut_edges_number = 0
        for vertex1 in a:
            for vertex2 in adjacency_list[vertex1]:
                if vertex2 not in a:
                    cut_edges_number += 1
        cut_density[k - 1] = vertices_number * cut_edges_number / \
                             (len(a) * (vertices_number - len(a)))

    # выбираем разрезы минимальной плотности
    min_cut_density = min(cut_density)
    min_cut_density_indices = []
    for index, density in enumerate(cut_density):
        if density == min_cut_density:
            min_cut_density_indices.append(index)

    # вывод лексикографически минимального разреза
    output_vertices_list = []
    for index in min_cut_density_indices:
        # выбираем наименьшую по мощности компоненту разреза
        if index + 1 < vertices_number / 2:
            a = permutation[:index + 1]
        elif index + 1 > vertices_number / 2:
            a = permutation[index + 1:]
        else:
            a = permutation[:index + 1]
            if 0 not in a:
                a = permutation[index + 1:]

        output_vertices = []
        for key, value in vertices.items():
            if value in a:
                output_vertices.append(key)
        output_vertices_list.append(sorted(output_vertices))
    print(' '.join(str(i) for i in min(output_vertices_list)))


if __name__ == '__main__':
    main()
