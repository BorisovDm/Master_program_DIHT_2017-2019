import numpy as np
import math

def main():
    #инициализация
    edges_number = int(input())
    adjacency_list = dict()
    coordinates_of_fixed_vertices = dict()

    #ввод рёбер
    for i in range(edges_number):
        vertex1, vertex2 = [int(i) for i in input().split(' ')]

        if vertex1 in adjacency_list:
            adjacency_list[vertex1].append(vertex2)
        else:
            adjacency_list[vertex1] = [vertex2]

        if vertex2 in adjacency_list:
            adjacency_list[vertex2].append(vertex1)
        else:
            adjacency_list[vertex2] = [vertex1]
    vertex_number = max(adjacency_list.keys()) + 1

    #Ищем вершины, образующие границу грани графа(простой цикл по последовательным вершинам, включающий 0)
    for i in range(2, vertex_number):
        if 0 in adjacency_list[i]:
            fixed_vertices_number = i + 1
            break

    #Размещаем эти вершины в вершинах правильно n-угольника, вписанного в единичную окружность
    angle_step = 2 * math.pi / fixed_vertices_number
    for i in range(fixed_vertices_number):
        angle = angle_step * i
        coordinates_of_fixed_vertices[i] = (math.cos(angle), math.sin(angle))

    #Находим координаты оставшихся вершин
    matrix_size = 2 * (vertex_number - fixed_vertices_number)
    linear_equations_system = np.zeros((matrix_size, matrix_size))
    right_side = np.zeros(matrix_size)

    for i in range(fixed_vertices_number, vertex_number):
        line_index = i - fixed_vertices_number

        linear_equations_system[2 * line_index, 2 * line_index] = -len(adjacency_list[i])
        linear_equations_system[2 * line_index + 1, 2 * line_index + 1] = -len(adjacency_list[i])

        for j in adjacency_list[i]:
            if j < fixed_vertices_number:
                x, y = coordinates_of_fixed_vertices[j]
                right_side[2 * line_index] -= x
                right_side[2 * line_index + 1] -= y
            else:
                column_index = j - fixed_vertices_number
                linear_equations_system[2 * line_index, 2 * column_index] = 1
                linear_equations_system[2 * line_index + 1, 2 * column_index + 1] = 1
    solution = np.linalg.solve(linear_equations_system, right_side).reshape((matrix_size // 2,2))

    #Вывод координат вершин
    for i in range(fixed_vertices_number):
        x, y = coordinates_of_fixed_vertices[i]
        print(i, x, y)

    for i in range(fixed_vertices_number, vertex_number):
        x, y = solution[i - fixed_vertices_number]
        print(i, x, y)

if __name__ == '__main__':
    main()