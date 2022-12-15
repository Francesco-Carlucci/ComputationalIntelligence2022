from collections import namedtuple
import logging
import random
import networkx as nx
import matplotlib.pyplot as plt
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

def nimSum(rows):  #pass to reduce
    sum=rows[0]
    for i in rows[1:]:
        sum^=i
    return sum

def checkMisere(rows):
    cnt=0
    nonOneRow=-1
    for i,row in enumerate(rows):
        if row>=2:
            cnt+=1
            nonOneRow=i
        if cnt==2:
            return -1
    return nonOneRow

def expert(game):
    rows=game.rows
    totNimSum=nimSum(rows)
    if(totNimSum!=0):
        OneRow=checkMisere(rows)
        if OneRow!=-1:
            if len([_ for _ in rows if _!=0])%2==0:
                return Nimply(OneRow,rows[OneRow])
            else:
                return Nimply(OneRow, rows[OneRow]-1)
        for i,row in enumerate(rows):
            lineNimSum=nimSum([totNimSum,row])
            if(lineNimSum<row):
                #print(f"removing {row-lineNimSum} elements from row {i}")
                #game.nimming(i,row-lineNimSum)
                return Nimply(i,row-lineNimSum)
    #altrimenti somma zero, siamo in posizione perdente
    return pure_random(game)

#@profile
def minmax(state: Nim,lvl) -> Nimply:
    possible = [Nimply(r, o) for r, c in enumerate(state.rows) for o in range(1,c+1)]  #(c+1,0,-1)
    possible.reverse()
    if state.endTest():
        return None, 1
    if lvl>stop_lvl:   #level stop
        possible=random.sample(possible, k=max(int(len(possible)/pruning_factor),1))
        #return None,0
    evaluations = list()
    for ply in possible:
        new_state = Nim(0, state.k).fromRows(state.rows)
        new_state.nimming(ply)

        _, val = minmax(new_state,lvl+1)
        if -val==1:
            return (ply,-val)
        evaluations.append((ply, -val))
    ply=max(evaluations, key=lambda k: k[1])
    return ply

def pure_random(state: Nim) -> Nimply:
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)

def evaluate(prob) -> float:
    win_count = 0
    for _ in range(eval_amount):
        game = Nim(7) #random.randint(5,7)
        turn=1   #inizia l'individuo turno 0, random turno 1
        while not game.endTest():
            turn = 1 - turn
            if not turn:
                game.nimming(minmax(game,0)[0])
            else:
                if random.random() < prob:
                    game.nimming(expert(game))
                else:
                    game.nimming(pure_random(game))
        if turn:   #gioco finito e ultima mossa di random
            win_count += 1
    return win_count/eval_amount

if __name__ == "__main__":
    stop_lvl=6
    pruning_factor=5
    eval_amount=50
    exp_eval=[0,0.2,0.4,0.5,0.6,0.8,0.9,1]

    graph = nx.DiGraph()
    game = Nim(7)
    #game.fromRows([20])


    graph.add_node(game.rows)
    graph.nodes[game.rows]["label"]=game.rows


    res=[]
    for prob in exp_eval:
        result=evaluate(prob)
        res.append(result)
        print(prob,': ',result)

    plt.plot(exp_eval,res)
    plt.show()


    #play against human
    turn = 1
    game.board()
    while not game.endTest():
        if turn:
            ply = minmax(game,0)
            print(ply)
            game.nimming(ply[0])
        else:
            game.nimming(human_play(game))
        print(game.rows)
        game.board()
        turn=1-turn

        """  #print graph of the search
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

