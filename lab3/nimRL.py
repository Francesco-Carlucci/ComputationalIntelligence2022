import matplotlib.pyplot as plt
import numpy as np
import random
from collections import namedtuple
import pickle

Nimply = namedtuple("Nimply", "row, num_objects")


class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [2 * i + 1 for i in range(num_rows)]
        self._k = k
        self._turn = 0

    def fromRows(self, rows):
        self._rows = [*rows]
        return self

    def nimming(self, ply: Nimply) -> None:
        if ply is None:
            for i, _ in self._rows:
                self._rows[i] = 0
            return
        row, num_objects = ply
        assert num_objects > 0
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects
        self._turn = 1 - self._turn

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    @property
    def k(self) -> int:
        return self._k

    @property
    def turn(self) -> int:
        return self._turn

    def endTest(self):
        if sum(self._rows) == 0:
            return 1
        return 0

    def board(self) -> None:
        for i, row in enumerate(self._rows):
            print(i, ":", end=" ")
            for j in range(row):
                print("|", end=' ')
            print("\n")

    # RL
    def get_reward(self):
        reward = -1
        if self.endTest():
            if self._turn == 0:
                reward = -2
            else:
                reward = 0
        return reward


class Agent(object):
    def __init__(self, states, alpha=0.15, random_factor=0.2):  # 80% explore, 20% exploit
        self.state_history = []  # state, reward
        self.alpha = alpha
        self.random_factor = random_factor
        self.G = {}

    #    self.init_reward(states)
    #
    # def init_reward(self, states):
    #    for move in [Nimply(r, o) for r, c in enumerate(states.rows) for o in range(1, c + 1)]:
    #        self.G[move] = np.random.uniform(low=1.0, high=0.1)

    def choose_action(self, state):
        maxG = -10e15
        next_move = None
        randomN = np.random.random()
        allowedMoves = [Nimply(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
        if randomN < self.random_factor:
            # if random number below random factor, choose random action
            next_move = random.choice(allowedMoves)
        else:
            # if exploiting, gather all possible actions and choose one with the highest G (reward)
            uncharted = []
            for action in allowedMoves:
                l = len(state.rows)
                new_state = Nim(l).fromRows(state.rows)
                new_state.nimming(action)
                if new_state.rows not in self.G:
                    uncharted.append(action)
                elif self.G[new_state.rows] >= maxG:
                    maxG = self.G[new_state.rows]
                    next_move = action
            if len(uncharted) != 0:
                next_move = random.choice(uncharted)
        return next_move

    def update_state_history(self, state, reward):
        self.state_history.append((state, reward))

    def learn(self):
        target = 0

        for prev, reward in reversed(self.state_history):
            if prev not in self.G:
                self.G[prev] = np.random.uniform(low=1.0, high=0.1)
            self.G[prev] = self.G[prev] + self.alpha * (target - self.G[prev])
            target += reward

        self.state_history = []

        self.random_factor -= 10e-5  # decrease random factor each episode of play

def nimSum(rows):
    sum = rows[0]
    for i in rows[1:]:
        sum ^= i
    return sum

def checkMisere(rows):
    cnt = 0
    nonOneRow = -1
    for i, row in enumerate(rows):
        if row >= 2:
            cnt += 1
            nonOneRow = i
        if cnt == 2:
            return -1
    return nonOneRow

def pure_random(state: Nim) -> Nimply:
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)

def expert(game) -> Nimply:
    rows = game.rows
    totNimSum = nimSum(rows)
    if (totNimSum != 0):
        nonOneRow = checkMisere(rows)
        if nonOneRow != -1:
            if len([_ for _ in rows if _ != 0]) % 2 == 0:
                return Nimply(nonOneRow, rows[nonOneRow])
            else:
                return Nimply(nonOneRow, rows[nonOneRow] - 1)
        for i, row in enumerate(rows):
            lineNimSum = nimSum([totNimSum, row])
            if (lineNimSum < row):
                return Nimply(i, row - lineNimSum)
    return pure_random(game)

def evaluate(gamesize: int, robot: Agent) -> float:
    win_count = 0
    neval = 100
    robot.random_factor = 0
    turn = 1
    for _ in range(neval):
        game = Nim(gamesize)
        while not game.endTest():
            turn = 1 - turn
            if not turn:
                game.nimming(robot.choose_action(game))
            else:
                game.nimming(pure_random(game))
        if turn:
            win_count += 1
    return win_count / neval

def almost_random(game,prob):
    if random.random() < prob:
        return expert(game)
    else:
        return pure_random(game)


if __name__ == '__main__':
    nrows = 5
    nepochs = 200_000
    game = Nim(nrows)
    robot = Agent(game, alpha=0.005, random_factor=0.4)
    perf=[]
    indices=[]

    for i in range(nepochs):
        while not game.endTest():
            action = robot.choose_action(game)
            game.nimming(action)
            if not game.endTest():
                game.nimming(almost_random(game,0.99))
            reward = game.get_reward()
            robot.update_state_history(game.rows, reward)
        robot.learn()
        game = Nim(nrows)
        if i % 50 == 0:
            res=evaluate(nrows,robot)
            print(f"{i}: {res}")
            perf.append(res)
            indices.append(i)
        if i==120_000:
            robot.alpha=robot.alpha/2

    plt.semilogy(indices, perf, "b")
    plt.show()

    with open("./agent", "bw") as out:
        print("Saving to file...")
        # print(robot.G)
        pickle.dump(robot.G, out)
    print(evaluate(nrows, robot))