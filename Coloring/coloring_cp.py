#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

from ortools.sat.python import cp_model

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

    model = cp_model.CpModel()
    vars = [model.NewIntVar(0, node_count, str(i)) for i in range(node_count)]
    for e in edges:
        model.Add(vars[e[0]] != vars[e[1]])
    color_count = node_count

    time_limit = 1800
    start_time = time.time()
    while True:
        t = time.time()
        if t - start_time > time_limit:
            break
        for i in range(node_count):
            model.Add(vars[i] < color_count)
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_limit
        status = solver.Solve(model)
        if status == cp_model.FEASIBLE:
            solution.clear()
            for i in range(node_count):
                solution.append(int(solver.Value(vars[i])))
            color_count = max(solution)
        else:
            break

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

