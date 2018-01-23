import numpy as np


def main():
    damping_factor = float(input())
    edges_number = int(input())
    edges = [0] * edges_number

    vertices = dict()
    vertices_number = 0

    for i in range(edges_number):
        vertex1, vertex2 = input().split(' ')
        for vertex in [vertex1, vertex2]:
            if vertex not in vertices:
                vertices[vertex] = vertices_number
                vertices_number += 1
        edges[i] = (vertices[vertex1], vertices[vertex2])

    page_rank_matrix = np.zeros((vertices_number, vertices_number))
    for (i, j) in edges:
        page_rank_matrix[j, i] = 1

    for j in range(vertices_number):
        outgoing_vertices_number = np.sum(page_rank_matrix[:, j])
        if outgoing_vertices_number > 0:
            page_rank_matrix[:, j] /= outgoing_vertices_number
        else:
            page_rank_matrix[:, j] = 1. / vertices_number

    page_rank_matrix = page_rank_matrix * (1 - damping_factor) + \
                       (np.zeros((vertices_number, vertices_number)) + 1) * \
                       damping_factor / vertices_number

    rank_vector_1 = (np.zeros((vertices_number, 1)) + 1) / vertices_number
    rank_vector_2 = np.dot(page_rank_matrix, rank_vector_1)

    while not np.array_equal(rank_vector_1, rank_vector_2):
        rank_vector_1 = np.copy(rank_vector_2)
        rank_vector_2 = np.dot(page_rank_matrix, rank_vector_1)

    for key, value in vertices.items():
        print(key, rank_vector_2[value, 0])


if __name__ == '__main__':
    main()
