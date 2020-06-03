from collections import namedtuple
import math
import random

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

# GLOBAL VARS
## problem parameter
facility_count = 0
customer_count = 0
facilities = []
customers = []
dis = [[0.0 for j in range(facility_count)] for i in range(customer_count)]
available = []

# GLS parameter
features = [[facilities[j].setup_cost for j in range(facility_count)] for i in range(customer_count)]
penalty = [[0 for _ in range(facility_count)] for _ in range(customer_count)]
lamda = 0

dd = [0 for _ in range(facility_count)]
solution = [-1 for _ in range(customer_count)]
obj = 0.0
aug_cost = 0.0

# calculate distance between 2 point
def length(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


# Initialize the weight of penalty
def init_lamda(cost, alpha):
    return alpha * cost / customer_count

# init greedy solution
def init_solution():
    global obj, aug_cost
    min_facility = -1

    for i in range(customer_count):
        min_dis = float('inf')
        for j in range(facility_count):
            if min_dis > dis[i][j] and customers[i].demand <= available[j]:
                min_dis = dis[i][j]
                min_facility = j
        # customer i is serviced by facility j
        solution[i] = min_facility
        available[min_facility] -= customers[i].demand
        dd[min_facility] += 1
        obj += min_dis
        aug_cost += dis[i][min_facility] + lamda * penalty[i][min_facility]
        if dd[min_facility] == 1:
            obj += facilities[min_facility].setup_cost
            aug_cost += facilities[min_facility].setup_cost


# get cost

# get new aug_cost and obj if solution[idx] = facility_new
# @return aug_cost_new, obj_new
def get_cost_move(idx, facility_new):
    global aug_cost, obj
    aug_cost_new = aug_cost
    obj_new = obj

    if solution[idx] == facility_new:
        return obj, aug_cost

    facility_old = solution[idx]
    aug_diff = (0 - penalty[idx][facility_old] + penalty[idx][facility_new]) * lamda
    diff = 0 - dis[idx][facility_old] + dis[idx][facility_new]

    if dd[facility_old] == 1:
        diff -= facilities[facility_old].setup_cost
    if dd[facility_new] == 0:
        diff += facilities[facility_new].setup_cost

    aug_cost_new += diff + aug_diff
    obj_new += diff

    return aug_cost_new, obj_new


# Select a customer, move it to a new facility.
# @return aug_cost_new, obj_new, customer, facility
def get_move():
    global aug_cost, obj

    min_delta = float('inf')
    min_delta_customers = []
    min_delta_facilities = []
    for i in range(customer_count):
        for j in range(facility_count):
            if customers[i].demand <= available[j] and j != solution[i]:
                aug_cost_new, obj_new = get_cost_move(i, j)
                delta = aug_cost_new - aug_cost
                if delta < min_delta:
                    min_delta = delta
                    min_delta_customers.clear()
                    min_delta_facilities.clear()
                    min_delta_customers.append(i)
                    min_delta_facilities.append(j)
                elif delta == min_delta:
                    min_delta_customers.append(i)
                    min_delta_facilities.append(j)

    if min_delta < 0:
        idx = random.randrange(0, len(min_delta_customers), 1)
        customer = min_delta_customers[idx]
        facility = min_delta_facilities[idx]
        return get_cost_move(customer, facility), customer, facility
    else:
        return (0, 0), -1, -1


# make a move
def move(aug_cost_new, obj_new, customer, facility):
    global aug_cost, obj
    aug_cost = aug_cost_new
    obj = obj_new
    dd[solution[customer]] -= 1
    dd[facility] += 1
    available[solution[customer]] += customers[customer].demand
    available[facility] -= customers[customer].demand
    solution[customer] = facility


# Penalize features with the maximum utility
# util = features[cus][fac] / (1 + penalty[cus][fac])
def add_penalty():
    global aug_cost
    max_util = - float('inf')
    max_util_customers = []
    for i in range(customer_count):
        util = features[i][solution[i]] / (1 + penalty[i][solution[i]])
        if util > max_util:
            max_util = util
            max_util_customers.clear()
            max_util_customers.append(i)
        elif util == max_util:
            max_util_customers.append(i)
    for customer in max_util_customers:
        penalty[customer][solution[customer]] += 1
        aug_cost += lamda


# Guided local search
def search(max_iter, alpha=0.05):
    global obj, lamda

    init_solution()
    best_obj = obj
    best_solution = list(solution)
    for _ in range(max_iter):
        (aug_cost_new, obj_new), customer, facility = get_move()
        if customer == -1:
            if lamda == 0:
                lamda = init_lamda(obj, alpha)
            add_penalty()
            # reset search
            break
        else:
            move(aug_cost_new, obj_new, customer, facility)

            if best_obj > obj:
                best_obj = obj
                best_solution = list(solution)

    return best_obj, best_solution


def init():
    global facility_count, customer_count, facilities, customers, features, penalty, dis, dd, solution, available

    dis = [[0.0 for j in range(facility_count)] for i in range(customer_count)]
    # GLS parameter
    features = [[facilities[j].setup_cost for j in range(facility_count)] for i in range(customer_count)]
    penalty = [[0 for _ in range(facility_count)] for _ in range(customer_count)]
    dd = [0 for _ in range(facility_count)]
    solution = [-1 for _ in range(customer_count)]
    available = [facilities[j].capacity for j in range(facility_count)]

    for i in range(customer_count):
        for j in range(facility_count):
            dis[i][j] = length(facilities[j].location, customers[i].location)


def solve_it(input_data):
    global facility_count, customer_count, facilities, customers, dis

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])

    for i in range(1, facility_count + 1):
        parts = lines[i].split()
        facilities.append(
            Facility(i - 1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3]))))

    for i in range(facility_count + 1, facility_count + 1 + customer_count):
        parts = lines[i].split()
        customers.append(Customer(i - 1 - facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

    init()

    # solve
    res_obj, res_solution = search(100000)

    # prepare the solution in the specified output format
    output_data = '%.2f' % res_obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, res_solution))

    return output_data


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
