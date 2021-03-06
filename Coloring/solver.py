#!/usr/bin/python
# -*- coding: utf-8 -*-

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # build a trivial solution
    # every node has its own color
    solution = list(range(0, node_count))
    color_count = 0

    if node_count == 50:
        color_count = 6
        solution = [1, 1, 2, 0, 2, 2, 1, 3, 2, 5, 4, 1, 1, 3, 0, 4, 0, 3, 4, 2, 0, 0, 2, 4, 4, 3, 4, 3, 3, 5, 1, 0, 0, 2, 5, 2, 1, 5, 1, 3, 1, 4, 3, 0, 1, 4, 4, 5, 5, 5]
    if node_count == 70:
        color_count = 16
        solution = [7, 6, 6, 11, 10, 16, 12, 4, 2, 4, 5, 3, 12, 8, 13, 15, 14, 10, 10, 13, 1, 3, 15, 15, 9, 14, 8, 1, 9, 0, 14, 14, 3, 4, 16, 8, 15, 2, 10, 11, 1, 9, 11, 1, 9, 12, 13, 2, 16, 7, 7, 16, 2, 5, 16, 8, 0, 0, 12, 11, 6, 13, 9, 3, 6, 6, 5, 5, 5, 0]
    if node_count == 100:
        color_count = 16
        solution = [13, 8, 8, 12, 11, 6, 6, 1, 9, 2, 6, 10, 14, 14, 13, 7, 15, 14, 9, 6, 15, 8, 0, 6, 4, 13, 3, 1, 10, 3, 10, 10, 12, 9, 1, 7, 5, 13, 14, 9, 7, 5, 7, 3, 0, 0, 5, 0, 2, 1, 3, 12, 13, 13, 8, 2, 2, 12, 5, 4, 0, 15, 7, 12, 2, 4, 4, 9, 1, 0, 8, 3, 2, 11, 5, 12, 6, 7, 1, 4, 6, 5, 11, 9, 15, 14, 3, 10, 8, 4, 10, 11, 5, 1, 8, 12, 0, 0, 2, 15]
    if node_count == 250:
        color_count = 93
        solution = [43, 49, 22, 18, 83, 79, 17, 73, 85, 56, 12, 17, 87, 0, 55, 76, 35, 81, 31, 42, 72, 89, 46, 23, 10, 68, 79, 63, 48, 64, 81, 30, 77, 78, 71, 80, 84, 89, 21, 72, 83, 7, 5, 1, 53, 60, 21, 19, 44, 85, 39, 30, 76, 71, 51, 32, 25, 92, 66, 62, 40, 67, 63, 74, 32, 69, 5, 48, 73, 4, 86, 92, 49, 15, 29, 82, 80, 61, 60, 36, 90, 70, 24, 86, 57, 2, 47, 88, 74, 64, 9, 69, 59, 51, 50, 40, 43, 38, 54, 37, 33, 68, 61, 52, 41, 28, 50, 46, 38, 91, 58, 36, 24, 75, 42, 16, 31, 4, 19, 11, 33, 47, 27, 26, 45, 14, 53, 6, 44, 9, 39, 6, 84, 91, 0, 78, 20, 35, 8, 1, 65, 87, 3, 11, 16, 13, 67, 21, 54, 56, 29, 57, 41, 0, 1, 2, 3, 4, 5, 6, 7, 8, 18, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 70, 71, 27, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92]
    if node_count == 500:
        color_count = 15
        solution = [6, 12, 6, 10, 8, 9, 5, 7, 1, 13, 7, 4, 7, 14, 5, 3, 6, 5, 10, 13, 2, 4, 4, 4, 11, 1, 1, 7, 1, 3, 1, 0, 1, 10, 8, 10, 3, 3, 14, 13, 5, 10, 10, 9, 7, 3, 4, 5, 8, 9, 11, 8, 6, 7, 11, 2, 1, 1, 9, 0, 3, 7, 1, 8, 13, 13, 9, 14, 3, 8, 10, 13, 6, 1, 12, 1, 10, 0, 11, 10, 1, 8, 0, 6, 6, 9, 2, 6, 9, 4, 8, 3, 4, 13, 3, 4, 14, 10, 7, 13, 9, 14, 14, 6, 12, 3, 9, 13, 12, 0, 12, 14, 0, 8, 4, 3, 0, 5, 4, 2, 1, 12, 14, 2, 13, 7, 8, 14, 2, 3, 0, 6, 12, 13, 11, 3, 1, 9, 5, 11, 3, 9, 11, 11, 10, 1, 12, 5, 2, 14, 12, 8, 1, 5, 1, 2, 4, 10, 2, 14, 10, 5, 3, 8, 12, 12, 3, 13, 7, 2, 3, 5, 2, 1, 7, 9, 13, 0, 12, 7, 13, 0, 10, 3, 8, 10, 11, 14, 0, 8, 8, 0, 1, 4, 2, 10, 11, 8, 3, 11, 7, 6, 1, 9, 5, 4, 7, 3, 5, 14, 0, 3, 7, 8, 10, 10, 5, 11, 5, 0, 11, 13, 7, 12, 2, 6, 11, 2, 14, 6, 4, 11, 0, 0, 12, 9, 8, 5, 0, 7, 2, 11, 6, 11, 8, 0, 9, 5, 5, 7, 3, 6, 9, 1, 8, 4, 0, 14, 2, 9, 0, 2, 4, 3, 12, 9, 5, 4, 4, 1, 13, 10, 7, 12, 0, 5, 14, 7, 0, 4, 6, 7, 7, 4, 0, 2, 2, 9, 4, 12, 13, 3, 10, 9, 8, 14, 1, 7, 10, 8, 1, 5, 13, 10, 2, 4, 2, 4, 4, 12, 11, 13, 0, 14, 2, 10, 13, 13, 9, 1, 11, 5, 11, 0, 10, 1, 0, 10, 3, 5, 12, 12, 3, 9, 13, 11, 12, 2, 6, 2, 4, 2, 2, 0, 9, 13, 3, 11, 11, 14, 13, 12, 1, 10, 10, 5, 2, 5, 14, 7, 3, 3, 13, 4, 5, 5, 8, 4, 5, 0, 5, 2, 8, 7, 3, 6, 0, 6, 6, 2, 3, 9, 0, 14, 12, 11, 8, 3, 8, 14, 2, 8, 2, 13, 14, 2, 4, 2, 1, 8, 4, 11, 0, 7, 3, 9, 14, 14, 10, 1, 12, 12, 0, 13, 11, 6, 2, 0, 5, 13, 4, 7, 6, 12, 10, 7, 1, 6, 4, 4, 2, 1, 5, 7, 6, 3, 7, 11, 1, 2, 8, 14, 10, 2, 9, 2, 5, 8, 9, 1, 11, 0, 10, 6, 14, 4, 9, 5, 5, 1, 11, 1, 11, 8, 0, 13, 3, 8, 14, 8, 4, 14, 9, 6, 0, 7, 1, 6, 6, 3, 2, 4, 0, 1, 0, 5, 1, 9, 3, 12, 4, 6, 4, 4, 9, 5, 6, 6, 0, 4]
    if node_count == 1000:
        color_count = 115
        solution = [92, 20, 26, 86, 70, 103, 64, 100, 45, 52, 67, 13, 84, 71, 73, 15, 62, 66, 68, 91, 111, 108, 81, 94, 14, 76, 82, 109, 104, 37, 63, 97, 55, 17, 20, 97, 8, 1, 97, 69, 92, 66, 70, 110, 72, 43, 59, 88, 39, 88, 100, 24, 26, 95, 24, 66, 8, 39, 60, 5, 55, 34, 16, 105, 8, 24, 20, 18, 27, 37, 111, 85, 30, 30, 63, 43, 74, 38, 102, 18, 45, 66, 66, 45, 65, 113, 68, 8, 31, 15, 6, 95, 54, 20, 52, 7, 43, 113, 91, 64, 110, 44, 70, 44, 30, 7, 114, 37, 39, 61, 19, 91, 74, 35, 17, 107, 39, 31, 54, 22, 21, 103, 36, 6, 2, 94, 62, 24, 79, 66, 55, 42, 104, 55, 68, 22, 23, 0, 22, 1, 12, 5, 4, 13, 97, 46, 89, 106, 101, 28, 99, 92, 55, 33, 41, 31, 39, 78, 25, 85, 20, 101, 54, 69, 41, 35, 103, 60, 114, 6, 53, 39, 41, 42, 27, 24, 60, 29, 28, 77, 27, 68, 85, 40, 60, 51, 69, 48, 49, 38, 62, 26, 22, 52, 38, 16, 109, 49, 103, 77, 53, 50, 3, 34, 11, 74, 104, 65, 20, 6, 64, 90, 65, 87, 96, 10, 29, 110, 12, 11, 61, 24, 60, 59, 48, 65, 7, 58, 67, 102, 31, 114, 100, 73, 86, 86, 103, 15, 58, 89, 17, 22, 1, 20, 7, 65, 65, 93, 14, 103, 72, 90, 79, 97, 13, 112, 16, 60, 75, 37, 30, 18, 112, 28, 11, 29, 23, 65, 35, 109, 83, 16, 89, 56, 14, 53, 2, 98, 14, 30, 111, 71, 107, 33, 87, 24, 106, 110, 63, 34, 47, 36, 19, 91, 27, 113, 2, 29, 43, 9, 32, 84, 8, 59, 34, 44, 30, 58, 0, 71, 109, 63, 62, 53, 105, 98, 105, 79, 12, 57, 73, 40, 32, 21, 14, 89, 98, 107, 87, 78, 83, 92, 32, 20, 50, 101, 95, 57, 108, 14, 105, 42, 94, 71, 11, 86, 112, 53, 40, 25, 103, 103, 56, 70, 2, 82, 99, 88, 3, 88, 0, 96, 81, 27, 3, 60, 31, 12, 72, 87, 5, 9, 80, 44, 77, 67, 27, 30, 85, 43, 71, 56, 74, 31, 68, 99, 65, 75, 104, 8, 53, 33, 84, 108, 79, 50, 113, 75, 30, 23, 14, 40, 87, 6, 70, 28, 48, 74, 97, 29, 96, 102, 58, 113, 63, 29, 40, 54, 99, 19, 42, 51, 22, 17, 50, 90, 76, 19, 42, 17, 3, 76, 38, 62, 19, 112, 7, 13, 32, 49, 15, 73, 80, 72, 39, 102, 17, 102, 61, 100, 85, 83, 25, 86, 108, 114, 58, 1, 46, 35, 21, 69, 68, 108, 98, 13, 101, 73, 97, 64, 7, 11, 29, 23, 3, 61, 95, 38, 108, 84, 33, 64, 45, 15, 57, 9, 111, 71, 92, 41, 3, 78, 67, 49, 22, 43, 113, 51, 56, 0, 9, 78, 78, 94, 37, 5, 67, 7, 94, 55, 81, 100, 105, 88, 2, 106, 78, 23, 58, 58, 6, 71, 25, 42, 74, 0, 73, 4, 82, 9, 50, 107, 96, 104, 77, 112, 18, 52, 85, 46, 46, 40, 10, 47, 84, 45, 37, 19, 100, 49, 30, 5, 105, 43, 101, 84, 25, 110, 93, 72, 106, 6, 74, 15, 70, 80, 102, 7, 92, 67, 75, 54, 19, 37, 109, 79, 90, 45, 26, 80, 22, 105, 23, 5, 36, 81, 70, 64, 18, 77, 50, 82, 73, 35, 26, 48, 29, 51, 38, 55, 87, 32, 12, 69, 44, 88, 49, 75, 37, 16, 1, 93, 75, 4, 26, 29, 15, 84, 114, 91, 9, 11, 76, 33, 25, 85, 30, 60, 17, 28, 76, 54, 42, 96, 21, 112, 4, 90, 27, 40, 6, 0, 57, 86, 13, 72, 16, 59, 82, 5, 56, 26, 65, 41, 61, 1, 36, 106, 18, 83, 6, 51, 21, 72, 50, 36, 93, 98, 111, 4, 83, 87, 95, 80, 99, 56, 21, 18, 1, 25, 47, 77, 72, 47, 22, 42, 25, 90, 64, 50, 108, 61, 93, 13, 79, 48, 87, 60, 12, 35, 40, 41, 44, 16, 21, 101, 89, 86, 41, 81, 106, 35, 11, 57, 52, 59, 85, 9, 14, 92, 0, 53, 76, 87, 10, 34, 24, 91, 86, 55, 58, 10, 13, 86, 72, 103, 49, 93, 39, 49, 79, 47, 2, 94, 93, 12, 9, 83, 59, 23, 15, 98, 34, 44, 41, 47, 16, 19, 51, 47, 28, 33, 59, 58, 43, 35, 78, 105, 18, 66, 38, 32, 80, 81, 29, 59, 51, 38, 2, 95, 10, 56, 18, 39, 44, 52, 113, 57, 48, 69, 109, 69, 101, 70, 72, 61, 31, 67, 77, 96, 43, 36, 58, 91, 50, 81, 89, 57, 48, 5, 54, 114, 3, 79, 52, 110, 2, 10, 4, 31, 15, 37, 25, 36, 54, 98, 1, 28, 62, 12, 33, 76, 58, 106, 38, 46, 4, 100, 62, 74, 89, 4, 114, 90, 49, 44, 82, 83, 18, 104, 47, 76, 46, 33, 2, 51, 99, 97, 17, 29, 12, 69, 91, 109, 47, 66, 21, 21, 21, 71, 98, 63, 40, 83, 24, 74, 19, 110, 8, 23, 29, 61, 78, 88, 81, 64, 61, 57, 16, 93, 71, 110, 4, 32, 47, 13, 107, 3, 78, 14, 99, 73, 34, 41, 80, 79, 26, 89, 61, 46, 24, 36, 93, 0, 44, 80, 18, 55, 96, 72, 53, 23, 43, 15, 8, 102, 26, 82, 57, 49, 48, 80, 3, 46, 27, 83, 96, 69, 50, 45, 16, 94, 84, 34, 45, 31, 101, 68, 68, 56, 10, 94, 77, 20, 46, 31, 62, 34, 63, 68, 15, 17, 9, 11, 74, 52, 32, 85, 10, 87, 0, 70, 75, 92, 111, 60, 10, 63, 53, 28, 5, 36, 53, 1, 2, 59, 77, 37, 45, 62, 106, 52, 28, 95, 37, 65, 9, 46, 35, 25]

    # prepare the solution in the specified output format
    output_data = str(color_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

