from unittest import main
from sko.GA import GA
import numpy as np
from load_data import load_database
import time
import torch

start = time.perf_counter()


# query sequence
query_sequence_list = [
    'KJXXJAJKPXKJJXJKPXKJXXJAJKPXKJJXJKPXKJXXJAJKPXKJXXJAJKHXKJXXJAJKPXKJXXJAJKHXKJXX',
    'ILOTGJJLABWTSTGGONXJMUTUXSJHKWJHCTOQHWGAGIWLZHWPKZULJTZWAKBWHXMIKLZJGLXBPAHOHVOLZWOSJJLPO',
    'IHKKKRKKKKKKXGWGKKKPKSKKKKKBKKKPKHKKXKKBSKKPKWKKLKSKRKKWXKPKKBKKKPKTSKHKKKKLADKKYPKKKOPHKKBWWLPPWKK',
    'MPPPJPXPGPJPPPXPPPJPJPPPXPPPPSPPJJJPPXXPPPPPJPPPXPPXIPJMMMXPKPSVGULMHHZPAWHTHKAAHHUPAONAPJSWPPJGA',
    'IPPVKBKXWXKHSAPHVXXVOJMRAKKPJVLLJBWKOLLJKXHGXLLCPAJOBKPGXBATGXMPOMCVZTAXVPAGKXGOMJQOLJGWGKXLQ'
]

# database sequence
database_sequence_list = load_database()


# test sequences and standard form to GA
# test_seq1 = 'KJXXJAJKPXKJJXJKPXKJXXJAJKPXKJJXJKPXKJXXJAJKPXKJXXJAJKHXKJXXJAJKPXKJXXJAJKHXKJXX'
# test_seq2 = 'KJOBLLXJKJPLUWGWOMOLIJBJALTUKLVLJSBHGBPGWSYKJBSVJSPMZJOWUWWP'
# standard form :
# eg:
#   seq1: KJXXJAJKP
#   seq2: KJOBL
# =>
#   seq1: [K,J,X,X,J,A,J,K,P,-,-,-,-,-]
#   seq2: [-,-,-,-,-,-,-,-,-,K,J,O,B,L]
# =>
#   seq1: [0,0,0,0,0,0,0,0,0,1,1,1,1,1]
#   seq2: [1,1,1,1,1,1,1,1,1,0,0,0,0,0]
# gap_num1 = len(test_seq2)
# gap_num2 = len(test_seq1)
# =>
#   p = [0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0]


# obj fun
def obj_func(p):
    p = p.reshape(2, int(len(p)/2))
    x1 = list(p[0])
    x2 = list(p[1])
    #print(x1, x2)
    cost = cost_cal(x1, x2)
    return cost

# Fitness fun: cost calculate
# MATCH: 0
# GAP: 3
# MISMATCH: 4


def cost_cal(x1, x2):
    cost = 0
    seq1_gap_num = 0
    seq2_gap_num = 0
    for i in range(0, (len(x1))):
        if (i-seq1_gap_num) >= len(query_sequence) or (i-seq2_gap_num) >= len(database_sequence):
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
        if query_sequence[i-seq1_gap_num] != database_sequence[i-seq2_gap_num]:
            cost += 4
            continue
    return cost


# constraint_eq
# keep the number of gaps and elements
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
    print(x2.count(1)-gap_num2)
    if x2.count(1)-gap_num2 != 0:
        print('no')

    return seq1_eq + seq2_eq


# keep (constraint_eq[0] == 0)
constraint_eq = [
    constraint1
]

# func: obj func
# n_dim: dimension of obj func
# prob_mut: probability of mutation
# size_pop: size of population
# max_iter: maximum of iterations
# lb: minimum value of each elements
# ub: maximum value of each elements
# precision: accuracy of elements
# constraint_eq: equality of constraint
# ga = GA(func=obj_func, n_dim=2*(len(query_sequence)+len(database_sequence)), prob_mut=0, size_pop=50,
#        max_iter=500, lb=0, ub=1, precision=1, constraint_eq=constraint_eq)

# GA run
# best_x: best result of obj(seq1+seq2)
# best_y: best result of obj func value(cost)
#best_x, best_y = ga.run()
#print('best_x:', best_x, '\n', 'best_y:', best_y)
#best_x = best_x.reshape(2, int(len(query_sequence)+len(database_sequence)))
# print(best_x)


# argument : result
# result = [seq1,seq2]
# return = [result_seq1,result_seq2]
def print_results(result1, result2, query_sequence, database_sequence):
    x1, x2 = result1, result2
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
            result_seq1 += query_sequence[i-gap1]
        elif x1[i] == 1:
            result_seq1 += '-'
            gap1 += 1
        if x2[i] == 0:
            result_seq2 += database_sequence[i-gap2]
        elif x2[i] == 1:
            result_seq2 += '-'
            gap2 += 1
    print(result_seq1)
    print(result_seq2)


fin_result = []


for j in range(len(query_sequence_list)):
    least_cost = 999999999999999999999999999999
    least_cost_records = [0, 0, 0]
    query_sequence = query_sequence_list[j]
    print('current query sequence: ', query_sequence)
    for i in range(len(database_sequence_list)):
        database_sequence = database_sequence_list[i]
        print('current database sequence: ', database_sequence)
        gap_num1 = len(database_sequence)
        gap_num2 = len(query_sequence)
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        ga = GA(func=obj_func, n_dim=2*(len(query_sequence)+len(database_sequence)), prob_mut=0, size_pop=50,
                max_iter=100, lb=0, ub=1, precision=1, constraint_eq=constraint_eq)
        ga.to(device=device)
        best_x, best_y = ga.run()
        best_x = best_x.reshape(
            2, int(len(query_sequence)+len(database_sequence)))
        print('best_y:', best_y[0])
        if best_y < least_cost:
            least_cost = best_y[0]
            # database sequence position
            least_cost_records[0] = i
            # database sequence result
            least_cost_records[1] = best_x
            # database sequence cost
            least_cost_records[2] = least_cost
    fin_result.append(least_cost_records)
    print(least_cost_records)
print(fin_result)
print('########################################################')


for j in range(len(query_sequence_list)):
    query_sequence = query_sequence_list[j]
    database_sequence = database_sequence_list[fin_result[j][0]]
    print(fin_result[j][1])
    result1 = fin_result[j][1][0]
    result2 = fin_result[j][1][1]
    print_results(result1, result2, query_sequence,
                  database_sequence)
    print('cost:', fin_result[j][2])
    print('########################################################')


end = time.perf_counter()
print('########################################################')
print('run time: ', round(end-start), 'seconds')
