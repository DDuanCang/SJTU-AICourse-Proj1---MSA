
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