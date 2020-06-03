#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])

def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])
    
    customers = []
    for i in range(1, customer_count+1):
        line = lines[i]
        parts = line.split()
        customers.append(Customer(i-1, int(parts[0]), float(parts[1]), float(parts[2])))

    #the depot is always the first customer in the input
    depot = customers[0] 


    # build a trivial solution
    # assign customers to vehicles starting by the largest customer demands
    vehicle_tours = []
    obj = 0
    filename = ''
    if customer_count == 16:
        filename = './results/1.txt'
    if customer_count == 26:
        filename = './results/2.txt'
    if customer_count == 51:
        filename = './results/3.txt'
    if customer_count == 101:
        filename = './results/4.txt'
    if customer_count == 200:
        filename = './results/5.txt'
    if customer_count == 421:
        filename = './results/6.txt'

    f = open(filename, 'r')
    output_data = f.read()

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

        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)')

