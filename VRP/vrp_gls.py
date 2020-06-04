import math
from collections import namedtuple
import random

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])

# GLOBAL VARIABLES
customer_count = 0
vehicle_count = 0
vehicle_capacity = 0
customers = []
dis = []

# GLS parameter
# Phương pháp giải giả sử có một vehicle ảo, sức chứa vô hạn nhưng khi chở hàng bằng xe này sẽ tốn nhiều chi phí hơn
# Chi phí trên vehicle ảo: dis_virtual[i][j] = (dis[i][j] + lamda * penalty[i][j]) * alpha1 + alpha2
features = []
penalty = []
alpha1 = 1.025
alpha2 = 0
lamda = 0

available = []  # sức chứa còn lại của vehicle
vehicles = []  # lời giải
obj = 0.0
aug_cost = 0.0


def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x) ** 2 + (customer1.y - customer2.y) ** 2)


# khởi tạo các biến của bài toán
def init():
    global dis, available, features, penalty, alpha2

    dis = [[0.0 for _ in range(customer_count)] for _ in range(customer_count)]
    max_dis = -float('inf')
    for i in range(customer_count):
        for j in range(customer_count):
            dis[i][j] = length(customers[i], customers[j])
            max_dis = max(max_dis, dis[i][j])
    alpha2 = 0.0005 * max_dis
    features = [[0.0 for _ in range(customer_count)] for _ in range(customer_count)]
    penalty = [[0.0 for _ in range(customer_count)] for _ in range(customer_count)]
    available = [vehicle_capacity for _ in range(vehicle_count + 1)]


# init lamda
def init_lamda():
    global lamda

    lamda = 0.3
    return lamda


# init greedy solution
# với mỗi vehicle, chọn customer gần nhất mà vehicle đủ sức chứa cho đến khi không còn thêm được customer nào
def init_solution():
    global obj, vehicles, aug_cost
    dd = [0 for _ in range(customer_count)]
    dd[0] = 1

    for i in range(vehicle_count):
        vehicles.append([])
        vehicles[i].append(0)
        prev_idx = 0
        while True:
            min_dis = float('inf')
            min_idx = -1
            for j in range(customer_count):
                if dd[j] == 0 and available[i] >= customers[j].demand and min_dis > dis[j][prev_idx]:
                    min_dis = dis[j][prev_idx]
                    min_idx = j

            if min_idx == -1:  # không tìm được customer nào thoả mãn điều kiện sức chứa
                break
            available[i] -= customers[min_idx].demand
            vehicles[i].append(min_idx)
            dd[min_idx] = 1
            obj += min_dis
            prev_idx = min_idx
        vehicles[i].append(0)
        obj += dis[prev_idx][0]

    aug_cost = obj

    # virtual vehicle
    # các customer chưa vào vehicle nào thì vào virtual_vehicle
    vehicles.append([])
    vehicles[vehicle_count].append(0)
    prev_idx = 0
    while True:
        min_dis = float('inf')
        min_idx = -1
        for j in range(customer_count):
            if dd[j] == 0 and min_dis > dis[j][prev_idx]:
                min_dis = dis[j][prev_idx]
                min_idx = j

        if min_idx == -1:
            break
        vehicles[vehicle_count].append(min_idx)
        dd[min_idx] = 1
        obj += min_dis
        aug_cost += (min_dis + lamda * penalty[min_idx][prev_idx]) * alpha1 + alpha2
        prev_idx = min_idx
    vehicles[vehicle_count].append(0)
    obj += dis[prev_idx][0]
    aug_cost += (dis[prev_idx][0] + lamda * penalty[0][prev_idx]) * alpha1 + alpha2


# khởi động lại tìm kiếm bằng lời giải ngẫu nhiên thoả mãn ràng buộc sức chứa
def restart_search():
    print("restart search")
    global obj, vehicles, aug_cost, available

    # khởi tạo lại các giá trị liên quan đến lời giải
    available = [vehicle_capacity for _ in range(vehicle_count + 1)]
    dd = [i for i in range(1, customer_count)]
    obj = 0
    aug_cost = 0
    vehicles.clear()

    # thêm ngẫu nhiên customer vào mỗi vehicle cho đến khi vehicle không đủ sức chứa thêm customer nào nữa
    for i in range(vehicle_count):
        vehicles.append([])
        vehicles[i].append(0)
        prev_idx = 0
        while True:
            # chose one customer
            idx = -1
            if len(dd) == 0:
                break
            for _ in range(customer_count):
                random_customer = random.randrange(0, len(dd), 1)
                if available[i] >= customers[dd[random_customer]].demand:
                    idx = random_customer
                    break
            if idx == -1:
                break
            customer = dd[idx]
            available[i] -= customers[customer].demand
            vehicles[i].append(customer)
            dd = dd[:idx] + dd[idx + 1:]
            obj += dis[prev_idx][customer]
            aug_cost += dis[prev_idx][customer] + lamda * penalty[prev_idx][customer]
            prev_idx = customer

        vehicles[i].append(0)
        obj += dis[prev_idx][0]
        aug_cost += dis[prev_idx][0] + lamda * penalty[prev_idx][0]

    # virtual vehicle
    # thêm hết customer còn lại vào virtual_vehicle
    vehicles.append([])
    vehicles[vehicle_count].append(0)
    prev_idx = 0
    for i in range(len(dd)):
        vehicles[vehicle_count].append(dd[i])
        obj += dis[prev_idx][dd[i]]
        aug_cost += (dis[prev_idx][dd[i]] + lamda * penalty[prev_idx][dd[i]]) * alpha1 + alpha2
        prev_idx = dd[i]
    vehicles[vehicle_count].append(0)
    obj += dis[prev_idx][0]
    aug_cost += (dis[prev_idx][0] + lamda * penalty[0][prev_idx]) * alpha1 + alpha2


# get new cost when relocate customer_1 from vehicle_1 to vehicle_2
# tính cost và aug_cost khi thực hiện di chuyển customer_1 từ xe vehicle_1 sang vehicle_2 (gọi là di chuyển relocate)
# @return aug_cost_new, obj_new, idx_old, idx_new
# trả về cost và aug_cost mới, vị trí của customer_1 ở vehicle_1 và vị trí tốt nhất của customer_1 khi chuyển sang vehicle_2
def get_relocate_move_cost(customer_1, vehicle_1, vehicle_2):
    if available[vehicle_2] < customers[customer_1].demand:  # vi phạm điều kiện về sức chứa
        return -1, -1, -1, -1

    obj_new = obj
    aug_cost_new = aug_cost
    old_idx = -1
    # tìm vị trí của customer_1 trong xe vehicle_1
    for i in range(1, len(vehicles[vehicle_1]) - 1, 1):
        if vehicles[vehicle_1][i] == customer_1:
            old_idx = i
            break
    prev_cus = vehicles[vehicle_1][old_idx - 1]  # customer đứng trước customer_1 trong vehicle_1
    next_cus = vehicles[vehicle_1][old_idx + 1]  # customer đứng sau customer_1 trong vehicle_1

    t1 = dis[prev_cus][customer_1] + dis[customer_1][next_cus]  # lượng mất đi trong cost nếu customer_1 rời vehicle_1
    t2 = dis[prev_cus][next_cus]  # lượng thêm vào trong cost nếu customer_1 rời vehicle_1

    aug_t1 = t1 + lamda * (penalty[prev_cus][customer_1] + penalty[customer_1][next_cus])  # tương tự t1, t2 nhưng dành cho aug_cost
    aug_t2 = t2 + lamda * penalty[prev_cus][next_cus]

    if vehicle_1 == vehicle_count:  # nếu vehicle_1 là virtual_vehicle, cập nhật lại aug_cost theo công thức
        aug_t1 = aug_t1 * alpha1 + 2 * alpha2
        aug_t2 = aug_t2 * alpha1 + alpha2

    min_diff = float('inf')
    new_idx = -1
    for i in range(0, len(vehicles[vehicle_2]) - 1, 1):
        next_idx = vehicles[vehicle_2][i + 1]
        cur_idx = vehicles[vehicle_2][i]

        t1_2 = dis[next_idx][cur_idx]  # lượng mất đi trong cost nếu customer_1 được thêm vào vị trí i+1 của vehicle_2
        t2_2 = dis[cur_idx][customer_1] + dis[customer_1][next_idx]  # lượng thêm vào trong cost nếu ...

        aug_t1_2 = t1_2 + lamda * penalty[next_idx][cur_idx]  # tương tự t1_2, t2_2 nhưng cho aug_cost
        aug_t2_2 = t2_2 + lamda * (penalty[cur_idx][customer_1] + penalty[customer_1][next_idx])
        diff = aug_t2 + aug_t2_2 - aug_t1 - aug_t1_2  # tổng lượng thay đổi của aug_cost nếu di chuyển customer_1 từ vehicle_1 sang vị trí i+1 trong vehicle_2

        if diff < min_diff:
            min_diff = diff
            new_idx = i

    # cập nhật bước di chuyển tốt nhất
    aug_cost_new = aug_cost_new + min_diff
    next_idx = vehicles[vehicle_2][new_idx + 1]
    cur_idx = vehicles[vehicle_2][new_idx]
    obj_new = obj_new - dis[next_idx][cur_idx] + dis[next_idx][customer_1] + dis[cur_idx][customer_1] - t1 + t2

    return aug_cost_new, obj_new, old_idx, new_idx


# thực hiện bước di chuyển customer_1 ở vị trí old_idx trên xe vehicle_1 sang vị trí new_idx trên xe vehicle_2
# giá trị cost và aug_cost đã được tính từ trước
def relocate_move(customer_1, vehicle_1, vehicle_2, aug_cost_new, obj_new, old_idx, new_idx):
    global aug_cost, obj, vehicles, available

    aug_cost = aug_cost_new
    obj = obj_new
    vehicles[vehicle_1] = vehicles[vehicle_1][:old_idx] + vehicles[vehicle_1][old_idx + 1:]
    vehicles[vehicle_2].insert(new_idx + 1, customer_1)
    available[vehicle_1] += customers[customer_1].demand
    available[vehicle_2] -= customers[customer_1].demand


# find best move
# tìm bước di chuyển relocate tốt nhất
def get_relocate_move():
    min_delta = float('inf')
    min_vehicle_old = []
    min_vehicle_new = []
    min_customer = []

    # thử tất cả các bước di chuyển có thể
    for i in range(vehicle_count + 1):
        for customer in vehicles[i]:
            for j in range(vehicle_count):
                if j != i and customer != 0:
                    aug_cost_new, obj_new, idx_old, idx_new = get_relocate_move_cost(customer, i, j)
                    delta = aug_cost_new - aug_cost
                    if delta < min_delta and aug_cost_new > 0:
                        min_delta = delta
                        min_customer.clear()
                        min_vehicle_new.clear()
                        min_vehicle_old.clear()

                        min_customer.append(customer)
                        min_vehicle_old.append(i)
                        min_vehicle_new.append(j)
                    elif delta == min_delta and aug_cost_new > 0:
                        min_customer.append(customer)
                        min_vehicle_old.append(i)
                        min_vehicle_new.append(j)

    # nếu bước di chuyển lại giảm aug_cost
    if min_delta < 0:
        idx = random.randrange(0, len(min_customer), 1)
        customer_idx = min_customer[idx]
        vehicle_old = min_vehicle_old[idx]
        vehicle_new = min_vehicle_new[idx]
        return customer_idx, vehicle_old, vehicle_new, get_relocate_move_cost(customer_idx, vehicle_old, vehicle_new)
    else:
        return -1, -1, -1, (-1, -1, -1, -1)


# các hàm tương tự như relocate nhưng dành cho di chuyển 2opt
# get_'name'_move_cost(): lấy giá trị mục tiêu nếu như thực hiện di chuyển
# 'name'_move(): thực hiện bước di chuyển
# get_'name'_move(): tìm bước di chuyển tốt nhất
# di chuyển 2opt: đảo ngược thứ tự thăm trên vehicle_idx trong khoảng [customer_1, customer_2]
def get_2opt_move_cost(customer_1, customer_2, vehicle_idx):
    N = len(vehicles[vehicle_idx])
    u = -1
    v = -1
    for i in range(N):
        if customer_1 == vehicles[vehicle_idx][i]:
            u = i
        if customer_2 == vehicles[vehicle_idx][i]:
            v = i
    t1 = dis[customer_1][vehicles[vehicle_idx][u - 1]] + dis[customer_2][vehicles[vehicle_idx][v + 1]]
    t2 = dis[vehicles[vehicle_idx][u - 1]][customer_2] + dis[customer_1][vehicles[vehicle_idx][v + 1]]
    aug_t1 = t1 + lamda * (penalty[customer_1][vehicles[vehicle_idx][u - 1]] + penalty[customer_2][vehicles[vehicle_idx][v + 1]])
    aug_t2 = t2 + lamda * (penalty[vehicles[vehicle_idx][u - 1]][customer_2] + penalty[customer_1][vehicles[vehicle_idx][v + 1]])

    aug_cost_new = aug_cost - aug_t1 + aug_t2
    obj_new = obj - t1 + t2

    return aug_cost_new, obj_new, u, v


def _2opt_move(customer_1, customer_2, vehicle_idx, aug_cost_new, obj_new, u, v):
    global aug_cost, obj, vehicles

    aug_cost = aug_cost_new
    obj = obj_new
    vehicles[vehicle_idx][u:v + 1] = reversed(vehicles[vehicle_idx][u:v + 1])


def get_2opt_move():
    min_delta = float('inf')
    min_customer_1 = []
    min_customer_2 = []
    min_vehicle = []
    for i in range(vehicle_count):
        N = len(vehicles[i])
        for u in range(1, N - 3):
            for v in range(u + 1, N - 2):
                aug_cost_new, obj_new, _, _ = get_2opt_move_cost(vehicles[i][u], vehicles[i][v], i)
                delta = aug_cost_new - aug_cost
                if delta < min_delta and aug_cost_new > 0:
                    min_delta = delta
                    min_customer_1.clear()
                    min_customer_2.clear()
                    min_vehicle.clear()

                    min_customer_1.append(vehicles[i][u])
                    min_customer_2.append(vehicles[i][v])
                    min_vehicle.append(i)
                elif delta == min_delta and aug_cost_new > 0:
                    min_customer_1.append(vehicles[i][u])
                    min_customer_2.append(vehicles[i][v])
                    min_vehicle.append(i)
    if min_delta < 0:
        idx = random.randrange(0, len(min_customer_1), 1)
        customer_1 = min_customer_1[idx]
        customer_2 = min_customer_2[idx]
        vehicle = min_vehicle[idx]
        return customer_1, customer_2, vehicle, get_2opt_move_cost(customer_1, customer_2, vehicle)
    else:
        return -1, -1, -1, (-1, -1, -1, -1)


# di chuyển exchange
# đổi vị trí của customer_1 trong vehicle_1 với customer_2 trong vehicle_2
def get_exchange_move_cost(customer_1, customer_2, vehicle_1, vehicle_2):
    if available[vehicle_1] < customers[customer_2].demand - customers[customer_1].demand \
            or available[vehicle_2] < customers[customer_1].demand - customers[customer_2].demand:
        return -1, -1, -1, -1

    obj_new = obj
    aug_cost_new = aug_cost
    u = -1
    v = -1
    for i in range(1, len(vehicles[vehicle_1]) - 1, 1):
        if vehicles[vehicle_1][i] == customer_1:
            u = i
            break
    for i in range(1, len(vehicles[vehicle_2]) - 1, 1):
        if vehicles[vehicle_2][i] == customer_2:
            v = i
            break
    prev_u = vehicles[vehicle_1][u - 1]
    next_u = vehicles[vehicle_1][u + 1]
    prev_v = vehicles[vehicle_2][v - 1]
    next_v = vehicles[vehicle_2][v + 1]
    t1 = dis[customer_1][prev_u] + dis[customer_1][next_u] + dis[customer_2][prev_v] + dis[customer_2][next_v]
    t2 = dis[customer_2][prev_u] + dis[customer_2][next_u] + dis[customer_1][prev_v] + dis[customer_1][next_v]
    aug_t1 = t1 + lamda * (penalty[customer_1][prev_u] + penalty[customer_1][next_u] + penalty[customer_2][prev_v] +
                           penalty[customer_2][next_v])
    aug_t2 = t1 + lamda * (penalty[customer_2][prev_u] + penalty[customer_2][next_u] + penalty[customer_1][prev_v] +
                           penalty[customer_1][next_v])
    if vehicle_1 == vehicle_count:
        aug_t1 = aug_t1 * alpha1 + 4 * alpha2
    if vehicle_2 == vehicle_count:
        aug_t2 = aug_t2 * alpha1 + 4 * alpha2

    aug_cost_new = aug_cost_new - aug_t1 + aug_t2
    obj_new = obj_new - t1 + t2

    return aug_cost_new, obj_new, u, v


def exchange_move(customer_1, customer_2, vehicle_1, vehicle_2, aug_cost_new, obj_new, u, v):
    global aug_cost, obj, vehicles, available

    aug_cost = aug_cost_new
    obj = obj_new
    vehicles[vehicle_1][u] = customer_2
    vehicles[vehicle_2][v] = customer_1
    available[vehicle_1] += customers[customer_1].demand - customers[customer_2].demand
    available[vehicle_2] += customers[customer_2].demand - customers[customer_1].demand


def get_exchange_move():
    min_delta = float('inf')
    min_customer_1 = []
    min_customer_2 = []
    min_vehicle_1 = []
    min_vehicle_2 = []
    for i in range(vehicle_count + 1):
        for j in range(i):
            for u in range(1, len(vehicles[i]) - 1):
                for v in range(1, len(vehicles[j]) - 1):
                    aug_cost_new, obj_new, _, _ = get_exchange_move_cost(vehicles[i][u], vehicles[j][v], i, j)
                    delta = aug_cost_new - aug_cost
                    if delta < min_delta and aug_cost_new > 0:
                        min_delta = delta
                        min_customer_1.clear()
                        min_customer_2.clear()
                        min_vehicle_1.clear()
                        min_vehicle_2.clear()

                        min_customer_1.append(vehicles[i][u])
                        min_customer_2.append(vehicles[j][v])
                        min_vehicle_1.append(i)
                        min_vehicle_2.append(j)
                    elif delta == min_delta and aug_cost_new > 0:
                        min_customer_1.append(vehicles[i][u])
                        min_customer_2.append(vehicles[j][v])
                        min_vehicle_1.append(i)
                        min_vehicle_2.append(j)
    if min_delta < 0:
        idx = random.randrange(0, len(min_customer_1), 1)
        customer_1 = min_customer_1[idx]
        customer_2 = min_customer_2[idx]
        vehicle_1 = min_vehicle_1[idx]
        vehicle_2 = min_vehicle_2[idx]
        return customer_1, customer_2, vehicle_1, vehicle_2, get_exchange_move_cost(customer_1, customer_2, vehicle_1,
                                                                                    vehicle_2)
    else:
        return -1, -1, -1, -1, (-1, -1, -1, -1)


# di chuyển cross
# chia thứ tự thăm ở vehicle_1 và vehicle_2 thành 2 phần, lần lượt ở vị trí của customer_1 và customer_2
# ghép phần 1 của vehicle_1 với phần 2 của vehicle_2
# ghép phần 1 của vehicle_2 với phần 2 của vehicle_1
def get_cross_move_cost(customer_1, customer_2, vehicle_1, vehicle_2):
    obj_new = obj
    aug_cost_new = aug_cost
    u = -1
    v = -1
    for i in range(1, len(vehicles[vehicle_1]) - 1, 1):
        if vehicles[vehicle_1][i] == customer_1:
            u = i
            break
    for i in range(1, len(vehicles[vehicle_2]) - 1, 1):
        if vehicles[vehicle_2][i] == customer_2:
            v = i
            break

    tmp1 = vehicles[vehicle_1][u + 1:]
    tmp2 = vehicles[vehicle_2][v + 1:]
    sum1 = 0
    for i in tmp1:
        sum1 += customers[i].demand
    sum2 = 0
    for i in tmp2:
        sum2 += customers[i].demand
    if available[vehicle_1] < sum2 - sum1 or available[vehicle_2] < sum1 - sum2:
        return -1, -1, -1, -1

    next_u = vehicles[vehicle_1][u + 1]
    next_v = vehicles[vehicle_2][v + 1]
    t1 = dis[customer_1][next_u] + dis[customer_2][next_v]
    t2 = dis[customer_1][next_v] + dis[customer_2][next_u]
    aug_t1 = t1 + lamda * (penalty[customer_1][next_u] + penalty[customer_2][next_v])
    aug_t2 = t2 + lamda * (penalty[customer_1][next_v] + penalty[customer_2][next_u])
    if vehicle_1 == vehicle_count:
        aug_t1 = (dis[customer_1][next_u] + lamda * penalty[customer_1][next_u]) * alpha1 + alpha2 + \
                 dis[customer_2][next_v] + lamda * penalty[customer_2][next_v]
        aug_t2 = (dis[customer_1][next_v] + lamda * penalty[customer_1][next_v]) * alpha1 + alpha2 + \
                 dis[customer_2][next_u] + lamda * penalty[customer_2][next_u]
        for i in range(len(tmp1) - 1):
            aug_t1 += (dis[tmp1[i]][tmp1[i + 1]] + lamda * penalty[tmp1[i]][tmp1[i + 1]]) * alpha1 + alpha2
            aug_t2 += dis[tmp1[i]][tmp1[i + 1]] + lamda * penalty[tmp1[i]][tmp1[i + 1]]
        for i in range(len(tmp2) - 1):
            aug_t1 += dis[tmp2[i]][tmp2[i + 1]] + lamda * penalty[tmp2[i]][tmp2[i + 1]]
            aug_t2 += (dis[tmp2[i]][tmp2[i + 1]] + lamda * penalty[tmp2[i]][tmp2[i + 1]]) * alpha1 + alpha2

    obj_new += - t1 + t2
    aug_cost_new += - aug_t1 + aug_t2

    return aug_cost_new, obj_new, u, v


def cross_move(customer_1, customer_2, vehicle_1, vehicle_2, aug_cost_new, obj_new, u, v):
    global aug_cost, obj, vehicles, available

    aug_cost = aug_cost_new
    obj = obj_new
    tmp1 = vehicles[vehicle_1][u + 1:]
    tmp2 = vehicles[vehicle_2][v + 1:]
    vehicles[vehicle_1] = vehicles[vehicle_1][:u + 1] + tmp2
    vehicles[vehicle_2] = vehicles[vehicle_2][:v + 1] + tmp1

    sum1 = 0
    for i in tmp1:
        sum1 += customers[i].demand
    sum2 = 0
    for i in tmp2:
        sum2 += customers[i].demand
    available[vehicle_1] += sum1 - sum2
    available[vehicle_2] += sum2 - sum1


def get_cross_move():
    min_delta = float('inf')
    min_customer_1 = []
    min_customer_2 = []
    min_vehicle_1 = []
    min_vehicle_2 = []
    for i in range(vehicle_count + 1):
        for j in range(i):
            for u in range(1, len(vehicles[i]) - 1):
                for v in range(1, len(vehicles[j]) - 1):
                    aug_cost_new, obj_new, _, _ = get_cross_move_cost(vehicles[i][u], vehicles[j][v], i, j)
                    delta = aug_cost_new - aug_cost
                    if delta < min_delta and aug_cost_new > 0:
                        min_delta = delta
                        min_customer_1.clear()
                        min_customer_2.clear()
                        min_vehicle_1.clear()
                        min_vehicle_2.clear()

                        min_customer_1.append(vehicles[i][u])
                        min_customer_2.append(vehicles[j][v])
                        min_vehicle_1.append(i)
                        min_vehicle_2.append(j)
                    elif delta == min_delta and aug_cost_new > 0:
                        min_customer_1.append(vehicles[i][u])
                        min_customer_2.append(vehicles[j][v])
                        min_vehicle_1.append(i)
                        min_vehicle_2.append(j)
    if min_delta < 0:
        idx = random.randrange(0, len(min_customer_1), 1)
        customer_1 = min_customer_1[idx]
        customer_2 = min_customer_2[idx]
        vehicle_1 = min_vehicle_1[idx]
        vehicle_2 = min_vehicle_2[idx]
        return customer_1, customer_2, vehicle_1, vehicle_2, get_cross_move_cost(customer_1, customer_2, vehicle_1,
                                                                                 vehicle_2)
    else:
        return -1, -1, -1, -1, (-1, -1, -1, -1)


# choose best 1 of those move
# tìm bước di chuyển tốt nhất trong tất các các cách di chuyển trên
def get_move():
    cus_r, veh_1_r, veh_2_r, (aug_r, obj_r, u_r, v_r) = get_relocate_move()
    cus_1_o, cus_2_o, veh_o, (aug_o, obj_o, u_o, v_o) = get_2opt_move()
    cus_1_e, cus_2_e, veh_1_e, veh_2_e, (aug_e, obj_e, u_e, v_e) = get_exchange_move()
    cus_1_c, cus_2_c, veh_1_c, veh_2_c, (aug_c, obj_c, u_c, v_c) = get_cross_move()
    move_type = -1  # 1=r, 2=o, 3=e, 4=c
    min_aug = float('inf')
    if cus_r >= 0:
        min_aug = aug_r
        move_type = 1
    if aug_o < min_aug and cus_1_o >= 0:
        min_aug = aug_o
        move_type = 2
    if aug_e < min_aug and cus_1_e >= 0:
        min_aug = aug_e
        move_type = 3
    if aug_c < min_aug and cus_1_c >= 0:
        min_aug = aug_c
        move_type = 4

    if move_type == -1:
        return -1, -1, -1, -1, -1, (-1, -1, -1, -1)
    if move_type == 1:
        return 1, cus_r, 0, veh_1_r, veh_2_r, (aug_r, obj_r, u_r, v_r)
    if move_type == 2:
        return 2, cus_1_o, cus_2_o, veh_o, 0, (aug_o, obj_o, u_o, v_o)
    if move_type == 3:
        return 3, cus_1_e, cus_2_e, veh_1_e, veh_2_e, (aug_e, obj_e, u_e, v_e)
    if move_type == 4:
        return 4, cus_1_c, cus_2_c, veh_1_c, veh_2_c, (aug_c, obj_c, u_c, v_c)


# make a move
# thực hiện bước di chuyển
def move(move_type, cus_1, cus_2, veh_1, veh_2, aug_cost_new, obj_new, u, v):
    if move_type == 1:
        relocate_move(cus_1, veh_1, veh_2, aug_cost_new, obj_new, u, v)
        return
    if move_type == 2:
        _2opt_move(cus_1, cus_2, veh_1, aug_cost_new, obj_new, u, v)
        return
    if move_type == 3:
        exchange_move(cus_1, cus_2, veh_1, veh_2, aug_cost_new, obj_new, u, v)
        return
    if move_type == 4:
        cross_move(cus_1, cus_2, veh_1, veh_2, aug_cost_new, obj_new, u, v)
        return


# add penalty
# tăng giá trị phạt với features có util cao nhất
# util = dis[u][v] / (1 + penalty[u][v]) nếu u và v đứng cạnh nhau trong 1 xe
def add_penalty():
    global penalty, aug_cost

    max_util = float('inf')
    max_edge = []
    for i in range(vehicle_count + 1):
        l = len(vehicles[i])
        for j in range(1, l - 1):
            util = dis[vehicles[i][j]][vehicles[i][j - 1]] / (1 + penalty[vehicles[i][j]][vehicles[i][j - 1]])
            if max_util < util:
                max_util = util
                max_edge.clear()
                max_edge.append([vehicles[i][j], vehicles[i][j - 1]])
            elif max_util == util:
                max_edge.append([vehicles[i][j], vehicles[i][j - 1]])
    for [i, j] in max_edge:
        penalty[i][j] += 1
        penalty[j][i] += 1
        aug_cost += lamda


# search
def search(max_iter):
    global obj, lamda, aug_cost

    init_solution()
    best_obj = obj
    best_solution = list(vehicles)

    for _ in range(max_iter):
        move_type, cus_1, cus_2, veh_1, veh_2, (aug_cost_new, obj_new, u, v) = get_move()
        if move_type == -1:
            if lamda == 0:
                lamda = init_lamda()
            add_penalty()
            # restart search
            restart_search()
        else:
            move(move_type, cus_1, cus_2, veh_1, veh_2, aug_cost_new, obj_new, u, v)
            if best_obj > obj and len(vehicles[vehicle_count]) <= 2:
                best_obj = obj
                best_solution = list(vehicles)

        # print(move_type, cus_1, cus_2, veh_1, veh_2, aug_cost)
        # outputData = '%.2f' % obj + ' ' + str(0) + '\n'
        # for v in range(0, vehicle_count + 1):
        #     outputData += ' '.join([str(customer) for customer in vehicles[v]]) + '\n'
        # print(outputData)
    return best_obj, best_solution


def solve_it(input_data):
    global vehicle_count, customer_count, vehicle_capacity, customers
    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])

    for i in range(1, customer_count + 1):
        line = lines[i]
        parts = line.split()
        customers.append(Customer(i - 1, int(parts[0]), float(parts[1]), float(parts[2])))

    # the depot is always the first customer in the input
    depot = customers[0]

    init()
    # solve
    rt_obj, vehicle_tours = search(50000)

    # prepare the solution in the specified output format
    outputData = '%.2f' % rt_obj + ' ' + str(0) + '\n'
    for v in range(0, vehicle_count):
        outputData += ' '.join([str(customer) for customer in vehicle_tours[v]]) + '\n'

    return outputData


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py '
            './data/vrp_5_4_1)')
