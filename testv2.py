import random
zobTable = [[[random.randint(1,2**10 - 1) for i in range(2)]for j in range(3)]for k in range(3)]

def indexing(piece):
    ''' mapping X and O to a particular number'''
    if (piece=='X'):
        return 0
    if (piece=='O'):
        return 1
    else:
        return -1
def computeHash(board):
    h = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != '-':
                piece = indexing(board[i][j])
                h ^= zobTable[i][j][piece]
    return h

def main():
    # X is player one and O is player 2
    # a [3][3] format board
    board = [
        ['-', 'O', 'X'],
        ['-', 'X', '-'],
        ['O', '-', 'O'],
    ]

    hashValue = computeHash(board)
    print("Current Board is :")
    print(*board,sep='\n')

    print( "\nThe Current hash is : ",hashValue,"\n")

    # an exaple of channge in game state and how it affects the hashes

    # Add X at [2][1] to disrupt the O's winning strategy

    piece = 'X'

    board[2][1] = piece
    hashValue ^= zobTable[2][1][indexing(piece)]
    print("The new board is :")
    print(*board,sep='\n')

    print("\nHash after the move is : ",hashValue,"\n")

if __name__ == "__main__":
    main()