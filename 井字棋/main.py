import numpy as np
import pickle
import random
import pdb
from matplotlib import pyplot as plt
EMPTY = 0
BLACK = 1
WHITE = 2
board_shape = (3, 3)



class State(object):
    def __init__(self):
        self.board = np.zeros(board_shape, dtype=np.int)
        self.winner = None
        self._hash = None
        self.turn = BLACK
        self.cnt = 0

    def __hash__(self):
        if self._hash is None:
            self._hash = 0
            for i in range(board_shape[0]):
                for j in range(board_shape[1]):
                    self._hash = self._hash * 3 + self.board[i][j]
            if self.turn == WHITE:
                self._hash = -self._hash
            self._hash = int(self._hash)
        return self._hash

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def apply(self, action: (int, int, int)):
        i, j, color = action
        if self.board[i][j] != 0:
            return None
        ret = State()
        ret.board = np.copy(self.board)
        ret.board[i][j] = color
        ret.cnt = self.cnt + 1
        ret.turn = 3 - self.turn
        return ret

    def finish(self):
        # check winner
        for color in (BLACK, WHITE):
            # check row & col
            for i in range(3):
                if color == self.board[i][0] and color == self.board[i][1] and color == self.board[i][2]:
                    self.winner = color
                    return True
                if color == self.board[0][i] and color == self.board[1][i] and color == self.board[2][i]:
                    self.winner = color
                    return True
            # check diagonal
            if color == self.board[0][0] and color == self.board[1][1] and color == self.board[2][2]:
                self.winner = color
                return True
            if color == self.board[0][2] and color == self.board[1][1] and color == self.board[2][0]:
                self.winner = color
                return True
        # check empty
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY:
                    return False
        # tie
        self.winner = EMPTY
        return True

record={}
def init():
    state = State()
    state = state.apply((1,1,BLACK))
    for i in range(3):
        for j in range(3):
            if i==1 and j==1:
                continue
            t = state.apply((i,j,WHITE))
            record[t]=[0.0]
    print(record)
init()
class Model(object):
    def __init__(self, file=None):
        if file is None:
            self.value_table = {}
        else:
            self.value_table = pickle.load(open(file, 'rb'))

    def value_function(self, state: State):
        if state.__hash__() not in self.value_table.keys():
            self.value_table[state] = 0.0
        return self.value_table[state]

    def policy_function(self, state: State, beta: float):
        ret = None
        rand = random.random()
        # random explore
        if rand < beta:
            empty_position = []
            for i in range(3):
                for j in range(3):
                    if state.board[i][j] == EMPTY:
                        empty_position.append((i, j))
            position = random.choice(empty_position)
            ret = state.apply((position[0], position[1], state.turn))
        # choice max value state
        else:
            max_value = None
            for i in range(3):
                for j in range(3):
                    if state.board[i][j] == EMPTY:
                        tmp = state.apply((i, j, state.turn))
                        #print(tmp.board,self.value_function(tmp))
                        if max_value is None or self.value_function(tmp) > max_value:
                            max_value = self.value_function(tmp)
                            ret = tmp
        return ret

    def train(self, alpha=0.1, beta=0.2, epochs=10000):
        for epoch in range(epochs):
            #pdb.set_trace()
            black_states = []
            white_states = []
            current_state = State()
            while True:
                next_state = self.policy_function(current_state, beta)
                if current_state.turn == BLACK:
                    black_states.append(next_state)
                else:
                    white_states.append(next_state)
                current_state=next_state
                if current_state.finish():
                    break
            # bp
            if current_state.winner == BLACK:
                black_reward = 1.0
                white_reward = 0.0
            elif current_state.winner == WHITE:
                black_reward = 0.0
                white_reward = 1.0
            else:
                black_reward = 0.5
                white_reward = 0.5
            for state in reversed(black_states):
                value = self.value_function(state)
                new_value = value + alpha * (black_reward - value)
                self.value_table[state] = new_value
                black_reward = self.value_table[state]
            for state in reversed(white_states):
                value = self.value_function(state)
                new_value = value + alpha * (white_reward - value)
                self.value_table[state] = new_value
                white_reward = self.value_table[state]
            if epoch%1000==999:
                print("training epoch %d"%(epoch+1))
                for state,value_list in record.items():
                    value_list.append(self.value_table.get(state) or 0.0)
                f = open("model-%d.pkl"%(epoch+1), 'wb')

                pickle.dump(self.value_table, f)
                f.close()

    def predict(self, state: State):
        return self.policy_function(state, -1)


def play(model):
    #model = Model("model.pkl")
    while True:
        op = None
        while True:
            op = input("请输入 [b]先手 [w]后手 [q]退出：")
            if op in ('b', 'w', 'q'):
                break
        if op == 'q':
            return
        state = State()
        if op == 'b':
            turn = "human"
        else:
            turn = "ai"
        while True:
            if turn=="human":
                turn="ai"
                pos = input("position(0-8):")
                pos = int(pos)
                i = pos//3
                j = pos%3
                state = state.apply((i,j,state.turn))
            else:
                turn = "human"
                state = model.policy_function(state,-1)
            print(state.board)
            if state.finish():
                print("Winner: %s"%state.winner)
                break

if __name__ == '__main__':
    model = Model()
    model.train(alpha=0.05,epochs=500000)
    play(model)
