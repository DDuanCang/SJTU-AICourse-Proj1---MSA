from environment import *
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

sns.set()


def plot_optimal_Q(Q):
    """
    matplotlib, plot the Q value figure
    :param Q: generally dict-like: state (player_score, dealer_score) -> Q values
    :return: you can save the figure
    """
    fig = plt.figure(figsize=(10, 5))
    ax = plt.axes(projection="3d")
    dealer_showing = np.arange(1, 11)
    player_score = np.arange(1, 22)
    dealer_showing, player_score = np.meshgrid(dealer_showing, player_score)
    max_Q = np.ndarray(shape=(21, 10))
    for state in Q.keys():
        max_Q[state[0] - 1][state[1] - 1] = Q[state].max()
    # Plot the surface
    surf = ax.plot_surface(dealer_showing, player_score, max_Q, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    plt.xlabel('Dealer showing', fontsize=12)
    plt.ylabel('Player score', fontsize=12)
    plt.title('Optimal Q value function', fontsize=16)
    plt.xticks(np.arange(1, 11))
    plt.yticks(np.arange(1, 22, 3))
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


# epsilon/m, epsilon/m+1-epsilon
def epsilon_greedy_policy(Q, state, m, epsilon):
    """
    implement epsilon greedy policy, then choose an action according to its probability
    you can also return the index of the action that we randomly choose according to its probability
    :param Q: generally dict-like: state (player_score, dealer_score) -> Q values
    :param state: (player_score, dealer_score)
    :param m: number of actions
    :param epsilon: hyper-parameter
    :return: probabilities of each action
    """
    return None


def get_greedy_policy(Q, state):
    """
    choose the action whose Q value is the largest
    :param Q: generally dict-like: state (player_score, dealer_score) -> Q values
    :param state: (player_score, dealer_score)
    :return: index of the action with the largest Q value
    """
    return None


def get_policy(Q):
    """
    get the policy according to Q
    :param Q: generally dict-like: state (player_score, dealer_score) -> Q values
    :return: policy
    """
    actions = {0: "h", 1: "s"}
    df = pd.DataFrame(columns=["player_score", "dealer_showing", "best_action"])
    for i, state in enumerate(Q.keys()):
        best_action = actions[get_greedy_policy(Q, state)]
        df.loc[i] = (state[0], state[1], best_action)

    df_pivot = df.pivot("player_score", "dealer_showing", "best_action")
    return df_pivot


def initial_Q(num_actions):
    """
    initial Q as zeros
    :param num_actions: number of actions
    :return: Q
    """
    Q = {}
    for player_score in range(1, 22):
        for dealer_score in range(1, 11):
            Q[(player_score, dealer_score)] = np.zeros(num_actions)
    return Q


def q_learning(env=Easy21Environment(), episode_nums=100, discount_factor=0.9, alpha=0.01, epsilon=0.1):
    """
    q-learning algorithm
    :param env: game environment
    :param episode_nums: number of episode
    :param discount_factor: hyper-parameter
    :param alpha: hyper-parameter
    :param epsilon: hyper-parameter
    :return: Q, rewards list
    """
    num_actions = len(env.actions)
    Q = initial_Q(num_actions)
    rewards = []
    for i in range(episode_nums):
        env.reset()
        # state: (player_score, dealer_score)
        cur_state, done = (env.state["player_score"], env.state["dealer_score"]), env.state["game_over"]
        sum_reward = 0.0
        while not done:
            # choose by epsilon greedy, update
            prob_actions = epsilon_greedy_policy(Q, cur_state, num_actions, epsilon)
            action = np.random.choice(np.arange(num_actions), p=prob_actions)
            # take action, observe
            next_state, reward = env.step(action=action)
            next_state, done = (next_state["player_score"], next_state["dealer_score"]), next_state["game_over"]
            if done:
                # Q[cur_state][action] = ...
                break
            else:
                # we need the next action (by greedy policy) to update Q and then update the current_state
                # ...
                # Q[cur_state][action] = ...
                # ...
                print()
            sum_reward += reward
        rewards.append(sum_reward)
    return Q, rewards


if __name__ == '__main__':
    # random.seed(511)
    # np.random.seed(511)
    epochs = 1000000
    gamma = 1.0
    alpha = 0.01
    epsilon = 0.1
    Q, rewards = q_learning(env=Easy21Environment(), episode_nums=epochs,
                            discount_factor=gamma, alpha=alpha, epsilon=epsilon)
    policy = get_policy(Q)
    print(policy)
    plot_optimal_Q(Q)
    policy.to_csv("q-learning.csv")
    print()
