
# Cost matrix
MATCH = 0
MISMATCH = 4
GAP = 3


# arguments: score_matrix,matrix length, matrix depth
# return: filled_score_matrix
def score_matrix_A(score_array, length, depth, sequence1, sequence2):
    for i in range(1, depth):
        for j in range(1, length):
            least_cost, direction = cost_cal(
                score_array, i, j, sequence1, sequence2)
            score_array[i][j][0] = least_cost
            score_array[i][j][1] = direction
    filled_score_matrix = score_array
    return filled_score_matrix


# arguments: score_matrix,current position of matrix length, current position of matrix depth
# return: current position cost, ways to move to current position
# 1:move right
# 3:move lean
# 5:move down
# 1+3=4: move right and lean
# 1+5=6: move right and down
# 3+5=7: move lean and down
# 1+3+5=9: move right and lean and down
def cost_cal(score_array, i, j, sequence1, sequence2):
    # g(n)
    # cal gap move cost
    right = score_array[i][j-1][0] + GAP
    # cal match or mismatch cost
    lean = score_array[i-1][j-1][0]
    if sequence1[j-1] == sequence2[i-1]:
        lean += MATCH
    else:
        lean += MISMATCH
    # cal gap move cost
    down = score_array[i-1][j][0] + GAP

    # h(n)
    hn = (i + j)*3

    # least_cost = [right, lean, down]
    # f(n) = g(n) + h(n)
    # case 1: only one way
    if (right + hn - 3) < (lean + hn - 6) and (right + hn - 3) < (down + hn - 3):
        return right, 1
    if (lean + hn - 6) < (right + hn - 3) and (lean + hn - 6) < (down + hn - 3):
        return lean, 3
    if (down + hn - 3) < (right + hn - 3) and (down + hn - 3) < (lean + hn - 6):
        return down, 5
    # case 2: two ways
    if (right + hn - 3) == (lean + hn - 6) and (right + hn - 3) < (down + hn - 3):
        return right, 1+3
    if (lean + hn - 6) == (down + hn - 3) and (lean + hn - 6) < (right + hn - 3):
        return lean, 3+5
    if (down + hn - 3) == (right + hn - 3) and (down + hn - 3) < (lean + hn - 6):
        return right, 5+1
    # case 3: three ways
    if (right + hn - 3) == (lean + hn - 6) and (lean + hn - 6) == (down + hn - 3):
        return right, 1+3+5
