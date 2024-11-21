###################################################################################################################################
# Deterministic Method
###################################################################################################################################
class Cell:
    def __init__(self, owner=-1):
        self.owner = owner  # 0=black, 1=white, -1=blank, 2=possible move

    def getOwner(self):
        return self.owner

    def setOwner(self, int):
        try:
            if int in [-1, 0, 1, 2]:
                self.owner = int
            else:
                raise ValueError("The values must be -1, 0, 1, 2")
        except ValueError as ve:
            print(ve)

class Reversi30:
    def __init__(self, pid=0, size=8):
        self.pid = pid      # 0=black, 1=white
        self.size = size    # even number, size of the board

    @staticmethod
    def getPlayerName():
        return "Player1"

    def setPid(self, int):
        try:
            if int in [0, 1]:
                self.pid = int
            else:
                raise ValueError("There are two players, 0 for black and 1 for white")
        except ValueError as ve:
            print(ve)

    def setBoardSize(self, int):
        try:
            if int % 2 == 0:
                self.size = int
            else:
                raise ValueError("The board size must be an even number")
        except ValueError as ve:
            print(ve)
'''
     def setBoard(self, size=8):     # Creates the initial board
         board = []
         for i in range(size):
             row = [Cell() for j in range(size)]      # Creates the board as a list of Cells
             board.append(row)
         # Sets initial positions on the board
         board[3][3].setOwner(1)
         board[4][4].setOwner(1)
         board[3][4].setOwner(0)
         board[4][3].setOwner(0)
         return board

     def printBoard(self, board):    # Converts the board to a list of ints using the getOwner function
         print("   0 1 2 3 4 5 6 7")
         print("  -----------------")
         for i in range(self.size):
             print("{:d} |".format(i), end="")     # end="" keeps it on the same line
             for j in range(self.size):
                 owner = board[i][j].getOwner()
                 if owner == -1:
                     print("-", end=" ")
                 else:
                     print(owner, end=" ")
             print("|")
         print("  -----------------")
'''
    def findNeighbours(self, board):
        find_cells = []
        for i in range(self.size):      # Finds the black or white Cells on the board based on the pid value
            for j in range(self.size):
                if board[i][j].getOwner() == self.pid:
                    find_cells.append((i,j))

        dir = [(0,-1), (0,1), (1,0), (-1,0), (1,-1), (1, 1), (-1, -1), (-1, 1)] # up, down, right, left, upright, downright, upleft, downleft
        for x, y in dir:
            for i, j in find_cells:
                i += x
                j += y
                while i >= 0 and i < self.size and j >= 0 and j < self.size and board[i][j].getOwner() == 1 - self.pid: # Looks for black if pid=1 (white)
                    i += x                                                                                              # Looks for white if pid=0 (black)
                    j += y
                    if i < 0 or i >= self.size or j < 0 or j >= self.size:  # Keeps the values within the board size defined by the instance var size
                        break;
                    if board[i][j].getOwner() == -1:
                        board[i][j].setOwner(2)
                    elif board[i][j].getOwner() == self.pid or board[i][j].getOwner() == 2:
                        break;
        return board

    def placeTile(self, board):
        board = self.findNeighbours(board)
        moves = []
        best_move = None

        for i in range(self.size):      # Finds possible moves on the board, i.e., pid=2
            for j in range(self.size):
                if board[i][j].getOwner() == 2:
                    moves.append((i,j))

        if len(moves) == 0:        # If there are no moves, return the empty tuple
            return best_move

        for move in moves:         # If any corner is a possible move, it is chosen immediately
            if move in [(0,0), (0,7), (7,0), (7,7)]:
                return move

        best_score = -1
        dir = [(0, -1), (0, 1), (1, 0), (-1, 0), (1, -1), (1, 1), (-1, -1), (-1, 1)]
        for move in moves:
            score = 0           # The number of opponent's cells between the player's cells in all directions
            for x, y in dir:
                i, j = move
                score_add = 0       # Defines score_add to count the score of each direction
                i += x
                j += y
                while i >= 0 and i < self.size and j >= 0 and j < self.size and board[i][j].getOwner() == 1 - self.pid:
                    i += x
                    j += y
                    score_add += 1
                    if i < 0 or i >= self.size or j < 0 or j >= self.size:
                        break;
                    if board[i][j].getOwner() == -1 or board[i][j].getOwner() == 2:
                        break;
                    elif board[i][j].getOwner() == self.pid:
                        score += score_add                      # Add score_add to score only when a direction ends in a player's cell
            if score > best_score:      # If multiple moves provide the same maximum score
                best_score = score       # It selects the first one it finds
                best_move = move
        return best_move #, best_score, moves

    def findTakeOverCells(self, board, row, col):
        # board = self.findNeighbours(board) Δεν χρειάζονται οι δυνατές κινήσεις σε αυτή την μέθοδο
        take_over_cells = []
        dir = [(0, -1), (0, 1), (1, 0), (-1, 0), (1, -1), (1, 1), (-1, -1), (-1, 1)]
        for x, y in dir:
            i, j = row, col
            i += x
            j += y
            cells_to_take_over = []     # List to store opponent's cells for takeover in each direction
            while i >= 0 and i < self.size and j >= 0 and j < self.size and board[i][j].getOwner() == 1 - self.pid:
                cells_to_take_over.append((i, j))
                i += x
                j += y
                if i < 0 or i >= self.size or j < 0 or j >= self.size:
                    break;
                if board[i][j].getOwner() == -1: # or board[i][j].getOwner() == 2:
                    break;
                elif board[i][j].getOwner() == self.pid:        # If the algorithm ends in a player's cell, only then is it added
                    take_over_cells += cells_to_take_over       # cells_to_take_over is added to take_over_cells, otherwise continues checking other directions
                    break;                                      
        return list(set(take_over_cells))   # Written this way to remove duplicates (they appeared in some cases)

    def applyChanges(self, board):
        board = self.findNeighbours(board)              # Get the board from findNeighbours to use
        best_move = self.placeTile(board)               # placeTile needs the possible moves to evaluate them

        if best_move is None:                           
#           for i in range(self.size):                  # Converts cells with owner 2 to -1
#               for j in range(self.size):
#                   if board[i][j].getOwner() == 2:
#                       board[i][j].setOwner(-1)
            return board
        else:
            i, j = best_move
            take_over_cells = self.findTakeOverCells(board, row=i, col=j)
            board[i][j].setOwner(self.pid)              # Places the player's cell in the best position

            for cell in take_over_cells:                # Takes the opponent's cells
                i, j = cell
                board[i][j].setOwner(self.pid)

            for i in range(self.size):                  # Converts cells with owner 2 to -1
                for j in range(self.size):
                    if board[i][j].getOwner() == 2:
                        board[i][j].setOwner(-1)
            return board

# # create an instance of the Reversi1 class with size 8
# game = Reversi30(0,8)
# # get the starting board
# board = game.setBoard()
# # print the starting board
# print("Starting board:")
# game.printBoard(board)
# # find the neighbors of each cell on the board
# print("Possible moves:")
# board = game.findNeighbours(board)
# game.printBoard(board)
# # place a tile on the board using the algorithm
# best_move = game.placeTile(board)
# # apply the changes to the board
# board = game.applyChanges(board)
# # print the board after the tile has been placed and changes have been made
# print("Board after placing tile and applying changes:")
# game.printBoard(board)

# print('\n\n')

# # create an instance of the Reversi30 class with size 8
# game = Reversi30(1,8)
# # create an example board
# exboard = game.setBoard()
# exboard[3][3].setOwner(0)
# exboard[4][4].setOwner(0)
# exboard[3][5].setOwner(0)
# exboard[2][4].setOwner(0)
# exboard[5][3].setOwner(0)
# exboard[5][4].setOwner(1)
# exboard[5][5].setOwner(1)
# exboard[5][6].setOwner(1)
# exboard[2][0].setOwner(1)
# exboard[2][1].setOwner(1)
# exboard[2][2].setOwner(1)
# exboard[2][3].setOwner(1)
# exboard[1][3].setOwner(1)
# exboard[0][3].setOwner(1)
# exboard[3][2].setOwner(1)
# exboard[4][2].setOwner(1)
# print("Example board:")
# game.printBoard(exboard)
# # find the neighbors of each cell on the board
# print("Possible moves for player {:d}:".format(game.pid))
# exboard = game.findNeighbours(exboard)
# game.printBoard(exboard)
# # place a tile on the board using the algorithm
# best_move = game.placeTile(exboard)
# print("Best Move:", best_move)
# # find the take over cells
# take_over_cells = game.findTakeOverCells(exboard, best_move[0], best_move[1])
# print("Cells to take over:", take_over_cells)
# # apply the changes to the board
# exboard = game.applyChanges(exboard)
# # print the board after the tile has been placed and changes have been made
# print("Board after placing tile and applying changes:")
# game.printBoard(exboard)

# print('\n\n')

# # create an instance of the Reversi30 class with size 8
# game = Reversi30(1,8)
# # create an example board
# exboard1 = game.setBoard()
# exboard1[3][3].setOwner(0)
# exboard1[5][3].setOwner(0)
# exboard1[1][3].setOwner(0)
# exboard1[3][5].setOwner(0)#
# exboard1[2][0].setOwner(1)
# exboard1[2][4].setOwner(1)
# exboard1[2][1].setOwner(1)
# exboard1[2][2].setOwner(1)
# exboard1[2][3].setOwner(1)
# exboard1[3][2].setOwner(1)
# exboard1[3][4].setOwner(1)
# exboard1[4][2].setOwner(1)
# exboard1[4][4].setOwner(1)
# exboard1[5][4].setOwner(1)
# exboard1[5][5].setOwner(1)
# exboard1[5][6].setOwner(1)
# print("Example board:")
# game.printBoard(exboard1)
# # find the neighbors of each cell on the board
# print("Possible moves for player {:d}:".format(game.pid))
# exboard1 = game.findNeighbours(exboard1)
# game.printBoard(exboard1)
# # place a tile on the board using the algorithm
# best_move = game.placeTile(exboard1)
# print("Best Move:", best_move)
# # find the take over cells
# take_over_cells = game.findTakeOverCells(exboard1, best_move[0], best_move[1])
# print("Cells to take over:", take_over_cells)
# # apply the changes to the board
# exboard = game.applyChanges(exboard1)
# # print the board after the tile has been placed and changes have been made
# print("Board after placing tile and applying changes:")
# game.printBoard(exboard1)

# print('\n\n')

# # create an instance of the Reversi30 class with size 8, Test: Corner Move
# game = Reversi30(1,8)
# # create an example board
# exboard = game.setBoard()
# exboard[3][3].setOwner(1)
# exboard[3][4].setOwner(0)
# exboard[4][3].setOwner(0)
# exboard[4][4].setOwner(1)
# exboard[4][5].setOwner(0)
# exboard[5][1].setOwner(1)
# exboard[5][2].setOwner(1)
# exboard[5][3].setOwner(1)
# exboard[5][4].setOwner(1)
# exboard[5][5].setOwner(1)
# exboard[6][1].setOwner(0)
# exboard[6][3].setOwner(0)
# print("Example board:")
# game.printBoard(exboard)
# # find the neighbors of each cell on the board
# print("Possible moves for player {:d}:".format(game.pid))
# exboard = game.findNeighbours(exboard)
# game.printBoard(exboard)
# # place a tile on the board using the algorithm
# best_move = game.placeTile(exboard)
# print("Best Move:", best_move)
# # find the take over cells
# take_over_cells = game.findTakeOverCells(exboard, best_move[0], best_move[1])
# print("Cells to take over:", take_over_cells)
# # apply the changes to the board
# exboard = game.applyChanges(exboard)
# # print the board after the tile has been placed and changes have been made
# print("Board after placing tile and applying changes:")
# game.printBoard(exboard)

# print('\n\n')

# # create an instance of the Reversi30 class with size 8, Test: No move
# game = Reversi30(1,8)
# # create an example board
# exboard = game.setBoard()
# for i in range(0,8):
#     exboard[i][7].setOwner(0)
# for i in range(0,4):
#     exboard[0][i].setOwner(0)
# exboard[0][5].setOwner(1)
# exboard[0][6].setOwner(0)
# for i in range(0,5):
#     exboard[1][i].setOwner(1)
# exboard[1][5].setOwner(0)
# exboard[1][6].setOwner(0)
# exboard[1][7].setOwner(0)
# exboard[2][0].setOwner(0)
# exboard[2][1].setOwner(1)
# exboard[2][2].setOwner(1)
# exboard[2][3].setOwner(1)
# exboard[2][4].setOwner(0)
# exboard[2][5].setOwner(1)
# exboard[2][6].setOwner(0)
# exboard[3][0].setOwner(0)
# exboard[3][1].setOwner(0)
# exboard[3][2].setOwner(1)
# exboard[3][3].setOwner(0)
# exboard[3][4].setOwner(1)
# exboard[3][5].setOwner(1)
# exboard[3][6].setOwner(1)
# exboard[4][0].setOwner(0)
# exboard[4][1].setOwner(1)
# exboard[4][2].setOwner(0)
# exboard[4][3].setOwner(0)
# exboard[4][4].setOwner(1)
# exboard[4][5].setOwner(1)
# exboard[4][6].setOwner(0)
# for i in range(0,4):
#     exboard[5][i].setOwner(0)
# for i in range(0,3):
#     exboard[6][i].setOwner(0)
# for i in range(0,7):
#     exboard[7][i].setOwner(0)
# for i in range(0,3):
#     exboard[6][4+i].setOwner(1)
# exboard[5][6].setOwner(0)
# exboard[5][5].setOwner(0)
# exboard[5][4].setOwner(0)
# exboard[6][3].setOwner(1)
# print("Example board:")
# game.printBoard(exboard)
# # find the neighbors of each cell on the board
# print("Possible moves for player {:d}:".format(game.pid))
# exboard = game.findNeighbours(exboard)
# game.printBoard(exboard)
# # place a tile on the board using the algorithm
# best_move = game.placeTile(exboard)
# print("Best Move:", best_move)
# # find the take over cells
# if best_move == None:
#     # apply the changes to the board
#     exboard = game.applyChanges(exboard)
#     take_over_cells = []
# else:
#     take_over_cells = game.findTakeOverCells(exboard, best_move[0], best_move[1])
#     # apply the changes to the board
#     exboard = game.applyChanges(exboard)
# print("Cells to take over:", take_over_cells)
# # print the board after the tile has been placed and changes have been made
# print("Board after placing tile and applying changes:")
# game.printBoard(exboard)
