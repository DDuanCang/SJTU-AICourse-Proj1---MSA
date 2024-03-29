from environment import *
import pandas as pd


def play(policy, num_games=100000):
    """
    play the Easy21 game using the given policy
    :param policy: generally dict-like: (player_score, dealer_score) -> stick or hit
    :param num_games: number of games
    :return: number of wins, loses, ties, and the rate of wins (%)
    """
    wins = 0
    loses = 0
    env = Easy21Environment()
    for game in range(num_games):
        env.reset()
        dealer_score = env.state['dealer_score']
        while True:
            player_score = env.state['player_score']
            if policy.iat[player_score-1, dealer_score-1] == "s":
                state, reward = env.step(action=1)
                break
            else:
                state, reward = env.step(action=0)
                if state["game_over"]:
                    break
        if reward == 1:
            wins += 1
        elif reward == -1:
            loses += 1
    return wins, loses, num_games - wins - loses, wins/num_games*100


if __name__ == '__main__':
    q_learning_path = "q-learning.csv"
    policy = pd.read_csv(q_learning_path)
    policy = policy.iloc[:, 1:]
    num_wins, num_loses, num_ties, win_rate = play(policy)
    print(num_wins, num_loses, num_ties, win_rate)
    print()
