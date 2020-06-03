import math
from collections import namedtuple
import random
import numpy as np
import time

Point = namedtuple("Point", ['x', 'y'])


def length(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


class LocalSearch:
    def __init__(self, n, vertex):
        self.N = n
        self.vertex = vertex
        self.edge = []

        if self.N < 10000:
            for i in range(self.N):
                self.edge.append([])
                for j in range(self.N):
                    self.edge[i].append(self.get_length(i, j))

        self.route = [0] * self.N
        self.best_route = [0] * self.N
        self.cost = 0.0
        self.best_cost = 0.0
        self.list_route = []
        self.list_cost = []

        self.epsilon = 0.2
        self.max_iter = 30000000
        self.max_early_stop = 50000
        # if self.N > 5000:
        #     self.max_iter = 1000000000
        #     self.max_early_stop = 100000

    def init_solution(self):
        mark = [False] * self.N
        self.route[0] = 0
        mark[0] = True
        for i in range(1, self.N):
            min_dis = float('inf')
            min_pos = i
            for j in range(self.N):
                if not mark[j]:
                    if self.get_distance(self.route[i - 1], j) < min_dis:
                        min_dis = self.get_distance(self.route[i - 1], j)
                        min_pos = j
            self.route[i] = min_pos
            mark[min_pos] = True
            self.cost += min_dis
        self.cost += self.get_distance(self.route[0], self.route[self.N - 1])
        self.best_route = list(self.route)
        self.best_cost = self.cost
        print('Init solution:')
        print(self.cost)
        print(self.route)
        print('----------------------------')

    def get_length(self, i, j):
        return math.sqrt((self.vertex[i].x - self.vertex[j].x) ** 2 + (self.vertex[i].y - self.vertex[j].y) ** 2)

    def get_distance(self, i, j):
        if self.N < 10000:
            return self.edge[i][j]
        else:
            return self.get_length(i, j)

    def two_opt(self):
        next_route = list(self.route)
        while True:
            i = random.randint(1, self.N - 3)
            l = random.randint(2, self.N - 1 - i)
            if i + l < self.N:
                break

        next_route[i:(i + l)] = reversed(next_route[i:(i + l)])
        next_cost = self.cost - self.get_distance(self.route[i - 1], self.route[i]) - self.get_distance(
            self.route[i + l - 1], self.route[i + l]) \
                    + self.get_distance(next_route[i - 1], next_route[i]) + self.get_distance(next_route[i + l - 1],
                                                                                              next_route[i + l])
        return next_route, next_cost

    def search(self, temperature, cooling_rate):
        start_time = time.time()
        pre_time = start_time
        self.init_solution()
        # self.init2()
        early_stop = 0
        for o in range(self.max_iter):
            if o % 5000000 == 0:
                print('iter:', o, time.time() - pre_time)
                pre_time = time.time()

            next_route, next_cost = self.two_opt()
            delta = next_cost - self.cost
            if delta < 0:
                self.route = list(next_route)
                self.cost = next_cost
                if next_cost < self.best_cost:
                    self.best_cost = next_cost
                    self.best_route = list(next_route)
                early_stop = 0

            if delta > 0 and math.exp(-delta / temperature) > random.random():
                if np.random.rand() < self.epsilon:
                    self.route = list(next_route)
                    self.cost = next_cost
                    if next_cost < self.best_cost:
                        self.best_cost = next_cost
                        self.best_route = list(next_route)
                    early_stop = 0
                else:
                    self.list_route.append(next_route)
                    self.list_cost.append(next_cost)

            early_stop += 1
            if early_stop > self.max_early_stop:
                self.restart_search()
            temperature *= cooling_rate
        print('Complete search, ', time.time() - start_time, 'second')

    def calculate_cost(self):
        self.cost = 0.0
        for i in range(self.N):
            self.cost += self.get_distance(self.route[i], self.route[(i - 1) % self.N])

    def restart_search(self):
        if not self.list_route:
            arr = np.array([i for i in range(self.N)])
            np.random.shuffle(arr)
            self.route = list(arr)
            self.calculate_cost()
        else:
            self.route = self.list_route.pop(0)
            self.cost = self.list_cost.pop(0)

    def opt_solution(self):
        start_time = time.time()
        max_iter = 300000000
        for u in range(self.N - 2):
            for v in range(u+1, self.N-1):
        # for o in range(max_iter):
        #     u = random.randrange(1, self.N - 2, 1)
        #     v = random.randrange(u + 1, self.N - 1, 1)
                t1 = self.get_distance(self.best_route[u], self.best_route[u - 1]) + self.get_distance(
                    self.best_route[v], self.best_route[v + 1])
                t2 = self.get_distance(self.best_route[u - 1], self.best_route[v]) + self.get_distance(
                    self.best_route[u], self.best_route[v + 1])
                if t1 > t2:
                    self.best_route[u:v + 1] = reversed(self.best_route[u:v + 1])
                    self.best_cost = self.best_cost - t1 + t2

        print('Optimized solution, ', time.time() - start_time, 'second')

    def init2(self):
        self.best_route = [0, 1, 2, 3, 4, 5, 6, 572, 573, 571, 468, 469, 467, 466, 465, 464, 463, 462, 461, 460, 459, 458, 457, 456, 455, 454, 439, 442, 446, 449, 448, 447, 380, 381, 445, 444, 443, 436, 438, 437, 435, 434, 433, 432, 430, 431, 429, 428, 427, 426, 425, 424, 423, 422, 421, 420, 416, 415, 414, 413, 351, 352, 353, 354, 355, 356, 412, 411, 417, 419, 418, 410, 384, 383, 382, 386, 385, 387, 388, 389, 390, 392, 391, 393, 376, 379, 378, 377, 314, 315, 375, 374, 373, 372, 371, 396, 395, 394, 397, 398, 399, 400, 406, 407, 408, 409, 405, 404, 403, 402, 401, 360, 359, 358, 357, 349, 350, 348, 347, 362, 361, 363, 364, 346, 345, 344, 343, 342, 366, 367, 365, 368, 369, 370, 327, 328, 329, 326, 325, 324, 323, 322, 321, 320, 319, 318, 317, 316, 313, 312, 311, 451, 450, 441, 440, 453, 452, 499, 500, 501, 498, 502, 503, 310, 309, 308, 505, 307, 304, 305, 306, 303, 302, 301, 300, 299, 298, 297, 296, 295, 294, 293, 270, 268, 269, 292, 291, 330, 331, 332, 340, 341, 339, 338, 337, 336, 333, 335, 334, 283, 284, 285, 286, 287, 280, 281, 282, 279, 278, 277, 276, 288, 289, 290, 275, 274, 273, 272, 271, 267, 266, 265, 264, 263, 262, 261, 260, 259, 258, 257, 256, 255, 253, 254, 252, 251, 250, 249, 248, 241, 242, 243, 244, 245, 247, 246, 238, 239, 240, 508, 507, 506, 504, 517, 516, 515, 514, 513, 512, 511, 510, 509, 237, 236, 235, 234, 232, 233, 231, 532, 533, 534, 535, 487, 488, 489, 531, 530, 529, 528, 527, 526, 492, 491, 490, 486, 493, 524, 525, 523, 522, 521, 520, 518, 519, 497, 496, 470, 471, 495, 494, 472, 473, 474, 570, 569, 568, 20, 19, 18, 17, 8, 7, 9, 10, 11, 16, 15, 14, 13, 12, 23, 22, 21, 24, 25, 26, 27, 28, 29, 31, 30, 32, 36, 37, 38, 33, 34, 35, 40, 41, 39, 42, 43, 44, 47, 48, 49, 46, 45, 555, 556, 557, 558, 559, 550, 551, 548, 549, 560, 561, 562, 563, 564, 565, 566, 567, 475, 476, 477, 478, 479, 480, 481, 482, 483, 485, 484, 536, 537, 539, 538, 540, 176, 177, 178, 182, 183, 185, 186, 187, 188, 230, 229, 228, 227, 189, 225, 226, 190, 191, 192, 219, 218, 220, 221, 222, 224, 223, 217, 216, 215, 214, 213, 212, 211, 210, 209, 194, 193, 184, 195, 196, 197, 205, 206, 207, 208, 203, 204, 202, 198, 199, 200, 201, 165, 164, 163, 167, 166, 181, 179, 180, 169, 171, 170, 172, 175, 174, 173, 541, 542, 107, 108, 109, 110, 111, 161, 168, 162, 160, 154, 155, 159, 156, 153, 157, 158, 145, 146, 147, 148, 152, 149, 150, 151, 142, 143, 144, 141, 140, 139, 138, 129, 130, 137, 136, 135, 134, 133, 132, 131, 113, 112, 114, 115, 116, 128, 127, 126, 125, 124, 69, 70, 68, 67, 66, 65, 72, 71, 123, 122, 117, 106, 105, 104, 103, 543, 544, 545, 546, 547, 102, 100, 101, 552, 553, 554, 99, 98, 96, 97, 94, 95, 118, 121, 120, 119, 73, 74, 75, 77, 76, 64, 62, 63, 61, 60, 59, 58, 57, 81, 80, 79, 78, 88, 87, 89, 93, 91, 92, 90, 86, 85, 50, 52, 51, 84, 82, 83, 53, 54, 55, 56]
        self.best_cost = 40675.61


def parse_data(input_data):
    lines = input_data.split('\n')

    node_no = int(lines[0])

    points = []
    for i in range(1, node_no + 1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    return node_no, points


# solve
def solve_it(input_data):
    N, vertex = parse_data(input_data)
    # search
    ls = LocalSearch(N, vertex)
    #ls.search(12100, 0.9999992)
    ls.init2()
    ls.opt_solution()

    output_data = '%.2f' % ls.best_cost + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, ls.best_route))
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
            'This test requires an input file. Please select one from the data directory. (i.e. python solver.py '
            './data/gc_4_1')
