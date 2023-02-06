import random


PLAYER = -1
COMPUTER = 1
EMPTY = 0
INFINITY = -1000

#Cato is the name of the AI that will play this tic tac toe game :)
class Cato:
    COUNT = 0
    def __init__(self) -> None:
        #self.memorizing_moves = {}
        #self.killer_moves = deque()
        pass


    def play(self,board_game):

        bestMove = 0
        #first play
        if (board_game.totalplay <= 0 and board_game.size == 3) or (board_game.totalplay <= 2 and board_game.size == 5):
            list_move = self.empty_space(board_game)
            if board_game.size == 3 and board_game.at(1,1) == EMPTY:
                bestMove = (1,1)
            elif board_game.size == 5 and board_game.at(2,2) == EMPTY:
                bestMove = (2,2)
            else: bestMove = random.choice(list_move)
        #elif board_game.size == 5 and board_game.totalplay == 3:    #defend strategy
        #    bestMove = self.defend(board_game)
        
        if bestMove == 0:
            bestScore = INFINITY
            limit_depth = 0
            if board_game.size == 5:
                limit_depth = 3
                if board_game.totalplay >= 17:limit_depth = 5
                elif board_game.totalplay >= 13:limit_depth = 4


            children = sorted(self.getChildren(board_game,COMPUTER),key=lambda x: x[0],reverse=True)
            for child_move in children:
                score = self.minimax(board_game,0,INFINITY,-1*INFINITY,False,child_move[1],limit_depth)
                if score > bestScore:
                    bestScore = score
                    bestMove = child_move[1]
                
                

        board_game.place(bestMove[0],bestMove[1],COMPUTER)


    def minimax(self,board_game,depth,a,b,MAX,move,limit=0):
         
        board_game.place(*move)
        
        '''
        memory = self.memorizing_moves.get((board_game.ZobristValue,Maximize),None)
        if memory != None:
            board_game.takeout(move[0],move[1])
            return memory
        '''

        result = self.check_board(board_game)
        if result != 0:
            board_game.takeout(move[0],move[1])
            if result > 0:
                return result - depth
            elif result < 0:
                return result + depth

        if depth >= limit and limit > 0:
            board_game.takeout(move[0],move[1])
            return 0

        if not board_game.ismoveleft():
            board_game.takeout(move[0],move[1])
            return 0

        value = 0
        if MAX:
            value = INFINITY
            children = sorted(self.getChildren(board_game,COMPUTER),key=lambda x: x[0],reverse=True)
            for child_move in children:
                value = max(self.minimax(board_game,depth+1,a,b,False,child_move[1],limit),value)
                a = max(a,value)
                if b <= a:
                    break

        else:
            value = -1*INFINITY
            children = sorted(self.getChildren(board_game,PLAYER),key=lambda x: x[0])
            for child_move in children:
                value = min(self.minimax(board_game,depth+1,a,b,True,child_move[1],limit),value)
                b = min(b,value)
                if b <= a:
                    break


        #if value != 0:self.memorizing_moves[(board_game.ZobristValue,Maximize)] = value
        board_game.takeout(move[0],move[1])
        return value


    def defend(self,board_game):
        move_pair = ()
        for i,move in enumerate(self.danger_moves):
            if board_game.at(move[0],move[1]) == PLAYER:
                move_pair += (i,)
                if len(move_pair) >= 2:break

        if len(move_pair) == 2:
            return self.strategy_defend[move_pair]
        else: return 0

    def getChildren(self,board_game,who):
        child_moves = []
        for i in random.sample(range(board_game.size),board_game.size):
            for j in random.sample(range(board_game.size),board_game.size):
                if board_game.at(i,j) == EMPTY:
                    board_game.place(i,j,who)
                    heuristic_value = self.heuristic(board_game,i,j,who)
                    move = (heuristic_value,(i,j,who))
                    child_moves.append(move)
                    board_game.takeout(i,j)

        return child_moves         

    def heuristic(self,board_game,i,j,who):
        heuristic_value = self.estimate(board_game)
        if board_game.size == 5:
            if 0 < i < 4 and 0 < j < 4:
                heuristic_value += 1
        elif board_game.size == 3:
            if i == 1 and j == 1:
                heuristic_value += 1

        if i == j or j == board_game.size - 1 - i:
            heuristic_value += 1 

        if (board_game.at(i-1,j) == -1*who or board_game.at(i+1,j) == -1*who
            or board_game.at(i-1,j-1) == -1*who or board_game.at(i-1,j+1) == -1*who
            or board_game.at(i+1,j-1) == -1*who or board_game.at(i+1,j+1) == -1*who
            or board_game.at(i,j-1) == -1*who or board_game.at(i,j+1) == -1*who):
            heuristic_value += 1

        return heuristic_value


    def estimate(self,board_game):
        #horizontal
        for row in range(board_game.size):
            for col in range(board_game.size):
                count = 1
                if board_game.at(row,col) == EMPTY:continue
                for i in range(col+1,board_game.size):
                    if board_game.at(row,col) == board_game.at(row,i):
                        count += 1
                    else: break
                if count == 4:return self.evaluate(board_game.at(row,col),count)
                elif count == 3 and board_game.size == 5 or count >= 2 and board_game.size == 2:
                    if board_game.at(row,col-1) == EMPTY or board_game.at(row,col+1) == EMPTY:
                        return self.evaluate(board_game.at(row,col),count)

        #vertical
        for col in range(board_game.size):
            for row in range(board_game.size):
                count = 1
                if board_game.at(row,col) == EMPTY:continue
                for i in range(row+1,board_game.size):
                    if board_game.at(row,col) == board_game.at(i,col):
                        count += 1
                    else:break
                if count == 4: return self.evaluate(board_game.at(row,col),count)
                elif count == 3 and board_game.size == 5 or count >= 2 and board_game.size == 2:
                    if board_game.at(row+1,col) == EMPTY or board_game.at(row-1,col) == EMPTY:
                        return self.evaluate(board_game.at(row,col),count)

        if board_game.size == 5:
            #diagonal
            for time in range(-1,2):    #from top left to bottow right
                for i in range(board_game.size - time):
                    count = 1 
                    if board_game.at(i,i+time) == EMPTY or board_game.at(i,i+time) == None:continue
                    for j in range(i+1,board_game.size - time):
                        if board_game.at(i,i+time) == board_game.at(j,j+time):
                            count += 1
                        else:break
                    if count == 4:return self.evaluate(board_game.at(i,i+time),count)
                    elif count == 3: 
                        if board_game.at(i-1,i+time -1) == EMPTY or board_game.at(i+1,i+time+1) == EMPTY:
                            return self.evaluate(board_game.at(i,i+time),count)

            for time in range(-1,2):    #from top right to bottom left
                for i in range(board_game.size - time):
                    count = 1
                    if board_game.at(i,board_game.size + time - i) == EMPTY or board_game.at(i,board_game.size+time - i) == None:continue
                    for j in range(i+1,board_game.size - time):
                        if board_game.at(i,board_game.size + time - i) == board_game.at(j,board_game.size + time - j):
                            count += 1
                        else:break
                    if count == 4:return self.evaluate(board_game.at(i,board_game.size + time - i),count)
                    elif count == 3: 
                        if board_game.at(i+1,board_game.size + time - i+1) == EMPTY or board_game.at(i-1,board_game.size + time - i - 1) == EMPTY:
                            return self.evaluate(board_game.at(i,board_game.size + time - i),count)
        elif board_game.size == 3:
            for i in range(board_game.size - 1):
                count = 1
                if board_game.at(i,i) == EMPTY or board_game.at(i,i) == None:continue
                for j in range(i+1,board_game.size):
                    if board_game.at(i,i) == board_game.at(j,j):
                        count += 1
                    else: break
                if count >= 2:
                    return self.evaluate(board_game.at(i,i),count)
            for i in range(board_game.size - 1):
                count = 1
                if board_game.at(i,board_game.size - 1 - i) == EMPTY or board_game.at(i,board_game.size - 1 - i) == None:continue
                for j in range(i+1,board_game.size):
                    if board_game.at(i,board_game.size - 1 - i) == board_game.at(j,board_game.size - 1 - j):
                        count += 1
                    else: break
                if count >= 2:
                    return self.evaluate(board_game.at(i,board_game.size - 1 - i),count)

            
        return 0


    


    def check_board(self,board_game):
        '''
        return 100 if bot wins
              -100 if player wins
                 0 if draw
        '''

        if board_game.size == 3:
            return self.check_board_3x3(board_game)
        elif board_game.size == 5:
            return self.check_board_5x5(board_game)



    def check_board_5x5(self,board_game,needResult=False):

        result = []
        if board_game.totalplay < 3 or not board_game.ismoveleft():
            if needResult: return 0,None
            return 0

        #horizontal
        for i,row in enumerate(board_game.board):    
            count = 0
            result = []
            check_block = row[2]
            if check_block == EMPTY:continue
            for j in range(0,4):
                if row[j] != check_block:
                    count = 0
                    result = []
                    break
                else:
                    count += 1
                    if needResult:result.append((i,j))
            
            if count >= 4:
                if needResult: 
                    return self.evaluate(check_block,count),result
                else:return self.evaluate(check_block,count)
            for j in range(1,5):
                if row[j] != check_block:
                    count = 0
                    result = []
                    break
                else:
                    count += 1
                    if needResult:result.append((i,j))
            if count >= 4:
                if needResult: 
                    return self.evaluate(check_block,count),result
                else:return self.evaluate(check_block,count)
            
        #vertical
        for col in range(board_game.size):
            count = 0
            result = []
            check_block = board_game.at(2,col)
            if check_block == EMPTY:continue
            for i in range(0,4):
                if board_game.at(i,col) != check_block:
                    count = 0
                    result = []
                    break
                else:
                    count += 1
                    if needResult:result.append((i,col))
            if count >= 4:
                if needResult: 
                    return self.evaluate(check_block,count),result
                else:return self.evaluate(check_block,count)
            for i in range(1,5):
                if board_game.at(i,col) != check_block:
                    count = 0
                    result = []
                    break
                else:
                    count += 1
                    if needResult:result.append((i,col))
            if count >= 4:
                if needResult: 
                    return self.evaluate(check_block,count),result
                else:return self.evaluate(check_block,count)
        
        #diagonal
        count = 0
        result = []
        check_block = board_game.at(2,2)
        for times in range(2):
            if check_block == EMPTY:
                check_block = board_game.at(0,1)
                continue
            for i in range(0,4):
                if board_game.at(i,i+times) != check_block:
                    count = 0
                    result = []
                    break
                else:
                    count += 1
                    if needResult:result.append((i,i+times))
            if count >= 4:
                if needResult: 
                    return self.evaluate(check_block,count),result
                else:return self.evaluate(check_block,count)
            check_block = board_game.at(0,1)
        check_block = board_game.at(2,2)
        for times in range(2):
            if check_block == EMPTY:
                check_block = board_game.at(1,0)
                continue
            for i in range(1,5):
                if board_game.at(i,i-times) != check_block:
                    count = 0
                    result = []
                    break
                else:
                    count += 1
                    if needResult:result.append((i,i-times))
            if count >= 4:
                if needResult: 
                    return self.evaluate(check_block,count),result
                else:return self.evaluate(check_block,count)
            check_block = board_game.at(1,0)

        check_block = board_game.at(2,2)
        for times in range(2):
            if check_block == EMPTY:
                check_block = board_game.at(0,3)
                continue
            for i in range(0,4):
                if board_game.at(i,board_game.size - 1 - i -times) != check_block:
                    count = 0
                    result = []
                    break
                else:
                    count += 1
                    if needResult:result.append((i,board_game.size - 1 - i -times))
            if count >= 4:
                if needResult: 
                    return self.evaluate(check_block,count),result
                else:return self.evaluate(check_block,count)
            check_block = board_game.at(0,3)
        check_block = board_game.at(2,2)
        for times in range(2):
            if check_block == EMPTY:
                check_block = board_game.at(1,4)
                continue
            for i in range(1,5):
                if board_game.at(i,board_game.size - 1 - i +times) != check_block:
                    count = 0
                    result = []
                    break
                else:
                    count += 1
                    if needResult:result.append((i,board_game.size - 1 - i +times))
            if count >= 4:
                if needResult: 
                    return self.evaluate(check_block,count),result
                else:return self.evaluate(check_block,count)
            check_block = board_game.at(1,4)

        if needResult: return 0,None
        return 0    

        


    def check_board_3x3(self,board_game,needResult=False):

        result = []
        for i,row in enumerate(board_game.board):
            result = []
            if row[0] == row[1] and row[1] == row[2]:
                if row[0] == COMPUTER:
                    if needResult:
                        result=[(i,0),(i,1),(i,2)]
                        return 100,result
                    return 100
                elif row[0] == PLAYER:
                    if needResult:
                        result=[(i,0),(i,1),(i,2)]
                        return -100,result
                    return -100
        
        for col in range(3):
            result = []
            if board_game.at(0,col) == board_game.at(1,col) and board_game.at(1,col) == board_game.at(2,col):
                if board_game.at(0,col) == COMPUTER:
                    if needResult:
                        result=[(0,col),(1,col),(2,col)]
                        return 100,result
                    return 100
                elif board_game.at(0,col) == PLAYER:
                    if needResult:
                        result=[(0,col),(1,col),(2,col)]
                        return -100,result
                    return -100

        if board_game.at(0,0) == board_game.at(1,1) and board_game.at(1,1)== board_game.at(2,2):
            if board_game.at(1,1) == COMPUTER:
                if needResult:
                    result=[(0,0),(1,1),(2,2)]
                    return 100,result
                return 100
            elif board_game.at(1,1) == PLAYER:
                if needResult:
                    result=[(0,0),(1,1),(2,2)]
                    return -100,result
                return -100

        if board_game.at(0,2) == board_game.at(1,1) and board_game.at(1,1) == board_game.at(2,0):
            if board_game.at(1,1) == COMPUTER:
                if needResult:
                    result=[(0,2),(1,1),(2,0)]
                    return 100,result
                return 100
            elif board_game.at(1,1) == PLAYER:
                if needResult:
                    result=[(0,2),(1,1),(2,0)]
                    return -100,result
                return -100

        if needResult:return 0,None
        return 0

    def evaluate(self,block,value):
        if value == 4:
            if block == COMPUTER:
                return 100
            elif block == PLAYER:
                return -100
        elif value >= 2:
            if block == COMPUTER:
                return 10
            elif block == PLAYER:
                return -10
        return 0

    def check_board_result(self,board_game):
        '''
        return 100 if bot wins
              -100 if player wins
                 0 if draw
            and a list of wining moves
        '''

        if board_game.size == 3:
            return self.check_board_3x3(board_game,needResult=True)
        elif board_game.size == 5:
            return self.check_board_5x5(board_game,needResult=True)


    def empty_space(self,board_game):
        result = []
        if board_game.size == 5:
            for i in range(1,4,2):
                for j in range(1,4,2):
                    if board_game.at(i,j) == EMPTY:
                        result.append((i,j))
        elif board_game.size == 3:
            for i in range(board_game.size):
                for j in range(board_game.size):
                    if board_game.at(i,j) == EMPTY:
                        result.append((i,j))
        
        return result



class BoardMap:
    def __init__(self,size) -> None:
        self.totalplay = 0
        self.size = size
        self.board = []
        for i in range(size):
            temp = [EMPTY] * size
            self.board.append(temp)


    def at(self,row,col):
        if row < 0 or col < 0 or row >= self.size or col >= self.size:return None 
        else:return self.board[row][col]

    def place(self,row,col,who):
        self.board[row][col] = who
        self.totalplay += 1

        #print(self.totalplay)

    def takeout(self,row,col):
        self.board[row][col] = EMPTY
        self.totalplay -= 1


    def ismoveleft(self):
        if self.totalplay >= (self.size*self.size):
            return False
        return True


    def clear(self):
        self.board.clear()
        for i in range(self.size):
            temp = [EMPTY] * self.size
            self.board.append(temp)
        self.totalplay = 0