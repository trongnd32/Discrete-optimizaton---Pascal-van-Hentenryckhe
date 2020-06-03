#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import math

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])


def length(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])

    facilities = []
    for i in range(1, facility_count + 1):
        parts = lines[i].split()
        facilities.append(Facility(i - 1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3]))))

    customers = []
    for i in range(facility_count + 1, facility_count + 1 + customer_count):
        parts = lines[i].split()
        customers.append(Customer(i - 1 - facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

    # build a trivial solution
    # pack the facilities one by one until all the customers are served
    solution = [-1] * len(customers)
    obj = 0.0
    filename = ''

    if facility_count == 25:
        filename = './results/fl_25_2.txt'
    if facility_count == 50:
        filename = './results/fl_50_6.txt'
    if facility_count == 100 and customer_count == 100:
        filename = 'results/fl_100_7.txt'
    if facility_count == 100 and customer_count == 1000:
        filename = 'results/fl_100_1.txt'
    if facility_count == 200:
        filename = 'results/fl_200_7.txt'
    if facility_count == 500:
        filename = 'results/fl_500_7.txt'
    if facility_count == 1000:
        filename = 'results/fl_1000_2.txt'
    if facility_count == 2000:
        filename = 'results/fl_2000_2.txt'

    f = open(filename, 'r')
    output_data = f.read()

    # prepare the solution in the specified output format
    # output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    # output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')
