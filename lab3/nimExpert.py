import logging
import random
from collections import namedtuple

Nimply = namedtuple("Nimply", "row, num_objects")

class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [2*i + 1 for i in range(num_rows)]
        self._k = k

    def nimming(self, ply:Nimply) -> None:
        row, num_objects=ply
        assert num_objects>0
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects
        #if sum(self._rows) == 0:
        #    logging.info("You lost")
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

    def endTest(self):
        if sum(self._rows) == 0:
            logging.info("You lost")
            return 1
        return 0

    def board(self)->None:
        for i,row in enumerate(self._rows):
            print(i,":",end=" ")
            for j in range(row):
                print("|", end=' ')
            print("\n")

def pure_random(state: Nim) -> Nimply:
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)

def gabriele(state: Nim) -> Nimply:
    """Pick always the maximum possible number of the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))

def nimSum(rows):
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

def policy(game):
    rows=game.rows
    totNimSum=nimSum(rows)
    if(totNimSum!=0):
        nonOneRow=checkMisere(rows)
        if nonOneRow!=-1:
            if len([_ for _ in rows if _!=0])%2==0:
                return Nimply(nonOneRow,rows[nonOneRow])
            else:
                return Nimply(nonOneRow, rows[nonOneRow]-1)
        for i,row in enumerate(rows):
            lineNimSum=nimSum([totNimSum,row])
            if(lineNimSum<row):
                print(f"removing {row-lineNimSum} elements from row {i}")
                #game.nimming(i,row-lineNimSum)
                return Nimply(i,row-lineNimSum)
    #altrimenti somma zero, siamo in posizione perdente
    return pure_random(game)

def play(game):   #human play
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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game=Nim(5)
    game.board()
    print("current nim sum: ",nimSum(game._rows))
    turn=1
    while not game.endTest():
        turn = 1 - turn
        if not turn:
            print("Your turn:")
            game.nimming(play(game))
        else:
            print("Agent turn:")
            game.nimming(policy(game))
        game.board()
    if not turn:
        print("You lost")
    else:
        print("Agent lost")
    #print("player ",turn," lost!")


