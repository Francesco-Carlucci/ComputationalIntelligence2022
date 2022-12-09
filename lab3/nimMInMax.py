from collections import namedtuple
import logging
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

Nimply = namedtuple("Nimply", "row, num_objects")


class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [2 * i + 1 for i in range(num_rows)]
        self._k = k

    def fromRows(self, rows):
        self._rows = [*rows]
        return self

    def nimming(self, ply: Nimply) -> None:
        if ply is None:
            self._rows = [0 for _ in self._rows]
            # for i, _ in self._rows:
            #    self._rows[i] = 0
            return
        row, num_objects = ply
        assert num_objects > 0
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects

        if self._rows[row] == 0:
            self._rows.pop(row)

        # if sum(self._rows) == 0:
        #    logging.info("You lost")

    def __bool__(self):
        return sum(self._rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"

    @property
    def rows(self) -> tuple:
        return tuple(
            self._rows)  # [row for row in self._rows if row!=0]) #list comprehension faster (~0.07) than tuple(filter(lambda num: num!=0,self._rows)) (~0.09)

    @property
    def k(self) -> int:
        return self._k

    def endTest(self):
        if sum(self._rows) == 0:
            logging.info("You lost")
            return 1
        return 0

    def board(self) -> None:
        for i, row in enumerate(self._rows):
            print(i, ":", end=" ")
            for j in range(row):
                print("|", end=' ')
            print("\n")

cnt=0
"""global cnt
    id=cnt
    cnt+=1"""

def minmax(state: Nim, turn) -> Nimply:

    # val=game.endTest()
    # possible=list(set(range(9))-board[0]-board[1])
    possible = [Nimply(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    if state.endTest():
        return None, 1
    evaluations = list()
    for ply in possible:
        # print(ply)
        new_state = Nim(1, state.k).fromRows(state.rows)
        new_state.nimming(ply)
        #graph.add_node(new_state.rows)
        #graph.nodes[new_state.rows]["label"] = new_state.rows
        #graph.add_edge(state, new_state)  #, label=ply

        #print("    ", end="")
        _, val = minmax(new_state, turn - 2 * turn)
        evaluations.append((ply, -val))
        #print(evaluations)
    ply=max(evaluations, key=lambda k: k[1])
    #print(ply)
    return ply


def won(cells):
    return cells >= {0, 1, 2} or cells >= {3, 4, 5} or cells >= {6, 7, 8} or cells >= {0, 3, 6} or cells >= {1, 4,
                                                                                                             7} or cells >= {
               2, 5, 8} or cells >= {0, 4, 8} or cells >= {2, 4, 6}

def human_play(game):   #human play
    while 1:
        str=input("Enter row index and number of elements to remove: ")
        rowIdx, n=str.split(" ")
        if int(rowIdx)>=len(game.rows):
            print("Invalid row!")
        elif int(n)>game.rows[int(rowIdx)]:
            print("Invalid number, convert to maximum!")
            n=game.rows[int(rowIdx)]
            return int(rowIdx), int(n)
        else:
            return int(rowIdx),int(n)



if __name__ == "__main__":
    cnt=0

    graph = nx.DiGraph()
    game = Nim(3)
    #game.fromRows([2])
    turn = 1
    game.board()
    #labels={}
    graph.add_node(game.rows)
    graph.nodes[game.rows]["label"]=game.rows
    #labels[cnt]=game.rows
    print(graph.nodes(),graph.nodes.data())

    while not game.endTest():
        if turn:
            ply = minmax(game,turn)
            print(ply)
            game.nimming(ply[0])
        else:
            game.nimming(human_play(game))
        game.board()
        turn=1-turn

        """
        # plt.figure(figsize=(15, 9))
        #pos = graphviz_layout(graph, prog="circo")  # dot neato twopi circo fdp sfdp
        pos = nx.spring_layout(graph, seed=32)
        nx.draw(
            graph,
            with_labels=True,
            labels={n: l for n, l in graph.nodes.data("label")},
            # pos=pos,
            node_size=500,
        )
        nx.draw_networkx_edge_labels(graph, pos=pos)
        plt.show()
        """

    if turn:
        print("You lost")
    else:
        print("Agent lost")

