from collections import namedtuple
import math
import random

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

# GLOBAL VARIABLES
## problem parameter
facility_count = 0
customer_count = 0
facilities = []
customers = []
dis = [[0.0 for j in range(facility_count)] for i in range(customer_count)]  # khoang cach tu facility den customer
available = []  # suc chua con lai cua moi facility

# GLS parameter
features = [[facilities[j].setup_cost for j in range(facility_count)] for i in range(customer_count)]  # đặc trưng đánh giá của mỗi bước di chuyển
penalty = [[0 for _ in range(facility_count)] for _ in range(customer_count)]  # giá trị phạt của mỗi bước di chuyển, khởi tạo = 0
lamda = 0  # trọng số của giá trị phạt

dd = [0 for _ in range(facility_count)]  # dd[i] đánh dấu số lượng customer sử dụng facility thứ i
solution = [-1 for _ in range(customer_count)]  # kết quả
obj = 0.0  # giá trị hàm mục tiêu
aug_cost = 0.0  # hàm mục tiêu với giá trị phạt


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


# khởi động lại tìm kiếm bằng một lời giải ngẫu nhiên
def restart_search(cnt):
    if cnt == 5:  # khởi động nhiều lần không được thì bỏ
        return False
    global obj, aug_cost, solution, available, dd

    obj = 0
    aug_cost = 0
    solution = [-1 for _ in range(customer_count)]
    available = [facilities[j].capacity for j in range(facility_count)]
    dd = [0 for _ in range(facility_count)]

    # mỗi customer chọn một facility còn đủ sức chứa
    for i in range(customer_count):
        done = False
        x = []
        for j in range(facility_count):
            if customers[i].demand <= available[j]:
                x.append(j)
        if len(x) == 0:
            cnt_c = cnt + 1
            return restart_search(cnt_c)

        random_fac = random.randrange(0, len(x), 1)
        random_fac = x[random_fac]
        solution[i] = random_fac
        available[random_fac] -= customers[i].demand
        dd[random_fac] += 1
        obj += dis[i][random_fac]
        aug_cost += dis[i][random_fac] + lamda * penalty[i][random_fac]
        if dd[random_fac] == 1:
            obj += facilities[random_fac].setup_cost
            aug_cost += facilities[random_fac].setup_cost

    return True


# tính aug_cost and obj nếu gán solution[idx] = facility_new
# @return aug_cost_new, obj_new
def get_cost_move(idx, facility_new):
    global aug_cost, obj
    aug_cost_new = aug_cost
    obj_new = obj

    # nếu solution[idx] == facility_new thì giá trị không đổi
    if solution[idx] == facility_new:
        return obj, aug_cost

    facility_old = solution[idx]
    aug_diff = (0 - penalty[idx][facility_old] + penalty[idx][facility_new]) * lamda  # thay đổi của aug_cost nếu thực hiện di chuyển
    diff = 0 - dis[idx][facility_old] + dis[idx][facility_new]  # thay đổi của obj nếu thực hiện bước di chuyển

    if dd[facility_old] == 1:
        diff -= facilities[facility_old].setup_cost
    if dd[facility_new] == 0:
        diff += facilities[facility_new].setup_cost

    aug_cost_new += diff + aug_diff
    obj_new += diff

    return aug_cost_new, obj_new


# Tìm kiếm bước di chuyển có aug_cost tốt nhất
# @return aug_cost_new, obj_new, customer, facility
def get_move():
    global aug_cost, obj

    min_delta = float('inf')
    # tập (customer, facility) (bước di chuyển) làm delta nhỏ nhất
    min_delta_customers = []
    min_delta_facilities = []

    # duyệt qua toàn bộ cặp customer, facility để thử
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
    # chỉ di chuyển bước làm giảm aug_cost
    if min_delta < 0:
        idx = random.randrange(0, len(min_delta_customers), 1)
        customer = min_delta_customers[idx]
        facility = min_delta_facilities[idx]
        return get_cost_move(customer, facility), customer, facility
    else:
        return (0, 0), -1, -1


# thực hiện bước di chuyển tìm được
def move(aug_cost_new, obj_new, customer, facility):
    global aug_cost, obj
    aug_cost = aug_cost_new
    obj = obj_new
    dd[solution[customer]] -= 1
    dd[facility] += 1
    available[solution[customer]] += customers[customer].demand
    available[facility] -= customers[customer].demand
    solution[customer] = facility


# Cập nhật giá trị phạt với các bước di chuyển có util cao nhất
# util = features[cus][fac] / (1 + penalty[cus][fac])
def add_penalty():
    global aug_cost
    max_util = - float('inf')
    max_util_customers = []  # tập bước di chuyển có util lớn nhất
    for i in range(customer_count):
        util = features[i][solution[i]] / (1 + penalty[i][solution[i]])
        if util > max_util:
            max_util = util
            max_util_customers.clear()
            max_util_customers.append(i)
        elif util == max_util:
            max_util_customers.append(i)
    # cập nhật giá trị phạt (tăng lên 1) với mỗi bước di chuyển có util lớn nhất
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
        if customer == -1:  # không tìm được bước di chuyển tốt hơn -> restart_search
            if lamda == 0:
                lamda = init_lamda(obj, alpha)
            add_penalty()
            # reset search
            restart = restart_search(1)
            if restart == False:
                break
        else:  # tìm được bước di chuyển tốt, cập nhật bước di chuyển và kết quả tốt nhất
            move(aug_cost_new, obj_new, customer, facility)

            if best_obj > obj:
                best_obj = obj
                best_solution = list(solution)

    return best_obj, best_solution

# khởi tạo các biến của bài toán
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
    res_obj, res_solution = search(50000)

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
