
# Cost matrix
MATCH = 0
MISMATCH = 4
GAP = 3

# test data
test_sequence_1 = 'KJXXJAJKPXKJJXJKPXKJXXJAJKPXKJJXJKPXKJXXJAJKPXKJXXJAJKHXKJXXJAJKPXKJXXJAJKHXKJXX'
test_sequence_2 = 'KJOBLLXJKJPLUWGWOMOLIJBJALTUKLVLJSBHGBPGWSYKJBSVJSPMZJOWUWWP'


def score_matrix_A(score_array, length, depth, sequence1, sequence2):
    current_position = {'transverse': 0, 'longitude': 0}
    while(current_position['transverse'] < length and current_position['longitude'] < depth):
        # cal g(n)
        right, lean, down = cal_cost_A(
            score_array, current_position['transverse'], current_position['longitude'], sequence1, sequence2)
        # f(n) = g(n) + h(n)
        # h(n)
        # right += (length - current_position['transverse'] - 1) +( depth - current_position['longitude'])
        # lean += (length - current_position['transverse'] - 1) + (depth - current_position['longitude'] - 1)
        # down += (length - current_position['transverse']) + (depth - current_position['longitude'] - 1)
        hn = (length - current_position['transverse']
              ) + (depth - current_position['longitude'])
        if lean + hn - 2 <= right + hn - 1 and lean + hn - 2 <= down + hn - 1:
            current_position['transverse'] += 1
            current_position['longitude'] += 1
            score_array[current_position['longitude']
                        ][current_position['transverse']][0] = lean
            score_array[current_position['longitude']
                        ][current_position['transverse']][1] = 3
            continue
        if right + hn - 1 <= lean + hn - 2 and right + hn - 1 <= down + hn - 1:
            current_position['transverse'] += 1
            #current_position['longitude'] += 1
            score_array[current_position['longitude']
                        ][current_position['transverse']][0] = right

            continue


def cal_cost_A(score_array, i, j, sequence1, sequence2):
    right = score_array[i][j][0] + GAP
    lean = score_array[i][j][0]
    if sequence1[j+1] == sequence2[i+1]:
        lean += MATCH
    else:
        lean += MISMATCH
    down = score_array[i][j][0] + GAP
    return right, lean, down
