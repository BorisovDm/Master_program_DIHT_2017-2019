# Задание 8: Разрез минимальной плотности

Реализуйте приближённый алгоритм поиска разреза минимальной плотности 
(алгоритм на основе собственного вектора, соответствующего второму по 
величине собственному значению лапласиана графа). На вход программы подаются рёбра графа в виде:

```
<количество рёбер>
<id начала ребра> <id конца ребра>
<id начала ребра> <id конца ребра> 
…
```

id вершин — натуральные числа (необязательно последовательные), изолированных вершин нет. 
Выход программы — разделённые пробельными символами и упорядоченные по возрастанию номера вершин, 
включённых в наименьшую по мощности компоненту разреза. Если есть разные полученные в строгом 
соответствии с алгоритмом ответы, имеющие одинаковую плотность, то нужно вывести лексикографически минимальный из них.

При использовании библиотеки numpy рекомендуется использовать функцию eigh, «заточенную» специально под эрмитовы матрицы.

### Sample Input 1:
```
4
1 4
4 5
5 2
1 5
```

### Sample Output 1:
```
2
```

### Sample Input 2:
```
13
0 5
2 0
8 3
10 5
6 3
9 2
10 3
4 6
7 10
6 0
10 9
1 0
3 2
```

### Sample Output 2:
```
4
```
