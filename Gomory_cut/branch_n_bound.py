import copy
from fractions import Fraction
from math import floor


class Gomory:
    # init
    def __init__(self, A, b, c, d):
        self.M = len(b)
        self.N = len(c)
        self.A = A
        self.b = b
        self.c = c
        self.d = d
        for i in range(100):
            self.d.append(0)

        self.a = [[Fraction(0) for i in range(self.M + self.N + 1)] for j in range(self.M + 2)]
        self.basis = [(self.N + i) for i in range(self.M)]
        self.basis_num = self.M
        self.gomory_var = self.N

        # a[i][j] = A[i][j]
        for i in range(self.M):
            for j in range(self.N):
                self.a[i][j] = Fraction(self.A[i][j])

        # artificial variables
        for i in range(self.M):
            self.a[i][self.N + i] = Fraction(1)
            self.a[self.M][self.N + i] = Fraction(-1)

        # b
        for i in range(self.M):
            self.a[i][self.M + self.N] = Fraction(b[i])

        # add objective function as an equation in row M + 1
        for i in range(self.N):
            self.a[self.M + 1][i] = Fraction(-c[i])

        # add phase 1 objective in row M
        for j in range(self.M + self.N + 1):
            for i in range(self.M):
                self.a[self.M][j] += self.a[i][j]
            self.a[self.M][j] = -self.a[self.M][j]

    # -----------  pivoting ---------------------
    # select pivot column by finding the most negative indicator (a[M][0, N + M])
    def select_pivot_col(self):
        col = -1
        min_negative = 0
        # self.N + self.M
        for i in range(0, len(self.a[0]) - 1):
            if self.a[self.basis_num][i] < 0 and self.a[self.basis_num][i] < min_negative:
                min_negative = self.a[self.basis_num][i]
                col = i
        return col

    # select pivot row after selected a pivot column
    # min positive a[i][M+N] / a[i][col] when a[i][col] > 0
    def select_pivot_row(self, col):
        row = -1
        min_positive = Fraction(100000)
        for i in range(self.basis_num):
            if self.a[i][col] > 0:
                temp = Fraction(self.a[i][len(self.a[i]) - 1], self.a[i][col])
                if temp < min_positive:
                    min_positive = temp
                    row = i
        return row

    def pivot(self, row, col):
        # pivot row
        pivot_val = self.a[row][col]

        # other row
        for i in range(self.basis_num + 2):
            if i != row:
                coef = Fraction(-self.a[i][col], pivot_val)
                for j in range(len(self.a[i])):
                    self.a[i][j] = self.a[i][j] + coef * self.a[row][j]

        for i in range(len(self.a[row])):
            self.a[row][i] = self.a[row][i] / pivot_val

        self.basis[row] = col

    # -------------- two phase simplex -------------------
    def phase_one(self):
        print('Phase 1:')
        while True:
            self.print_a()
            col = self.select_pivot_col()
            if col < 0:
                break
            row = self.select_pivot_row(col)
            if row < 0:
                break
            print("Pivot:", row, col)
            self.pivot(row, col)

        # remove artificial variables
        pop_list = []
        for i in range(len(self.basis)):
            if self.basis[i] >= self.N:
                if self.a[i][self.M + self.N] != 0:
                    return False
                    break
                else:
                    remove = True
                    for j in range(self.N):
                        if self.a[i][j] != 0:
                            self.pivot(i, j)
                            remove = False
                            break
                    if remove:
                        pop_list.append(i)

        pop_list.sort(reverse=True)
        for i in range(len(pop_list)):
            self.basis.pop(pop_list[i])
            self.basis_num -= 1
            self.a.pop(pop_list[i])

        return True

    def init_phase_two(self):
        # check feasible solution or not
        temp = self.a[self.basis_num]
        self.a[self.basis_num] = self.a[self.basis_num + 1]
        self.a[self.basis_num + 1] = temp
        for i in range(self.basis_num + 2):
            for j in range(self.N + self.M - 1, self.N - 1, -1):
                # self.a[i][j] = Fraction(0)
                self.a[i].pop(j)

    def phase_two(self):
        print('=========================================\n\nPhase 2:')
        while True:
            self.print_a()
            col = self.select_pivot_col()
            if col < 0:
                break
            row = self.select_pivot_row(col)
            if row < 0:
                break
            print("pivot:", row, col)
            self.pivot(row, col)

    def two_phase_simplex(self):
        check = self.phase_one()
        if not check:
            print("No solution")
            return
        self.init_phase_two()
        self.phase_two()
        print('Simplex solution:')
        self.print_result()

    # -------------- dual simplex ----------------------
    def dual_simplex(self):
        row = self.select_pivot_row_dual()
        if row < 0:
            return False

        print('pivot', row, end=' ')
        col = self.select_pivot_col_dual(row)
        if col < 0:
            return False
        self.pivot(row, col)
        print(col)
        self.print_a()
        return True

    def select_pivot_row_dual(self):
        row = -1
        min_negative = 0
        for i in range(self.basis_num):
            if self.a[i][len(self.a[i]) - 1] < 0 and self.a[i][len(self.a[i]) - 1] < min_negative:
                min_negative = self.a[i][len(self.a[i]) - 1]
                row = i
        return row

    def select_pivot_col_dual(self, row):
        col = -1
        min_positive = Fraction(10000)
        for i in range(len(self.a[row]) - 1):
            if self.a[row][i] < 0:
                temp = Fraction(-self.a[self.basis_num][i], self.a[row][i])
                if min_positive > temp:
                    min_positive = temp
                    col = i
        return col

    # -------- print --------------------
    def print_result(self):
        print('Optimal function: ', end='')
        cnt = 0
        for i in range(self.N):
            if self.c[i] != 0:
                if cnt > 0:
                    print(' + ', end='')
                print(str(self.c[i]) + ' * x[' + str(i + 1) + ']', end='')
                cnt += 1
        print()
        print('Optimal value = ', self.a[self.basis_num][len(self.a[0]) - 1])

        print('Result: ')
        res = [0] * self.N
        for i in range(self.basis_num):
            if self.basis[i] < self.N:
                res[self.basis[i]] = self.a[i][len(self.a[0]) - 1]
        for i in range(self.N):
            print('x[' + str(i + 1) + '] =', res[i])
        print('****************************')

    def print_a(self):
        for i in range(len(self.a)):
            if i < len(self.basis):
                print(self.basis[i] + 1, '| ', end='')
            else:
                print('    ', end='')
            for j in range(len(self.a[i])):
                leng = len(str(self.a[i][j]))
                print(self.a[i][j], (8 - leng) * ' ', end='')
            print()
        print("-------------------------------------------")

    # --------------- branch and bound ---------------------
    def pivot_bnb(self, row, col, simplex_table, basis, basis_num):
        # pivot row
        pivot_val = simplex_table[row][col]

        # other row
        for i in range(basis_num + 2):
            if i != row:
                coef = Fraction(-simplex_table[i][col], pivot_val)
                for j in range(len(simplex_table[i])):
                    simplex_table[i][j] = simplex_table[i][j] + coef * simplex_table[row][j]

        for i in range(len(simplex_table[row])):
            simplex_table[row][i] = simplex_table[row][i] / pivot_val

        basis[row] = col

    def dual_simplex_bnb(self, simplex_table, basis, basis_num):
        row = self.select_pivot_row_dual_bnb(simplex_table, basis_num)
        if row < 0:
            return False

        print('pivot', row, end=' ')
        col = self.select_pivot_col_dual_bnb(row, simplex_table, basis_num)
        if col < 0:
            return False
        self.pivot_bnb(row, col, simplex_table, basis, basis_num)
        print(col)
        self.print_simplex_table(simplex_table, basis, basis_num)
        return True

    def select_pivot_row_dual_bnb(self, simplex_table, basis_num):
        row = -1
        min_negative = 0
        for i in range(basis_num):
            if simplex_table[i][len(simplex_table[i]) - 1] < 0 and simplex_table[i][len(simplex_table[i]) - 1] < min_negative:
                min_negative = simplex_table[i][len(simplex_table[i]) - 1]
                row = i
        return row

    def select_pivot_col_dual_bnb(self, row, simplex_table, basis_num):
        col = -1
        min_positive = Fraction(10000)
        for i in range(len(simplex_table[row]) - 1):
            if simplex_table[row][i] < 0:
                temp = Fraction(-simplex_table[basis_num][i], simplex_table[row][i])
                if min_positive > temp:
                    min_positive = temp
                    col = i
        return col

    def bnb(self, simplex_table, basis, basis_num, bnb_var):
        # self.print_simplex_table(simplex_table, basis, basis_num)

        value = -1
        idx = -1
        for i in range(basis_num):
            if simplex_table[i][len(simplex_table[i]) - 1].denominator != 1 and self.d[basis[i]] == 1:
                value = int(simplex_table[i][len(simplex_table[i]) - 1])
                idx = i
                break

        if idx == -1:
            return simplex_table, basis, basis_num, simplex_table[basis_num][len(simplex_table[0]) - 1], 0

        simplex_table1 = copy.deepcopy(simplex_table)
        basis_num1 = basis_num
        basis1 = copy.deepcopy(basis)
        bnb_var1 = bnb_var

        simplex_table2 = copy.deepcopy(simplex_table)
        basis_num2 = basis_num
        basis2 = copy.deepcopy(basis)
        bnb_var2 = bnb_var

        # branch 1: x[i] <= value
        l = len(simplex_table1[idx])
        new_row1 = [Fraction(0) for _ in range(l + 1)]
        new_row1[basis1[idx]] = Fraction(1)
        new_row1[l - 1] = Fraction(1)
        new_row1[l] = Fraction(value)
        for j in range(basis_num1 + 1):
            simplex_table1[j].insert(l - 1, Fraction(0))
        for j in range(l+1):
            new_row1[j] = new_row1[j] - simplex_table1[idx][j]
        simplex_table1.insert(basis_num1, new_row1)
        basis1.append(bnb_var1)
        bnb_var1 += 1
        basis_num1 += 1

        print("add x[", basis1[idx], "] <=", value)
        self.print_simplex_table(simplex_table1, basis1, basis_num1)
        ok1 = self.dual_simplex_bnb(simplex_table1, basis1, basis_num1)
        obj1 = -1000000000
        st_1 = []
        bs_1 = []
        bsn_1 = 0
        done_1 = 0
        if ok1:
            st_1, bs_1, bsn_1, obj1, done_1 = self.bnb(simplex_table1, basis1, basis_num1, bnb_var1)

        # branch 2: x[i] >= value + 1

        l = len(simplex_table2[idx])
        new_row2 = [Fraction(0) for _ in range(l + 1)]
        new_row2[basis2[idx]] = Fraction(1)
        new_row2[l - 1] = Fraction(-1)
        new_row2[l] = Fraction(value + 1)
        for j in range(basis_num2 + 1):
            simplex_table2[j].insert(l - 1, Fraction(0))
        for j in range(l+1):
            new_row2[j] = simplex_table2[idx][j] - new_row2[j]
        simplex_table2.insert(basis_num2, new_row2)
        basis2.append(bnb_var2)
        bnb_var2 += 1
        basis_num2 += 1

        print("add x[", basis2[idx], "] >=", value+1)
        self.print_simplex_table(simplex_table2, basis2, basis_num2)

        ok2 = self.dual_simplex_bnb(simplex_table2, basis2, basis_num2)
        obj2 = -1000000000
        st_2 = []
        bs_2 = []
        bsn_2 = 0
        done_2 = 0
        if ok2:
            st_2, bs_2, bsn_2, obj2, done_2 = self.bnb(simplex_table2, basis2, basis_num2, bnb_var2)

        if obj1 > obj2 and obj1 != -1000000000:
            return st_1, bs_1, bsn_1, obj1, done_1
        elif obj2 != -1000000000:
            return st_2, bs_2, bsn_2, obj2, done_2

        return simplex_table, basis, basis_num, simplex_table[basis_num][len(simplex_table[0]) - 1], -1

    def run_bnb(self):
        self.two_phase_simplex()

        simplex_table = copy.deepcopy(self.a)
        basis = copy.deepcopy(self.basis)
        basis_num = self.basis_num
        bnb_var = self.N
        rs_st = []
        rs_bs = []
        rs_bsn = 0
        rs_obj = 0
        rs_done = -1
        rs_st, rs_bs, rs_bsn, rs_obj, rs_done = self.bnb(simplex_table, basis, basis_num, bnb_var)
        if rs_done == 0:
            self.print_result_bnb(rs_st, rs_bs, rs_bsn)
        else:
            print("no solution")

    def print_result_bnb(self, simplex_table, basis, basis_num):
        print('Optimal function: ', end='')
        cnt = 0
        for i in range(self.N):
            if self.c[i] != 0:
                if cnt > 0:
                    print(' + ', end='')
                print(str(self.c[i]) + ' * x[' + str(i + 1) + ']', end='')
                cnt += 1
        print()
        print('Optimal value = ', simplex_table[basis_num][len(simplex_table[0]) - 1])

        print('Result: ')
        res = [0] * self.N
        for i in range(basis_num):
            if basis[i] < self.N:
                res[basis[i]] = simplex_table[i][len(simplex_table[i]) - 1]
        for i in range(self.N):
            print('x[' + str(i + 1) + '] =', res[i])
        print('****************************')

    def print_simplex_table(self, simplex_table, basis, basis_num):
        for i in range(len(simplex_table)):
            if i < len(basis):
                print(basis[i] + 1, '| ', end='')
            else:
                print('    ', end='')
            for j in range(len(simplex_table[i])):
                leng = len(str(simplex_table[i][j]))
                print(simplex_table[i][j], (8 - leng) * ' ', end='')
            print()
        print("-------------------------------------------")


if __name__ == '__main__':
    # A = [
    #     [2, 1],
    #     [2, 3]
    # ]
    # b = [8, 12]
    # c = [3, 1]

    # A = [
    #     [2, 1, 0],
    #     [2, -1, 1]
    # ]
    # b = [2, 5]
    # c = [3, 2, 4]

    # A = [
    #     [3, 2, 1,1,0,0],
    #     [2, 3, 3,0,1,0],
    #     [1, 1, -1,0,0,1]
    # ]
    # b = [10, 15, 4]
    # c = [2, 3, 4,0,0,0]

    # c = [-2,-1, -1, 0,0]
    # A = [
    #     [1,1,1,1,1],
    #     [1,1,2,2,2],
    #     [1,1,0,0,0],
    #     [0,0,1,1,1]
    # ]
    # b = [5,8,2,3]

    A = [
        [3,2,1,0],
        [-3,2,0,1]
    ]
    b=[6,0]
    c=[0,1,0,0]
    d = [1,1,1,1]

    # A = [
    #     [1,1,-1,0,0],
    #     [2,-1,0,-1,0],
    #     [0,3,0,0,1]
    # ]
    # b = [1,1,2]
    # c = [-6, -3, 0,0,0]
    # d = [1,1,1,1,1]

    # A = [
    #     [5,15,1,0,0],
    #     [4,4,0,1,0],
    #     [35,20,0,0,1]
    # ]
    # b = [480, 160, 1190]
    # c = [13,23,0,0,0]
    # d = [1,1,1,1,1]

    # A = [
    #     [2, 1, -1, 0],
    #     [1, 7, 0, -1]
    # ]
    # b = [4, 7]
    # c = [-1, -1, 0, 0]
    # d = [1, 1, 1, 0]

    # A = [
    #     [Fraction(4,100), Fraction(6, 100), Fraction(5, 100), 1],
    #     [Fraction(7, 100), 0, Fraction(2, 100), 1]
    # ]
    # b = [500, 300]
    # c = [3, 2, Fraction(5, 2), 0]
    # d = [1, 1, 0, 0]

    gomory = Gomory(A, b, c, d)
    gomory.run_bnb()
