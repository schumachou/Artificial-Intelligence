#!/usr/bin/python

import time
import math
from copy import deepcopy


def main():

    start_time = time.time()  # test
    global n, t, speed
    global search_depth, check_children

    infile = open('input_26.txt', 'r')
    outfile = open('output.txt', 'w')
    try:
        calibrationfile = open('calibration.txt', 'r')
    except IOError:
        speed = 15000
    else:
        speed = float(calibrationfile.readline())


    lines = tuple(infile)
    n = int(lines[0])
    p = int(lines[1])
    t = float(lines[2])

    # print('n = {}, p = {}, t = {}'.format(n, p, t)) # test

    fruits = []
    for i in range(3, 3 + n):
        fruits.append([fruit for fruit in lines[i].strip()])

    coords = [[-2] * (n + 2) for i in range(n + 2)]
    for i in range(0, n):
        for index, fruit in enumerate(fruits[i]):
            if fruit == '*':
                coords[index + 1][i + 1] = -1
            else:
                coords[index + 1][i + 1] = int(fruit)

    # print(coords) # test

    # choice = minimax_decision(coords)
    choice = alpha_beta_search(coords)

    if estimate_branch != 1:
        curr_t = time.time() - start_time
        # print('curr_t:', curr_t)
        print('estimate_branch:', estimate_branch)
        m = math.log(curr_t, estimate_branch) * 1.2
        next_t = math.pow(estimate_branch, (m + 1)/1.2)
        # print('next_t:', next_t)

        if curr_t + next_t < t:
            # t - (time.time() - start_time) > 150 and
            search_depth += 1
            check_children = False
            choice = alpha_beta_search(coords)


    column_mapping = dict( [(1,'A'), (2 ,'B'), (3 ,'C'), (4 ,'D'), (5 ,'E'), (6 ,'F'), (7 ,'G'), (8 ,'H'), (9 ,'I'), (10 ,'J'),\
                    (11 ,'K'), (12 ,'L'), (13 ,'M'), (14 ,'N'), (15 ,'O'), (16 ,'P'), (17 ,'Q'), (18 ,'R'), (19 ,'S'), \
                    (20 ,'T'), (21 ,'U'), (22 ,'V'), (23 ,'W'), (24 ,'X'), (25 ,'Y'), (26 ,'Z')])

    # print('{}{}'.format(column_mapping[choice[0]], choice[1])) # std ouput
    print('{}{}'.format(column_mapping[choice[0]], choice[1]), file = outfile)
    # outfile.write(str(column_mapping[choice[0]]))
    # outfile.write(str(choice[1]))
    # outfile.write('\n')

    # transfer the coordinate system
    final_coords = apply(choice, coords)
    row = [[] for i in range(n + 2)]
    for col in final_coords:
        for index, fruit in enumerate(col):
            row[index].append(fruit)

    # output the table
    for i in range(1, n+1):
        for j in range(1, n+1):
            if row[i][j] == -1:
                # print('*', end = '') # std ouput
                print('*', file = outfile, end='')
                # outfile.write('*')

            else:
                # print(row[i][j], end = '') # std ouput
                print(row[i][j], file = outfile, end='')
                # outfile.write(str(row[i][j]))
        # print() # std ouput
        print(file = outfile)
        # outfile.write('\n')

    infile.close()
    outfile.close()
    print(time.time() - start_time) # test


def all_child(coords):
    children = []
    for j, col in enumerate(coords):
        for i, fruit in enumerate(col):
            if fruit != -1 and fruit != -2:
                children.append((j,i))
    return children


def connect(coord, coords):
    connections = []
    queue = [coord]
    fruit = coords[coord[0]][coord[1]]
    while len(queue) != 0:
        node = queue.pop()
        col, row = node[0], node[1]
        if node not in connections:
            connections.append((node))
            if coords[col][row + 1] == fruit:
                queue.append((col, row + 1))
            if coords[col][row - 1] == fruit:
                queue.append((col, row - 1))
            if coords[col + 1][row] == fruit:
                queue.append((col + 1, row))
            if coords[col - 1][row] == fruit:
                queue.append((col - 1, row))
    return connections


def apply(coord, coords):
    # connections = []
    # queue = [coord]
    # fruit = coords[coord[0]][coord[1]]
    # while len(queue) != 0:
    #     node = queue.pop()
    #     col, row = node[0], node[1]
    #     if node not in connections:
    #         connections.append((node))
    #         if coords[col][row + 1] == fruit:
    #             queue.append((col, row + 1))
    #         if coords[col][row - 1] == fruit:
    #             queue.append((col, row - 1))
    #         if coords[col + 1][row] == fruit:
    #             queue.append((col + 1, row))
    #         if coords[col - 1][row] == fruit:
    #             queue.append((col - 1, row))
    connections = connect(coord, coords)


    apply_coords = deepcopy(coords)
    for conn in connections:
        apply_coords[conn[0]][conn[1]] = -1


    return gravity(apply_coords)
    # return (gravity(apply_coords), connections)
    # return (gravity(apply_coords), len(connections))

def gravity(apply_coords):

    for col in apply_coords:
        col.reverse()

    for i, col in enumerate(apply_coords):
        if -1 in col:
            while True:
                for j in range(col.index(-1) + 1, n + 1):
                    if col[j] != -1:
                        col[col.index(-1)] = col[j]
                        col[j] = -1
                        continue

                break

    for col in apply_coords:
        col.reverse()
    return apply_coords


def minimax_decision(coords):
    v = -math.inf

    children = all_child(coords)
    print('curr:', coords) #test
    print('#1:', children) #test

    while len(children) != 0:
        child = children.pop()
        # new_coords, connections = apply(child, coords)
        new_coords = apply(child, coords)
        connections = connect(child, coords)
        score = len(connections) ** 2
        print(child) # test

        connections.remove(child)
        while len(connections) != 0:
            node = connections.pop()
            children.remove(node)
        print('#2:', children) #test
        print('new:', new_coords) #test

        temp = minimax_value(new_coords, score, 0)
        print('score = {}'.format(score)) #test
        if temp > v:
            v = temp
            action = child

    return action


def minimax_value(coords, curr_score, depth):
    depth += 1
    if depth == search_depth:
        return curr_score
    elif depth % 2 == 0:
        v = -math.inf

        children = all_child(coords)
        print('curr:', coords) #test
        print('#3:', children) # test

        while len(children) != 0:
            child = children.pop()
            new_coords, connections = apply(child, coords)
            next_score = len(connections) ** 2
            print(child)  # test

            connections.remove(child)
            while len(connections) != 0:
                node = connections.pop()
                children.remove(node)
            print('#4:', children) #test
            print('new:', new_coords) #test

            score = curr_score + next_score
            print('curr + next = {} + {} = {}'.format(curr_score, next_score, score)) #test
            temp = minimax_value(new_coords, score, depth)
            # print((i, j), temp)
            if temp > v:
                v = temp
        return v
    else:
        v = math.inf

        children = all_child(coords)
        print('curr:', coords) #test
        print('#5:', children)  # test

        while len(children) != 0:
            child = children.pop()
            new_coords, connections = apply(child, coords)
            next_score = len(connections) ** 2
            print(child)  # test

            connections.remove(child)
            while len(connections) != 0:
                node = connections.pop()
                children.remove(node)
            print('#6:', children) #test
            print('new:', new_coords) #test

            score = curr_score - next_score
            print('curr + next = {} + {} = {}'.format(curr_score, next_score, score)) #test
            temp = minimax_value(new_coords, score, depth)
            # print((i, j), temp)
            if temp < v:
                v = temp
        return v


def largest_connection_coord(coords):

    max_connections_len = 0
    children = all_child(coords)
    while len(children) != 0:
        child = children.pop()
        connections = connect(child, coords)
        connections_len = len(connections)

        connections.remove(child)
        while len(connections) != 0:
            node = connections.pop()
            children.remove(node)

        if connections_len > max_connections_len:
            max_connections_len = connections_len
            largest_child = child
    return largest_child

def alpha_beta_search(coords):
    if check_children:

        global search_depth, estimate_branch
        repeat_children_len = []

        # estimate branch
        children = all_child(coords)
        estimate_branch = len(children)
        while len(children) != 0:
            child = children.pop()
            connections = connect(child, coords)
            connections_len = len(connections)
            repeat_children_len.append(connections_len)

            connections.remove(child)
            while len(connections) != 0:
                node = connections.pop()
                children.remove(node)

            # if connections_len > max_connections_len:
            #     max_connections_len = connections_len
            #     first_node = child

        for j in repeat_children_len:
            estimate_branch = estimate_branch - j + 1

        # evaluate search depth
        total_children_len = estimate_branch
        i = 1
        while estimate_branch - i > 0 and speed * t > total_children_len * (estimate_branch - i):
            search_depth += 1
            total_children_len = total_children_len * (estimate_branch - i)
            i += 1
        print('total_children_len:', total_children_len)

        ########## test #########
        total_children_len = total_children_len if estimate_branch - i < 2 else total_children_len * (estimate_branch - i - 1)
        print('total_children_len:', total_children_len)
        # search_depth += 1
        # print('search_depth:', search_depth)  # test
        ########## test #########
    print('search_depth:', search_depth)  # tes

    return max_value(coords, -math.inf, math.inf, 0, 0)

# function ALPHA-BETA-SEARCH(state) returns an action
#   v ←MAX-VALUE(state,−∞,+∞)
#   return the action in ACTIONS(state) with value v


def max_value(coords, a, b, curr_score, depth):

    # print('max:', coords, a, b, curr_score, depth)

    global reorder
    v = -math.inf
    children = all_child(coords)

    if depth == search_depth or len(children) == 0:
        return curr_score

    largest_child = largest_connection_coord(coords)
    index = children.index(largest_child)
    first = True

    while len(children) != 0:

        # if reorder:
        #     index = children.index(first_node)
        #     child = children.pop(index)
        #     print('max:',child)
        #     reorder = False
        # else:
        #     child = children.pop()
        if first:
            child = children.pop(index)
            first = False
        else:
            child = children.pop()

        new_coords = apply(child, coords)
        connections = connect(child, coords)
        next_score = len(connections) ** 2

        connections.remove(child)
        while len(connections) != 0:
            node = connections.pop()
            children.remove(node)

        score = curr_score + next_score

        v = max(min_value(new_coords, a, b, score, depth + 1), v)

        if v >= b: return v
        if v > a:
            action = child

        a = max(a, v)

    if depth == 0:
        # return v, action
        print('action:', action)
        return action
    else:
        return v

# function MAX-VALUE(state, α, β) returns a utility value
#   if TERMINAL-TEST(state) then return UTILITY(state)
#   v ← −∞
#   for each a in ACTIONS(state) do
#       v ← MAX(v, MIN-VALUE(RESULT(s,a), α, β))
#       ifv ≥ β then return v
#       α←MAX(α, v)
#   return v


def min_value(coords, a, b, curr_score, depth):

    # print('min:', coords, a, b, curr_score, depth)

    v = math.inf
    children = all_child(coords)


    if depth == search_depth or len(children) == 0:
        return curr_score

    largest_child = largest_connection_coord(coords)
    index = children.index(largest_child)
    first = True

    while len(children) != 0:

        if first:
            child = children.pop(index)
            first = False
        else:
            child = children.pop()

        new_coords = apply(child, coords)
        connections = connect(child, coords)
        next_score = len(connections) ** 2

        connections.remove(child)
        while len(connections) != 0:
            node = connections.pop()
            children.remove(node)

        score = curr_score - next_score

        v = min(max_value(new_coords, a, b, score, depth + 1), v)

        if a >= v: return v
        b = min(b, v)

    return v

# function MIN-VALUE(state, α, β) returns a utility value
#   if TERMINAL-TEST(state) then return UTILITY(state)
#   v ← +∞
#   for each a in ACTIONS(state) do
#       v ← MIN(v, MAX-VALUE(RESULT(s,a) , α, β))
#       ifv ≤ αthenreturnv
#       β ← MIN(β, v)
#   return v


n, t, speed = 0, 0, 0
search_depth = 1
reorder = True
# first_node = None
check_children = True
estimate_branch = 0


if __name__ == "__main__": main()
