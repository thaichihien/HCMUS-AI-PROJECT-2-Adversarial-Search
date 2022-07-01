from unittest import result
import random

PLAYER = 'O'
COMPUTER = 'X'
INFINITY = -1000

def ismoveleft():
    for row in board:
        if ' ' in row:
            return True
    return False

def empty_space():
    result = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                result.append((i,j))
    
    return result

def check():

    for row in board:
        if row[0] == row[1] and row[1] == row[2]:
            if row[0] == COMPUTER:
                return 100
            elif row[0] == PLAYER:
                return -100
   
    for col in range(3):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col]:
            if board[0][col] == COMPUTER:
                return 100
            elif board[0][col] == PLAYER:
                return -100

    if (board[0][0] == board[1][1] and board[1][1]== board[2][2] 
        or board[0][2] == board[1][1] and board[1][1] == board[2][0]):
        if board[1][1] == COMPUTER:
            return 100
        elif board[1][1] == PLAYER:
            return -100

    return 0


   
def player():
    player_move1 = int(input("\nPlace at row: "))
    player_move2 = int(input("Place at col: "))
    #check
    board[player_move1][player_move2] = PLAYER


def minimax(_board,depth,a,b,Maximize,limit=0):

    if depth >= limit and limit > 0:return 0

    result = check()
    if result != 0:
        return result

    if not ismoveleft():return 0


    if Maximize:
        bestValue = INFINITY
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':

                    board[i][j] = COMPUTER
                    value = minimax(_board,depth+1,a,b,False,limit)
                    board[i][j] = ' '
                    bestValue = max(value,bestValue)
                    a = max(a,value)
                    if b <= a:
                        break

        return bestValue
    else:
        worstValue = INFINITY*-1
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':

                    board[i][j] = PLAYER
                    value = minimax(_board,depth+1,a,b,True,limit)
                    board[i][j] = ' '
                    worstValue = min(value,worstValue)
                    b = min(b,value)
                    if b <= a:
                        break
                    
        return worstValue


def computer_hard():
    bestScore = INFINITY
    bestMove = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = COMPUTER
                score = minimax(board,0,INFINITY,-1*INFINITY,False)
                board[i][j] = ' '
                
                if score > bestScore:
                    bestScore = score
                    bestMove = (i,j)
    if bestMove != 0:
        board[bestMove[0]][bestMove[1]] = COMPUTER

def computer_easy():
    list_move = empty_space()

    bestMove = random.choice(list_move)

    board[bestMove[0]][bestMove[1]] = COMPUTER

def computer_normal():
    bestScore = INFINITY
    bestMove = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = COMPUTER
                score = minimax(board,0,INFINITY,-1*INFINITY,False,limit=3)
                board[i][j] = ' '
                
                if score > bestScore:
                    bestScore = score
                    bestMove = (i,j)

    if bestMove != 0:
        board[bestMove[0]][bestMove[1]] = COMPUTER


def checkgame():
    result = check()
    if result != 0:
        return True,result
    elif not ismoveleft():
        return True,0
    return False,0

board = [[' ',' ',' '],
         [' ',' ',' '],
         [' ',' ',' ']]

print(*board,sep='\n')
result = 0
isFinish = False

while True:
    
    isFinish,result = checkgame()
    if isFinish:break
    player()
    computer_hard()
    print(*board,sep='\n')
    

if result>0:
    print("bot wins")
elif result<0:
    print("player wins")
else: print("draw")
    



   

    



