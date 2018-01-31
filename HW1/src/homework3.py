from copy import deepcopy
from collections import deque
import random
import math
import time



def main():

    global n, p, column, row, diaRight, diaLeft, house, result, queue, trees, empty, arrange

    infile = open('input.txt', 'r')
    outfile = open('output.txt', 'w')

    # # Initialize
    lines = tuple(infile)
    alg = lines[0].strip()
    n = int(lines[1])
    p = int(lines[2])

    for i in range(n):
        house.append([int(nursery) for nursery in lines[i+3].strip()])

    # # initialize queue
    for i in range(n):
        for idx, nursery in enumerate(house[i]):
            if nursery == 0:
                empty.append((i, idx))
                queue.append({(i, idx): {'placed': [],
                                         'check': {'column': [True] * n,
                                                   'row': [True] * n,
                                                   'right': [True] * (2 * n - 1),
                                                   'left': [True] * (2 * n - 1)
                                                  }
                                        }
                              })
            else:
                trees.append((i, idx))
    # print("queue:", queue) #
    # print("tree:", trees) #
    # print("empty:", empty) #

    # # randomly place lizards
    for i in range(p):
        arrange.append(empty.pop(random.randrange(0,len(empty))))
    # print("arrange:", arrange) #
    # print("empty:", empty) #

    if alg == 'BFS':
        result = bfs()
    elif alg == 'DFS':
        result = dfs()
    else:
        sa()
        if conflict(arrange) == 0:
            result = 'OK'
            for lizard in arrange:
                house[lizard[0]][lizard[1]] = 1
        else:
            result = 'FAIL'

    # print('final arrange:', arrange) #
    # print('success:', success) #

    for lizard in success:
        house[lizard[0]][lizard[1]] = 1

    print(result) #
    print(result, file = outfile)
    for row in house:
        for nursery in row:
            print(nursery, end='') #
            print(nursery, file = outfile, end = '')
        print() #
        print(file = outfile)

    infile.close()
    outfile.close()


def sa():

    global empty, arrange
    num_arrange = len(arrange)
    num_empty = len(empty)
    temperature = n**2
    rate = 0.99

    timeout = time.time() + 60 * 4
    while True:
        # print('arrange:', arrange) #

        temperature = temperature * rate
        if temperature == 0 or time.time() > timeout: return
        next_arrange = deepcopy(arrange)
        next_empty = deepcopy(empty)

        curr = conflict(arrange)
        if curr == 0: return

        print('current conflict:', curr) #

        temp = next_arrange.pop(random.randrange(0, num_arrange))

        next_arrange.append(next_empty.pop(random.randrange(0, num_empty)))
        next_empty.append(temp)
        next = conflict(next_arrange)
        print('next conflict:', next)  #

        delta = next - curr

        if delta < 0:
            arrange = deepcopy(next_arrange)
            empty = deepcopy(next_empty)
        else:
            probability = math.exp(-delta/temperature)
            if accept(probability):
                arrange = deepcopy(next_arrange)
                empty = deepcopy(next_empty)


def conflict(lizards):
    num = 0
    for i in range(p):
        for j in range(i+1, p):
            if lizards[i][0] == lizards[j][0]:
                num += 1
                for tree in trees:
                    if tree[0] == lizards[i][0]:
                        if lizards[i][1] < tree[1] < lizards[j][1] or lizards[i][1] > tree[1] > lizards[j][1]:
                            num -= 1
                            break
            elif lizards[i][1] == lizards[j][1]:
                num += 1
                for tree in trees:
                    if tree[1] == lizards[i][1]:
                        if lizards[i][0] < tree[0] < lizards[j][0] or lizards[i][0] > tree[0] > lizards[j][0]:
                            num -= 1
                            break
            elif lizards[i][0] - lizards[j][0] == lizards[i][1] - lizards[j][1]:
                num += 1
                for tree in trees:
                    if tree[0] - lizards[i][0] == tree[1] - lizards[i][1]:
                        if lizards[i][0] < tree[0] < lizards[j][0] or lizards[i][0] > tree[0] > lizards[j][0]:
                            num -= 1
                            break
            elif lizards[i][0] - lizards[j][0] == -(lizards[i][1] - lizards[j][1]):
                num += 1
                for tree in trees:
                    if tree[0] - lizards[i][0] == -(tree[1] - lizards[i][1]):
                        if lizards[i][0] < tree[0] < lizards[j][0] or lizards[i][0] > tree[0] > lizards[j][0]:
                            num -= 1
                            break
    return num


def accept(p):
    r = random.random()
    if r < p : return True
    else: return False


def dfs():
    global queue, success
    while len(queue) != 0:

        # for node in queue: #
        #     print(node) #

        coord = queue.pop()
        for k, v in coord.items():
            # print('k:', k) #
            # print('v:', v) #
            i, j = k[1], k[0]
            r = j + i
            l = j - i + n - 1

            # print('i,j,r,l:', i,j,r,l) #
            # print(v['check']['column'], v['check']['row'], v['check']['right'], v['check']['left']) #

            # # check if the popp node valid
            if check_valid(v, i, j, r, l):
                v['check']['column'][i], v['check']['row'][j], v['check']['right'][r], v['check']['left'][l] \
                    = False, False, False, False
                # print(v['check']['column'], v['check']['row'], v['check']['right'], v['check']['left'])  #

                # # add this node into close queue

                # # if the number of lizards is equal to p - 1, then success
                if len(v['placed']) == p - 1:
                    success = v['placed']
                    success.append((j, i))
                    # print('success:', success) #
                    return 'OK'

                # # add the valid children into open queue
                for x in range(n - i - 1):
                    ii, jj = x + i + 1, j
                    rr = jj + ii
                    ll = jj - ii + n - 1

                    # print('next:', (jj, ii)) #
                    # print('not tree:', (jj, ii) not in tree) #
                    # print(v['check']['column'][ii], v['check']['row'][jj], v['check']['right'][rr], v['check']['left'][ll])
                    # print('ii,jj,rr,ll:', ii, jj, rr, ll) #
                    # print(v['check']['column'], v['check']['row'], v['check']['right'], v['check']['left'])  #

                    # # if the node is a tree
                    if (jj, ii) in trees:
                        v['check']['column'][ii], v['check']['row'][jj], v['check']['right'][rr], v['check']['left'][ll] \
                            = True, True, True, True
                        continue
                    # # check if the child is valid
                    if check_valid(v, ii, jj, rr, ll):
                        curr = deepcopy(v['placed'])
                        curr.append((j, i))
                        queue.append({(jj, ii): {'placed': curr,
                                                 'check': {'column': deepcopy(v['check']['column']),
                                                           'row': deepcopy(v['check']['row']),
                                                           'right': deepcopy(v['check']['right']),
                                                           'left': deepcopy(v['check']['left'])
                                                           }
                                                 }
                                      })
                for y in range(n - j - 1):
                    for x in range(n):
                        ii, jj = x, y + j + 1
                        rr = jj + ii
                        ll = jj - ii + n - 1

                        # print('next:', (jj, ii))  #
                        # print('not tree:', (jj, ii) not in tree)  #
                        # print(v['check']['column'][ii], v['check']['row'][jj], v['check']['right'][rr],
                        #       v['check']['left'][ll])
                        # print('ii,jj,rr,ll:', ii, jj, rr, ll)  #

                        # # if the node is a tree
                        if (jj, ii) in trees:
                            v['check']['column'][ii], v['check']['row'][jj], v['check']['right'][rr], \
                            v['check']['left'][ll] \
                                = True, True, True, True
                            continue
                        # # check if the child is valid
                        if check_valid(v, ii, jj, rr, ll):
                            # q.append((jj, ii)) #
                            curr = deepcopy(v['placed'])
                            curr.append((j, i))
                            queue.append({(jj, ii): {'placed': curr,
                                                     'check': {'column': deepcopy(v['check']['column']),
                                                               'row': deepcopy(v['check']['row']),
                                                               'right': deepcopy(v['check']['right']),
                                                               'left': deepcopy(v['check']['left'])
                                                               }
                                                     }
                                          })
    if p == 0:
        return 'OK'
    else:
        return 'FAIL'


def bfs():
    global queue, success
    while len(queue) != 0:

        # for node in queue: #
        #     print(node) #

        coord = queue.popleft()
        for k, v in coord.items():
            # print('k:', k) #
            # print('v:', v) #
            i, j = k[1], k[0]
            r = j + i
            l = j - i + n - 1

            # print('i,j,r,l:', i,j,r,l) #
            # print(v['check']['column'], v['check']['row'], v['check']['right'], v['check']['left']) #

            # # check if the popp node valid
            if check_valid(v, i, j, r, l):
                v['check']['column'][i], v['check']['row'][j], v['check']['right'][r], v['check']['left'][l] \
                    = False, False, False, False
                # print(v['check']['column'], v['check']['row'], v['check']['right'], v['check']['left'])  #

                # # add this node into close queue

                # # if the number of lizards is equal to p - 1, then success
                if len(v['placed']) == p - 1:
                    success = v['placed']
                    success.append((j, i))
                    # print('success:', success) #
                    return 'OK'

                # # add the valid children into open queue
                for x in range(n - i - 1):
                    ii, jj = x + i + 1, j
                    rr = jj + ii
                    ll = jj - ii + n - 1

                    # print('next:', (jj, ii)) #
                    # print('not tree:', (jj, ii) not in tree) #
                    # print(v['check']['column'][ii], v['check']['row'][jj], v['check']['right'][rr], v['check']['left'][ll])
                    # print('ii,jj,rr,ll:', ii, jj, rr, ll) #
                    # print(v['check']['column'], v['check']['row'], v['check']['right'], v['check']['left'])  #

                    # # if the node is a tree
                    if (jj, ii) in trees:
                        v['check']['column'][ii], v['check']['row'][jj], v['check']['right'][rr], v['check']['left'][ll] \
                            = True, True, True, True
                        continue
                    # # check if the child is valid
                    if check_valid(v, ii, jj, rr, ll):
                        curr = deepcopy(v['placed'])
                        curr.append((j, i))
                        queue.append({(jj, ii): {'placed': curr,
                                                 'check': {'column': deepcopy(v['check']['column']),
                                                           'row': deepcopy(v['check']['row']),
                                                           'right': deepcopy(v['check']['right']),
                                                           'left': deepcopy(v['check']['left'])
                                                           }
                                                 }
                                      })
                for y in range(n - j - 1):
                    for x in range(n):
                        ii, jj = x, y + j + 1
                        rr = jj + ii
                        ll = jj - ii + n - 1

                        # print('next:', (jj, ii))  #
                        # print('not tree:', (jj, ii) not in tree)  #
                        # print(v['check']['column'][ii], v['check']['row'][jj], v['check']['right'][rr],
                        #       v['check']['left'][ll])
                        # print('ii,jj,rr,ll:', ii, jj, rr, ll)  #

                        # # if the node is a tree
                        if (jj, ii) in trees:
                            v['check']['column'][ii], v['check']['row'][jj], v['check']['right'][rr], v['check']['left'][ll] \
                                = True, True, True, True
                            continue
                        # # check if the child is valid
                        if check_valid(v, ii, jj, rr, ll):
                            # q.append((jj, ii)) #
                            curr = deepcopy(v['placed'])
                            curr.append((j, i))
                            queue.append({(jj, ii): {'placed': curr,
                                                     'check': {'column': deepcopy(v['check']['column']),
                                                               'row': deepcopy(v['check']['row']),
                                                               'right': deepcopy(v['check']['right']),
                                                               'left': deepcopy(v['check']['left'])
                                                               }
                                                     }
                                          })
    if p == 0:
        return 'OK'
    else:
        return 'FAIL'


def check_valid(v, i, j, r, l):
    if v['check']['column'][i] and v['check']['row'][j] and v['check']['right'][r] and v['check']['left'][l]:
        return True
    return False


n, p = 0, 0
# column, row, diaRight, diaLeft, house, queue, trees, success, empty, arrange = [], [], [], [], [], [], [], [], [], []
column, row, diaRight, diaLeft, house, queue, trees, success = deque(), deque(), deque(), deque(), deque(), deque(), deque(), deque()
empty, arrange = [], []
result = ''

if __name__ == "__main__": main()