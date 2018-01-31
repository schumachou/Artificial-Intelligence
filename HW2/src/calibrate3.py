#!/usr/bin/python
import time
from copy import deepcopy

def main():
    start_time = time.time()
    global n

    n = 5
    fruits = [[0, 5, 0, 5, 0],
              [1, 6, 1, 6, 1],
              [2, 7, 2, 7, 2],
              [3, 8, 3, 8, 3],
              [4, 9, 4, 9, 4]]

    coords = [[-2] * (n + 2) for i in range(n + 2)]
    for i in range(0, n):
        for index, fruit in enumerate(fruits[i]):
            if fruit == '*':
                coords[index + 1][i + 1] = -1
            else:
                coords[index + 1][i + 1] = int(fruit)

    # choice = alpha_beta_search(coords)
    choice = minimax_decision(coords)

    outfile = open('calibration.txt', 'w')
    outfile.write(str(expanded_node / (time.time() - start_time)))
    # print(expanded_node / (time.time() - start_time), file = outfile)
    outfile.close()

    print('nods/sec:', expanded_node / (time.time() - start_time))


def all_child(coords):
    children = []
    for j, col in enumerate(coords):
        for i, fruit in enumerate(col):
            if fruit != -1 and fruit != -2:
                children.append((j, i))
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
    connections = connect(coord, coords)

    apply_coords = deepcopy(coords)
    for conn in connections:
        apply_coords[conn[0]][conn[1]] = -1

    return gravity(apply_coords)


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


# def alpha_beta_search(coords):
#
#     return max_value(coords, float('-inf'), float('inf'), 0, 0)
#
#
# def max_value(coords, a, b, curr_score, depth):
#
#     global reorder, expanded_node
#     expanded_node += 1
#
#     v = float('-inf')
#     children = all_child(coords)
#
#     if depth == search_depth or len(children) == 0:
#         return curr_score
#
#     while len(children) != 0:
#
#         child = children.pop()
#
#         new_coords = apply(child, coords)
#         connections = connect(child, coords)
#
#         next_score = len(connections) ** 2
#
#         connections.remove(child)
#         while len(connections) != 0:
#             node = connections.pop()
#             children.remove(node)
#
#         score = curr_score + next_score
#
#         v = max(min_value(new_coords, a, b, score, depth + 1), v)
#
#         if v >= b: return v
#         if v > a: action = child
#         a = max(a, v)
#
#     if depth == 0:
#         return v, action
#     else:
#         return v
#
#
# def min_value(coords, a, b, curr_score, depth):
#
#     global expanded_node
#     expanded_node += 1
#
#     v = float('inf')
#     children = all_child(coords)
#
#     if depth == search_depth or len(children) == 0:
#         return curr_score
#
#     while len(children) != 0:
#
#         child = children.pop()
#         new_coords = apply(child, coords)
#         connections = connect(child, coords)
#
#         next_score = len(connections) ** 2
#
#         connections.remove(child)
#         while len(connections) != 0:
#             node = connections.pop()
#             children.remove(node)
#
#         score = curr_score - next_score
#
#         v = min(max_value(new_coords, a, b, score, depth + 1), v)
#
#         if a >= v: return v
#         b = min(b, v)
#
#     return v


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

    # global search_depth
    # repeat_children_len = []
    #
    # # estimate branch
    # children = all_child(coords)
    # estimate_branch = len(children)
    # while len(children) != 0:
    #     child = children.pop()
    #     connections = connect(child, coords)
    #     connections_len = len(connections)
    #     repeat_children_len.append(connections_len)
    #
    #     connections.remove(child)
    #     while len(connections) != 0:
    #         node = connections.pop()
    #         children.remove(node)
    #
    # for i in repeat_children_len:
    #     estimate_branch = estimate_branch - i + 1
    #
    # # evaluate search depth
    # total_children_len = estimate_branch
    # i = 1
    # while estimate_branch - i > 0 and speed * t > total_children_len * (estimate_branch - i):
    #     search_depth += 1
    #     total_children_len = total_children_len * (estimate_branch - i)
    #     i += 1

    # print('total_children_len:', total_children_len)
    # print('search_depth:', search_depth)  # tes

    return max_value(coords, float('-inf'), float('inf'), 0, 0)


def max_value(coords, a, b, curr_score, depth):

    global expanded_node
    expanded_node += 1

    v = float('-inf')
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

        score = curr_score + next_score

        v = max(min_value(new_coords, a, b, score, depth + 1), v)

        if v >= b: return v
        if v > a:
            action = child

        a = max(a, v)

    if depth == 0:
        return action
    else:
        return v


def min_value(coords, a, b, curr_score, depth):

    global expanded_node
    expanded_node += 1

    v = float('inf')
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


def minimax_decision(coords):

    v = float('-inf')
    children = all_child(coords)

    while len(children) != 0:
        child = children.pop()
        new_coords = apply(child, coords)
        connections = connect(child, coords)
        score = len(connections) ** 2

        connections.remove(child)
        while len(connections) != 0:
            node = connections.pop()
            children.remove(node)

        temp = minimax_value(new_coords, score, 0)
        if temp > v:
            v = temp
            action = child

    return action


def minimax_value(coords, curr_score, depth):

    global expanded_node
    expanded_node += 1
    depth += 1

    if depth == search_depth:
        return curr_score
    elif depth % 2 == 0:
        v = float('-inf')
        children = all_child(coords)

        while len(children) != 0:
            child = children.pop()
            new_coords = apply(child, coords)
            connections = connect(child, coords)
            next_score = len(connections) ** 2

            connections.remove(child)
            while len(connections) != 0:
                node = connections.pop()
                children.remove(node)

            score = curr_score + next_score
            temp = minimax_value(new_coords, score, depth)

            if temp > v:
                v = temp
        return v
    else:
        v = float('inf')
        children = all_child(coords)

        while len(children) != 0:
            child = children.pop()
            new_coords = apply(child, coords)
            connections = connect(child, coords)
            next_score = len(connections) ** 2

            connections.remove(child)
            while len(connections) != 0:
                node = connections.pop()
                children.remove(node)

            score = curr_score - next_score
            temp = minimax_value(new_coords, score, depth)

            if temp < v:
                v = temp
        return v


n = 0
search_depth = 4
expanded_node = 0


if __name__ == "__main__": main()