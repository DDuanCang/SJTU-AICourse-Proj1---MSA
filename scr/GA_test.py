'''
min seq1:seq2
fitness
    seq1:seq2 => match = 0、mismatch = 4、gap = 3
s.t.
    x1*x2 >= 1
    x1*x2 <= 5
    x2 + x3 = 1
    0 <= x1, x2, x3 <= 5
'''

# test data
from sko.DE import GA
import numpy as np

#test_sequence_1 = 'KJXXJAJKPXKJJXJKPXKJXXJAJKPXKJJXJKPXKJXXJAJKPXKJXXJAJKHXKJXXJAJKPXKJXXJAJKHXKJXX'
#test_sequence_2 = 'KJOBLLXJKJPLUWGWOMOLIJBJALTUKLVLJSBHGBPGWSYKJBSVJSPMZJOWUWWP'

'''
test:
test_seq1:'KJXXJAJKP'
test_seq2:'KJOBL'
seq1 = 'KJXXJAJKP_____'
seq1 = [0,0,0,0,0,0,0,0,0,1,1,1,1,1]
seq2 = '_________KJOBL'
seq2 = [1,1,1,1,1,1,1,1,1,0,0,0,0,0]
'''
test_seq1 = 'KJXXJAJKP'
test_seq2 = 'KJOBL'

test_seq1 = 'KJXXJAJKPXKJJXJKPXKJXXJAJKPXKJJXJKPXKJXXJAJKPXKJXXJAJKHXKJXXJAJKPXKJXXJAJKHXKJXX'
test_seq2 = 'KJOBLLXJKJPLUWGWOMOLIJBJALTUKLVLJSBHGBPGWSYKJBSVJSPMZJOWUWWP'

gap_num1 = len(test_seq2)
gap_num2 = len(test_seq1)
print('GAP:', gap_num1, gap_num2)


def obj_func(p):
    p = p.reshape(2, int(len(p)/2))
    x1 = list(p[0])
    x2 = list(p[1])
    #print(x1, x2)
    cost = cost_cal(x1, x2)
    return cost


def cost_cal(x1, x2):
    cost = 0
    seq1_gap_num = 0
    seq2_gap_num = 0
    for i in range(0, (len(x1))):
        # seq1 GAP
        # print(i)
        # print(x1)
        # print(x2)
        #print('gap:', seq1_gap_num, seq2_gap_num)
        #print('cost', cost)
        #print(i - seq1_gap_num, i-seq2_gap_num)
        if (i-seq1_gap_num) >= len(test_seq1) or (i-seq2_gap_num) >= len(test_seq2):
            return 4 * len(x1)
        if x1[i] == 1:
            if x2[i] == 1:
                seq1_gap_num += 1
                seq2_gap_num += 1
                continue
            cost += 3
            seq1_gap_num += 1
            continue
        # seq2 GAP
        if x2[i] == 1:
            cost += 3
            seq2_gap_num += 1
            continue
        # NO GAP
        if test_seq1[i-seq1_gap_num] != test_seq2[i-seq2_gap_num]:
            cost += 4
            continue
    return cost


def constraint1(p):
    p = p.reshape(2, int(len(p)/2))
    x1, x2 = list(p[0]), list(p[1])
    seq1_GAP_count = 0
    seq2_GAP_count = 0
    for i in range(len(x1)):
        seq1_GAP_count += x1[i]
    if (seq1_GAP_count - gap_num1) == 0:
        seq1_eq = 0
    else:
        seq1_eq = 1
    for i in range(len(x2)):
        seq2_GAP_count += x2[i]
    if (seq2_GAP_count - gap_num2) == 0:
        seq2_eq = 0
    else:
        seq2_eq = 1
    return seq1_eq + seq2_eq


constraint_eq = [
    constraint1
]


ga = GA(func=obj_func, n_dim=2*(len(test_seq1)+len(test_seq2)), prob_mut=0, size_pop=50,
        max_iter=500, lb=0, ub=1, precision=1, constraint_eq=constraint_eq)

best_x, best_y = ga.run()
print('best_x:', best_x, '\n', 'best_y:', best_y)
best_x = best_x.reshape(2, int(len(test_seq1)+len(test_seq2)))
print(best_x)


def print_results(result):
    x1, x2 = result[0], result[1]
    result_seq1 = ''
    result_seq2 = ''
    gap1 = 0
    gap2 = 0
    for i in range(len(x1)):
        if x1[i] == 1 and x2[i] == 1:
            gap1 += 1
            gap2 += 1
            continue
        if x1[i] == 0:
            result_seq1 += test_seq1[i-gap1]
        elif x1[i] == 1:
            result_seq1 += '-'
            gap1 += 1
        if x2[i] == 0:
            result_seq2 += test_seq2[i-gap2]
        elif x2[i] == 1:
            result_seq2 += '-'
            gap2 += 1
    return result_seq1, result_seq2


result_seq1, result_seq2 = print_results(best_x)
print('################################################################')
print(result_seq1)
print(result_seq2)
print('################################################################')
