from score_matrix_fill import score_matrix_fill
from score_matrix_init import score_matrix_init

# test data
test_sequence_1 = 'KJXXJAJKPXKJJXJKPXKJXXJAJKPXKJJXJKPXKJXXJAJKPXKJXXJAJKHXKJXXJAJKPXKJXXJAJKHXKJXX'
test_sequence_2 = 'KJOBLLXJKJPLUWGWOMOLIJBJALTUKLVLJSBHGBPGWSYKJBSVJSPMZJOWUWWP'

test, form = score_matrix_init(test_sequence_1, test_sequence_2, 'init')

test_filled = score_matrix_fill(test, form['length'], form['depth'])
print(test)
print("################################")
print(form)
print("################################")
print(test_filled)
