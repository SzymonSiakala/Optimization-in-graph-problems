# Optimization in graph problems
# Szymon Siąkała & Artur Oleksiński

import csv
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

''' FUNCTION FOR LOADING DATA FROM CSV FILES '''
def load_data(matrix_file_path = "./Matrix.csv", coordinates_file_path = "./Coordinates.csv"):
    with open(matrix_file_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        matrix = []
        labels = {}
        for row in csv_reader:
            if labels:
                temp = []
                for j in range(len(row)):
                    temp.append(int(row[j]))
                matrix.append(temp)
            else:
                labels = {j: name for j, name in enumerate(row)}

    with open(coordinates_file_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        coordinates = {}
        for row in csv_reader:
            coordinates[row[0]] = [int(row[1]), int(row[2])];

    return labels, matrix, coordinates

''' PLOT CREATION FUNCTION '''
def create_plot(labels, coordinates, matrix, start, target, route, distance, map_file = "./Map.png"):
    x = [coordinates[i][0] for i in coordinates]
    y = [coordinates[i][1] for i in coordinates]
    plt.plot(x, y, 'bo')
    
    x_start = coordinates[start][0]
    y_start = coordinates[start][1]

    plt.plot(x_start, y_start, 'ro')

    x_target = coordinates[target][0]
    y_target = coordinates[target][1]

    plt.plot(x_target, y_target, 'ro')

    x_range = float('-inf')
    y_range = float('-inf')
    for values in coordinates.values():
        x_range = max(x_range, values[0])
        y_range = max(y_range, values[1])
    plt.axis([0, x_range + 3, 0, y_range + 3])

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j]:
                plt.plot([x[i], x[j]], [y[i], y[j]], color='blue')
                # plt.text((x[i] + x[j]) / 2, (y[i] + y[j]) / 2, matrix[i][j],  weight='bold')

    for i, j in route:
        temp = [coordinates[i][0], coordinates[j][0], coordinates[i][1], coordinates[j][1]]
        plt.plot([temp[0], temp[1]], [temp[2], temp[3]], color='red')
        index_i = list(labels.keys())[list(labels.values()).index(i)]
        index_j = list(labels.keys())[list(labels.values()).index(j)]
        plt.text((temp[0] + temp[1]) / 2, (temp[2] + temp[3]) / 2, matrix[index_i][index_j], color='red',  weight='bold')

    for i in range(len(labels)):
        plt.text(x[i] - 1, y[i] + 1, labels[i], weight='bold')

    plt.text(1, 1, f"Distance from {start} to {target} is equal to: {distance} km.", weight='bold', backgroundcolor='#E0E0E0')
    plt.title("Optimization in graph problems - Dijkstra algorithm", weight='bold')

    img = mpimg.imread(map_file)
    plt.imshow(img, extent=[0, x_range + 3, 0, y_range + 3], aspect='auto')

    return plt

''' GRAPH CREATION FUNCTION '''
def create_graph(labels, matrix):
    graph = {}

    for i in range(len(matrix)):
        temp = []
        for j in range(len(matrix[i])):
            if matrix[i][j]:
                temp.append((labels[j], matrix[i][j]))
        graph[labels[i]] = temp

    return graph

''' DIJKSTRA ALGORITHM '''
def dijkstra(graph, start, target):
    distances = dict.fromkeys(graph, float('inf'))
    previous = dict.fromkeys(graph)
    names = list(graph)
    distances[start] = 0

    while names:
        node = min(names, key=lambda x: distances[x])
        names.remove(node)
        for i, j in graph[node]:
            alt = distances[node] + j
            if alt < distances[i]:
                distances[i] = alt
                previous[i] = node

    route = []
    temp = target
    while temp != start:
        route.append([previous[temp], temp])
        temp = previous[temp]
    route.reverse()
    return route, distances[target]

''' MAIN FUNCTION '''
if __name__ == "__main__":
    labels, matrix, coordinates = load_data()

    graph = create_graph(labels, matrix)

    start = random.choice(list(labels.values()))
    target = random.choice(list(labels.values()))
    route, distance = dijkstra(graph, start, target)

    plt = create_plot(labels, coordinates, matrix, start, target, route, distance)
    plt.show()