from score_matrix_get import score_matrix_get
from score_matrix_fill import score_matrix_fill
from score_matrix_A import score_matrix_A
from load_data import load_database


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
    print(b1)
    print(b2)


# query sequence
query_sequence_list = [
    'KJXXJAJKPXKJJXJKPXKJXXJAJKPXKJJXJKPXKJXXJAJKPXKJXXJAJKHXKJXXJAJKPXKJXXJAJKHXKJXX',
    'ILOTGJJLABWTSTGGONXJMUTUXSJHKWJHCTOQHWGAGIWLZHWPKZULJTZWAKBWHXMIKLZJGLXBPAHOHVOLZWOSJJLPO',
    'IHKKKRKKKKKKXGWGKKKPKSKKKKKBKKKPKHKKXKKBSKKPKWKKLKSKRKKWXKPKKBKKKPKTSKHKKKKLADKKYPKKKOPHKKBWWLPPWKK',
    'MPPPJPXPGPJPPPXPPPJPJPPPXPPPPSPPJJJPPXXPPPPPJPPPXPPXIPJMMMXPKPSVGULMHHZPAWHTHKAAHHUPAONAPJSWPPJGA',
    'IPPVKBKXWXKHSAPHVXXVOJMRAKKPJVLLJBWKOLLJKXHGXLLCPAJOBKPGXBATGXMPOMCVZTAXVPAGKXGOMJQOLJGWGKXLQ'
]

# database sequence
database_sequence = load_database()


least_cost = len(query_sequence_list[0]) * 4
least_cost_records = [0, 0]
fin_reasult = []

for j in range(len(query_sequence_list)):
    query_sequence = query_sequence_list[j]
    least_cost = 9999999999999999999999999999999999
    least_cost_records = [0, 0]
    for i in range(len(database_sequence)):
        test, form = score_matrix_get(
            query_sequence, database_sequence[i], 'init')
        length = form['length']
        depth = form['depth']
        test_filled = score_matrix_A(
            test, form['length'], form['depth'], query_sequence, database_sequence[i])
        if least_cost > test_filled[-1][-1][0]:
            least_cost_records[0] = i
            least_cost_records[1] = test_filled[-1][-1][0]
            #least_cost_records.append([i, test_filled[-1][-1][0]])
            least_cost = test_filled[-1][-1][0]
    print(least_cost_records)
    fin_reasult.append(least_cost_records)
print(fin_reasult)
print('#############################################################################################')


for j in range(len(query_sequence_list)):
    query_sequence = query_sequence_list[j]
    test, form = score_matrix_get(
        query_sequence, database_sequence[fin_reasult[j][0]], 'init')
    length = form['length']
    depth = form['depth']
    test_filled = score_matrix_A(
        test, form['length'], form['depth'], query_sequence, database_sequence[i])
    seq1, seq2 = get_result(test_filled, form)
    seq1.reverse()
    seq2.reverse()
    print_sequence(seq1, seq2, query_sequence,
                   database_sequence[fin_reasult[j][0]])
    print('cost:', fin_reasult[j][1])
    print('#############################################################################################')
