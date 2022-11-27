import logging

class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [2*i + 1 for i in range(num_rows)]
        self._k = k

    def nimming(self, row: int, num_objects: int) -> None:
        assert num_objects>0
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects
        if sum(self._rows) == 0:
            logging.info("You lost")

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
        #print('\n')


def nimSum(rows):
    sum=rows[0]
    for i in rows[1:]:
        sum^=i
    return sum

def policy(game):
    rows=game._rows
    totNimSum=nimSum(rows)
    if(totNimSum!=0):
        for i,row in enumerate(rows):
            lineNimSum=nimSum([totNimSum,row])
            if(lineNimSum<row):
                print(f"removing {row-lineNimSum} elements from row {i}")
                game.nimming(i,row-lineNimSum)
                return
    #altrimenti somma zero, siamo in posizione perdente
    for i,row in enumerate(rows):
        if row>0:
            print(f"removing {1} elements from row {i}")
            game.nimming(i,1)
            return

def play(game):
    str=input("Enter row index and number of elements to remove: ")
    rowIdx, n=str.split(" ")
    game.nimming(int(rowIdx),int(n))

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
            play(game)
        else:
            print("Agent turn:")
            policy(game)
        game.board()
    if not turn:
        print("You lost")
    else:
        print("Agent lost")
    #print("player ",turn," lost!")


