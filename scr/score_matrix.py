import numpy as np

# Cost matrix
MATCH = 0
MISMATCH = 4
GAP = 3

# test data
test_sequence_1 = 'KJXXJAJKPXKJJXJKPXKJXXJAJKPXKJJXJKPXKJXXJAJKPXKJXXJAJKHXKJXXJAJKPXKJXXJAJKHXKJXX'
test_sequence_2 = 'KJOBLLXJKJPLUWGWOMOLIJBJALTUKLVLJSBHGBPGWSYKJBSVJSPMZJOWUWWP'


class score_tree_node():
    def __init__(self, score):
        self.score = score
        self.parent = NULL
        self.child_down = NULL
        self.child_right = NULL
        self.child_lean = NULL

    def create_child_down(self, score):
        self.child_down = score_tree_node(score)
        self.child_down.parent = self

    def create_child_right(self, score):
        self.child_right = score_tree_node(score)
        self.child_down.parent = self

    def create_child_lean(self, score):
        self.child_lean = score_tree_node(score)
        self.child_down.parent = self

    def score_set(self, score):
        self.score = score


def score_matrix_create(sequence_1, sequence_2):
    # query object
    sequence_1 = sequence_1
    sequence_1_length = len(sequence_1)
    # query sequence
    sequence_2 = sequence_2
    sequence_2_length = len(sequence_2)
    # create_score_array
    # score_array = [[1] * (sequence_1_length + 1)
    #               for _ in range(0, sequence_2_length + 1)]
    score_array = np.ones((sequence_2_length, sequence_1_length, 2))
    init_score_array = score_matrix_init(
        score_array, sequence_1_length, sequence_2_length)
    return score_array, init_score_array


def score_matrix_init(score_array, length, depth):
    score_array[0][0][0] = 0
    score_array[0][0][1] = 0
    for i in range(1, length):
        score_array[0][i][0] = score_array[0][i - 1][0] + 3
        score_array[0][i][1] = 1
    for i in range(1, depth):
        score_array[i][0][0] = score_array[i - 1][0][0] + 3
        score_array[i][0][1] = 5
    return score_array


def fill_score_matrix(score_array, depth, length):
    for i in range(1, depth):
        for j in range(1, length):
            least_cost, direction = cost_cal(score_array, i, j)
            score_array[i][j][0] = least_cost
            score_array[i][j][1] = direction
    filled_score_matrix = score_array
    return filled_score_matrix


def cost_cal(score_array, i, j):
    right = score_array[i][j-1][0] + 3
    lean = score_array[i-1][j-1][0]
    down = score_array[i-1][j][0] + 3
    if test_sequence_1[j-1] == test_sequence_2[i-1]:
        lean += 0
    else:
        lean += 4
    # least_cost = [right, lean, down]
    # case 1: only one way
    if right < lean and right < down:
        return right, 1
    if lean < right and lean < down:
        return lean, 3
    if down < right and down < lean:
        return down, 5
    # case 2: two ways
    if right == lean and right < down:
        return right, 1+3
    if lean == down and lean < right:
        return lean, 3+5
    if down == right and down < lean:
        return right, 5+1
    # case 3: three ways
    if right == lean and lean == down:
        return right, 1+3+5


test_matrix, init_score_array = score_matrix_create(
    test_sequence_1, test_sequence_2)

print(init_score_array)

aft_score_matrix = fill_score_matrix(
    init_score_array, len(test_sequence_2), len(test_sequence_1))
print(aft_score_matrix[10])
