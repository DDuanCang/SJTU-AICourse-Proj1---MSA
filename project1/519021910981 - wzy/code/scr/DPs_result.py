from score_matrix_get import score_matrix_get
from score_matrix_fill import score_matrix_fill
from score_matrix_A import score_matrix_A
from load_data import load_database
import time


def get_result(filled_array, form):
    length = form['length']
    depth = form['depth']
    # tree = score_tree_node.score_tree_node(filled_array[depth-1][length-1][0])
    # current_node = tree
    result1 = []
    result2 = []

    while (filled_array[depth-1][length-1][1] != 0):
        if filled_array[depth-1][length-1][1] == 1 or filled_array[depth-1][length-1][1] == 4 or filled_array[depth-1][length-1][1] == 6 or filled_array[depth-1][length-1][1] == 9:
            result1.append(length-1)
            result2.append(-1)
            length -= 1
            depth = depth

        if filled_array[depth-1][length-1][1] == 3 or filled_array[depth-1][length-1][1] == 8:
            result1.append(length-1)
            result2.append(depth-1)
            length -= 1
            depth -= 1

        if filled_array[depth-1][length-1][1] == 5:
            result1.append(-1)
            result2.append(depth-1)
            length = length
            depth -= 1

    return result1, result2


def print_sequence(a1, a2, origin_seq1, origin_seq2):
    b1 = ''
    b2 = ''
    for i in range(max(len(a1), len(a2))):
        if a1[i] == -1:
            letter1 = '_'
        else:
            letter1 = origin_seq1[a1[i]-1]
        if a2[i] == -1:
            letter2 = '_'
        else:
            letter2 = origin_seq2[a2[i]-1]
        b1 += letter1
        b2 += letter2
    return b1, b2


start = time.perf_counter()


query_sequences_list = ['IPZJJLMLTKJULOSTKTJOGLKJOBLTXGKTPLUWWKOMOYJBGALJUKLGLOSVHWBPGWSLUKOBSOPLOOKUKSARPPJ',
                        'IWTJBGTJGJTWGBJTPKHAXHAGJJSJJPPJAPJHJHJHJHJHJHJHJHJPKSTJJUWXHGPHGALKLPJTPJPGVXPLBJHHJPKWPPDJSG']

# database sequence
database_sequence = load_database()


least_cost = len(query_sequences_list[0]) * 4
least_cost_records = [0, 0]
fin_reasult = []


query_sequence1 = query_sequences_list[0]
query_sequence2 = query_sequences_list[1]
least_cost = 9999999999999999999999999999999999
least_cost_records = [0, 0]
for i in range(len(database_sequence)):
    test1, form1 = score_matrix_get(
        query_sequence1, database_sequence[i], 'init')
    test_filled1 = score_matrix_fill(
        test1, form1['length'], form1['depth'], query_sequence1, database_sequence[i])
    cost1 = test_filled1[-1][-1][0]
    test2, form2 = score_matrix_get(
        query_sequence2, database_sequence[i], 'init')
    test_filled2 = score_matrix_fill(
        test2, form2['length'], form2['depth'], query_sequence2, database_sequence[i])
    cost2 = test_filled2[-1][-1][0]
    if least_cost > cost1 + cost2:
        least_cost_records[0] = i
        least_cost_records[1] = [test_filled1[-1]
                                 [-1][0], test_filled2[-1][-1][0]]
        #least_cost_records.append([i, test_filled[-1][-1][0]])
        least_cost = cost1 + cost2
print(least_cost_records)
fin_reasult.append(least_cost_records)
print(fin_reasult)
print('#############################################################################################')


database_sequence = database_sequence[fin_reasult[0][0]]
test1, form1 = score_matrix_get(
    query_sequence1, database_sequence, 'init')
test_filled1 = score_matrix_fill(
    test1, form1['length'], form1['depth'], query_sequence1, database_sequence)
test2, form2 = score_matrix_get(
    query_sequence2, database_sequence, 'init')
test_filled2 = score_matrix_fill(
    test2, form2['length'], form2['depth'], query_sequence2, database_sequence)
seq1, seq2 = get_result(test_filled1, form1)
seq3, seq4 = get_result(test_filled2, form2)
seq1.reverse()
seq2.reverse()
seq3.reverse()
seq4.reverse()
seq1, seq2 = print_sequence(seq1, seq2, query_sequence1,
                            database_sequence)
seq3, seq4 = print_sequence(seq3, seq4, query_sequence2,
                            database_sequence)
print(seq1)
print(seq3)
print(seq2)

print('cost:', fin_reasult[0][1])
print('#############################################################################################')
end = time.perf_counter()
print('run time: ', round(end-start), 'seconds')
