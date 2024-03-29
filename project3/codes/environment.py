import random
from copy import deepcopy


class Easy21Environment:
    def __init__(self):
        """
        Initially pick a random card for the player and the dealer
        """
        player_score, _ = self.draw_card()
        dealer_score, _ = self.draw_card()
        # define state
        self.state = {"player_score": player_score, "dealer_score": dealer_score,
                      "game_over": False}
        # game history, record state, reward, action of each step
        self.history = ["Initial state: {}".format(self.state)]
        # define actions
        self.actions = {0: "h", 1: "s"}

    def reset(self):
        """
        Reset the environment
        """
        player_score, _ = self.draw_card()
        dealer_score, _ = self.draw_card()
        self.state = {"player_score": player_score, "dealer_score": dealer_score,
                      "game_over": False}
        self.history = ["Initial state: {}".format(self.state)]

    def step(self, current_state=None, action=0):
        """
        Compute a step in Easy21 game.
        Common format: next_state, reward = step(current_state, action)
        """
        self.history.append("Player action: {}".format(action))
        if self.state["game_over"]:
            self.history.append("The game is over. Please reset for a new game.")
            return None, None

        # player hits
        if action == 0:
            value, color = self.draw_card()
            self.state['player_score'] = self.update_score(value, color, current_score=self.state['player_score'])
            if self.check_bust(self.state['player_score']):
                # player goes bust
                reward = -1
                self.state["game_over"] = True
                self.history.append("The player goes bust.")
                self.history.append("State: {}".format(self.state))
                return deepcopy(self.state), reward
            else:
                reward = 0
                self.history.append("State: {}".format(self.state))
                return deepcopy(self.state), reward
        # player sticks
        elif action == 1:
            self.history.append("State: {}".format(self.state))
            return self.dealer_moves()
        else:
            self.history.append("Invalid action id.")
            return None, None

    @staticmethod
    def draw_card():
        """
        v in {1, ..., 10}, red 1/3, black 2/3
        """
        value = random.randint(1, 10)
        color = ("red" if random.uniform(0, 1) <= 1 / 3 else "black")
        return value, color

    @staticmethod
    def check_bust(score):
        """
        Check whether the player/dealer goes bust
        """
        return (score > 21) or (score < 1)

    @staticmethod
    def update_score(value, color, current_score):
        """
        Update the score given the value and the color
        """
        if color == "black":
            new_score = current_score + value
        else:
            new_score = current_score - value
        return new_score

    def dealer_moves(self):
        """
        The dealer's turn
        """
        self.history.append("Dealer's turn.")
        # score < 16, dealer hits
        while self.state['dealer_score'] < 16:
            value, color = self.draw_card()
            new_dealer_score = self.update_score(value, color, current_score=self.state['dealer_score'])
            self.state['dealer_score'] = new_dealer_score
            self.history.append("Dealer action: hit")
            if self.check_bust(new_dealer_score):
                # dealer goes bust, player wins
                reward = 1
                self.state["game_over"] = True
                self.history.append("The dealer goes bust.")
                self.history.append("State: {}".format(self.state))
                return deepcopy(self.state), reward
            self.history.append("State: {}".format(self.state))

        # score >= 16, dealer sticks
        self.history.append("Dealer action: stick")
        self.state["game_over"] = True
        self.history.append("State: {}".format(self.state))

        player_score = self.state['player_score']
        dealer_score = self.state['dealer_score']
        # compare their scores
        if player_score > dealer_score:
            reward = 1
        elif player_score == dealer_score:
            reward = 0
        else:
            reward = -1
        return deepcopy(self.state), reward


if __name__ == '__main__':
    easy21_game = Easy21Environment()
    easy21_game.step(action=0)
    easy21_game.step(action=0)
    easy21_game.step(action=0)
    print(easy21_game.history)
    easy21_game.reset()
    easy21_game.step(action=0)
    easy21_game.step(action=1)
    easy21_game.step(action=0)
    print(easy21_game.history)
    print()
