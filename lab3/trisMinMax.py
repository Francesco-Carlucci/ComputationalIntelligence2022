from collections import namedtuple
import logging

def minmax(board):
    val=eval_terminal(*board)
    possible=list(set(range(9))-board[0]-board[1])
    if val!=0 or not possible:
        return None, val
    evaluations=list()
    for ply in possible:
        _,val=minmax((board[1],board[0]|{ply}))
        evaluations.append((ply,-val))
    return max(evaluations, key=lambda k: k[1])

def won(cells):
    return cells>={0,1,2}  or cells>={3,4,5}  or cells>={6,7,8}  or cells>={0,3,6}  or cells>={1,4,7}  or cells>={2,5,8}  or cells>={0,4,8}  or cells>={2,4,6}

def eval_terminal(x, o):
    if won(x):
        return 1
    elif won(o):
        return -1
    else:
        return 0

if __name__=="__main__":
    board=(set([]),set([]))  #range(9)

    for i in range(9):
        if (i!=0 and i % 3 == 0):
            print("\n______")
        if i in board[0]:
            print("x",end='')
        elif i in board[1]:
            print("o",end='')
        else:
            print(" ", end='')
        print("|",end='')
    print()

    print(minmax(board))

