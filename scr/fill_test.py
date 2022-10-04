from score_matrix_get import score_matrix_get
from score_matrix_fill import score_matrix_fill
from score_matrix_A import score_matrix_A


# test data
test_sequence_1 = 'KJXXJAJKPXKJJXJKPXKJXXJAJKPXKJJXJKPXKJXXJAJKPXKJXXJAJKHXKJXXJAJKPXKJXXJAJKHXKJXX'
test_sequence_2 = 'KJOBLLXJKJPLUWGWOMOLIJBJALTUKLVLJSBHGBPGWSYKJBSVJSPMZJOWUWWP'

test, form = score_matrix_get(test_sequence_1, test_sequence_2, 'init')

length = form['length']
depth = form['depth']

test_filled = score_matrix_A(
    test, form['length'], form['depth'], test_sequence_1, test_sequence_2)
print(test[1])
print("################################")
print('test_sequence_1:'+str(len(test_sequence_1)))
print('test_sequence_2:'+str(len(test_sequence_2)))
print(form)
print("################################")
print(test_filled[-1])
print(test_filled[depth-1][length-1][0])
print(len(test_filled[0]))


def get_result(filled_array, form):
    length = form['length']
    depth = form['depth']
    # tree = score_tree_node.score_tree_node(filled_array[depth-1][length-1][0])
    # current_node = tree
    result1 = []
    result2 = []

    while(filled_array[depth-1][length-1][1] != 0):
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


a1, a2 = get_result(test_filled, form)
print(a1, a2)
print(len(a1), len(a2))
a1.reverse()
a2.reverse()
print(a1, a2)
print(len(a1), len(a2))

b1 = ''
b2 = ''
for i in range(max(len(a1), len(a2))):
    if a1[i] == -1:
        letter1 = '_'
    else:
        letter1 = test_sequence_1[a1[i]-1]
    if a2[i] == -1:
        letter2 = '_'
    else:
        letter2 = test_sequence_2[a2[i]-1]
    b1 += letter1
    b2 += letter2
print(test_sequence_1)
print(test_sequence_2)
print(b1)
print(b2)
