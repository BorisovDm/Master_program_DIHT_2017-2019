import numpy as np
import random


def main():
    vertices_number = int(input())
    vertex_weight = np.zeros(vertices_number, dtype=np.int)

    for i in range(vertices_number):
        vertex_weight[i] = int(input())

    edges_number = int(input())
    edges = []

    for i in range(edges_number):
        vertex1, vertex2 = [int(i) for i in input().split(' ')]
        edges.append((vertex1, vertex2))

    edges_list = [i for i in range(edges_number)]
    random.shuffle(edges_list)

    for i in edges_list:
        vertex1, vertex2 = edges[i]
        if vertex_weight[vertex1] > 0 and vertex_weight[vertex2] > 0:
            min_weight = min(vertex_weight[vertex1], vertex_weight[vertex2])
            vertex_weight[vertex1] -= min_weight
            vertex_weight[vertex2] -= min_weight

    print(' '.join(str(i) for i in range(vertices_number) if vertex_weight[i] == 0))


if __name__ == '__main__':
    main()
