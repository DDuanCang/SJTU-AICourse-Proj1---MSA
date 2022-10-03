import numpy as np

# test data
test_sequence_1 = 'KJXXJAJKPXKJJXJKPXKJXXJAJKPXKJJXJKPXKJXXJAJKPXKJXXJAJKHXKJXXJAJKPXKJXXJAJKHXKJXX'
test_sequence_2 = 'KJOBLLXJKJPLUWGWOMOLIJBJALTUKLVLJSBHGBPGWSYKJBSVJSPMZJOWUWWP'

# arguments: sequence1,sequence2,return type
# return: score matrix, size of the matrix


def score_matrix_init(sequence_1, sequence_2, type):
    score_array, score_array_init, form = score_matrix_create(
        sequence_1, sequence_2)
    if type == 'origin':
        print('return prigin matrix')
        return score_array, form
    if type == 'init':
        print('return init matrix')
        return score_array_init, form
    return [], {'length': 0, 'depth': 0}

# arguments: sequence1,sequence2
# return: score matrix, size of the matrix


def score_matrix_create(sequence_1, sequence_2):
    # query object
    # length
    sequence_1 = sequence_1
    sequence_1_length = len(sequence_1)
    # query sequence
    # depth
    sequence_2 = sequence_2
    sequence_2_length = len(sequence_2)
    form = {'length': sequence_1_length, 'depth': sequence_2_length}
    # create matrix by np.ones
    score_array = np.ones((sequence_2_length, sequence_1_length, 2))
    print('np.ones complete')
    init_score_array = score_matrix_init(
        score_array, form['length'], form['depth'])
    print('init complete')
    return score_array, init_score_array, form

# arguments: matrix,length of matrix,depth of matrix


def score_matrix_init(score_array, length, depth):
    print('start init')
    score_array[0][0][0] = 0
    score_array[0][0][1] = 0
    for i in range(1, length):
        score_array[0][i][0] = score_array[0][i - 1][0] + 3
        score_array[0][i][1] = 1
    for i in range(1, depth):
        score_array[i][0][0] = score_array[i - 1][0][0] + 3
        score_array[i][0][1] = 5
    return score_array


test = score_matrix_init(test_sequence_1, test_sequence_2, 'init')
print(test)
